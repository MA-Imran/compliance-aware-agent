import json
import logging
import sqlite3
import hashlib
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class EnhancedMemorySystem:
    def __init__(self, db_path: str = "agent_memory.db"):
        self.db_path = db_path
        self._init_database()

    @contextmanager
    def _get_connection(self):
        """Context manager that yields a database connection and guarantees cleanup."""
        conn = sqlite3.connect(self.db_path)
        # Enable WAL mode for better concurrent-access resilience
        conn.execute("PRAGMA journal_mode=WAL")
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_database(self):
        """Initialize SQLite database schema for persistent memory."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Query history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_hash TEXT UNIQUE,
                    query_text TEXT,
                    timestamp TEXT,
                    success_rate REAL DEFAULT 0,
                    execution_count INTEGER DEFAULT 1,
                    avg_processing_time REAL DEFAULT 0
                )
            ''')

            # Compliance violations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS compliance_violations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    violation_type TEXT,
                    description TEXT,
                    timestamp TEXT,
                    resolved BOOLEAN DEFAULT FALSE,
                    severity TEXT DEFAULT 'medium'
                )
            ''')

            # Agent performance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT,
                    task_type TEXT,
                    success_count INTEGER DEFAULT 0,
                    total_count INTEGER DEFAULT 0,
                    avg_response_time REAL,
                    last_updated TEXT
                )
            ''')

            # System insights table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    insight_type TEXT,
                    insight_data TEXT,
                    confidence REAL,
                    timestamp TEXT
                )
            ''')

            # Indexes for range queries used by analytics
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_query_history_timestamp
                ON query_history (timestamp)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_compliance_violations_timestamp
                ON compliance_violations (timestamp)
            ''')

    def log_query(self, query: str, success: bool = True, processing_time: float = 0.0):
        """Log a query with incremental success-rate and processing-time tracking."""
        query_hash = self._hash_query(query)
        current_time = datetime.now().isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT execution_count, success_rate, avg_processing_time '
                'FROM query_history WHERE query_hash = ?',
                (query_hash,)
            )
            result = cursor.fetchone()

            if result:
                execution_count = result['execution_count']
                old_success_rate = result['success_rate']
                old_avg_time = result['avg_processing_time'] or 0.0

                new_count = execution_count + 1
                new_success_rate = (old_success_rate * execution_count + int(success)) / new_count
                new_avg_time = (old_avg_time * execution_count + processing_time) / new_count

                cursor.execute('''
                    UPDATE query_history
                    SET execution_count = ?, success_rate = ?, avg_processing_time = ?, timestamp = ?
                    WHERE query_hash = ?
                ''', (new_count, new_success_rate, new_avg_time, current_time, query_hash))
            else:
                cursor.execute('''
                    INSERT INTO query_history
                        (query_hash, query_text, timestamp, success_rate, avg_processing_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (query_hash, query, current_time, float(success), processing_time))

    def log_compliance_violation(self, violation_type: str, description: str, severity: str = "medium"):
        """Log a compliance violation for audit and learning."""
        with self._get_connection() as conn:
            conn.execute('''
                INSERT INTO compliance_violations (violation_type, description, timestamp, severity)
                VALUES (?, ?, ?, ?)
            ''', (violation_type, description, datetime.now().isoformat(), severity))

    def get_query_success_rate(self, query: str) -> float:
        """Return the historical success rate for a query, defaulting to 0.5."""
        query_hash = self._hash_query(query)

        with self._get_connection() as conn:
            row = conn.execute(
                'SELECT success_rate FROM query_history WHERE query_hash = ?',
                (query_hash,)
            ).fetchone()

        return row['success_rate'] if row else 0.5

    def get_common_violations(self, days: int = 30) -> List[Dict[str, Any]]:
        """Return the most frequent unresolved compliance violations in the last *days* days."""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        with self._get_connection() as conn:
            rows = conn.execute('''
                SELECT violation_type, COUNT(*) AS count, severity
                FROM compliance_violations
                WHERE timestamp > ? AND resolved = FALSE
                GROUP BY violation_type, severity
                ORDER BY count DESC
                LIMIT 10
            ''', (cutoff_date,)).fetchall()

        return [{'type': r['violation_type'], 'count': r['count'], 'severity': r['severity']} for r in rows]

    def update_agent_performance(self, agent_name: str, task_type: str,
                                 success: bool, response_time: float):
        """Upsert agent performance metrics using an incremental moving average."""
        current_time = datetime.now().isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT success_count, total_count, avg_response_time
                FROM agent_performance
                WHERE agent_name = ? AND task_type = ?
            ''', (agent_name, task_type))
            result = cursor.fetchone()

            if result:
                success_count = result['success_count']
                total_count = result['total_count']
                old_avg_time = result['avg_response_time'] or 0.0

                new_success_count = success_count + int(success)
                new_total_count = total_count + 1
                new_avg_time = (old_avg_time * total_count + response_time) / new_total_count

                cursor.execute('''
                    UPDATE agent_performance
                    SET success_count = ?, total_count = ?, avg_response_time = ?, last_updated = ?
                    WHERE agent_name = ? AND task_type = ?
                ''', (new_success_count, new_total_count, new_avg_time,
                      current_time, agent_name, task_type))
            else:
                cursor.execute('''
                    INSERT INTO agent_performance
                        (agent_name, task_type, success_count, total_count, avg_response_time, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (agent_name, task_type, int(success), 1, response_time, current_time))

    def store_system_insight(self, insight_type: str, insight_data: Dict[str, Any], confidence: float = 0.8):
        """Persist a system-generated insight."""
        with self._get_connection() as conn:
            conn.execute('''
                INSERT INTO system_insights (insight_type, insight_data, confidence, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (insight_type, json.dumps(insight_data), confidence, datetime.now().isoformat()))

    def get_recent_insights(self, insight_type: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Return the most recent system insights, optionally filtered by type."""
        with self._get_connection() as conn:
            if insight_type:
                rows = conn.execute('''
                    SELECT insight_type, insight_data, confidence, timestamp
                    FROM system_insights
                    WHERE insight_type = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (insight_type, limit)).fetchall()
            else:
                rows = conn.execute('''
                    SELECT insight_type, insight_data, confidence, timestamp
                    FROM system_insights
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,)).fetchall()

        return [
            {
                'type': r['insight_type'],
                'data': json.loads(r['insight_data']),
                'confidence': r['confidence'],
                'timestamp': r['timestamp'],
            }
            for r in rows
        ]

    def get_system_insights(self) -> Dict[str, Any]:
        """Return a comprehensive snapshot of system health and performance."""
        with self._get_connection() as conn:
            total_queries = conn.execute(
                'SELECT COUNT(*) AS n FROM query_history'
            ).fetchone()['n']

            avg_row = conn.execute(
                'SELECT AVG(success_rate) AS avg FROM query_history'
            ).fetchone()
            avg_success = avg_row['avg'] if avg_row['avg'] is not None else 0.0

            agent_rows = conn.execute('''
                SELECT agent_name,
                       AVG(success_count * 1.0 / total_count) AS success_rate,
                       AVG(avg_response_time) AS avg_time
                FROM agent_performance
                GROUP BY agent_name
            ''').fetchall()

        agent_performance = {
            r['agent_name']: {
                'success_rate': r['success_rate'] or 0.0,
                'avg_response_time': r['avg_time'] or 0.0,
            }
            for r in agent_rows
        }

        if avg_success > 0.8:
            system_health = 'excellent'
        elif avg_success > 0.6:
            system_health = 'good'
        elif avg_success > 0.4:
            system_health = 'fair'
        else:
            system_health = 'poor'

        return {
            'total_queries_processed': total_queries,
            'average_success_rate': round(avg_success, 3),
            'common_compliance_issues': self.get_common_violations(days=7),
            'agent_performance': agent_performance,
            'system_health': system_health,
            'performance_trend': self._calculate_performance_trend(),
        }

    def _calculate_performance_trend(self) -> str:
        """Compare the last 7 days against the prior 7 days to detect trends."""
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        two_weeks_ago = (datetime.now() - timedelta(days=14)).isoformat()

        with self._get_connection() as conn:
            recent_row = conn.execute(
                'SELECT AVG(success_rate) AS avg FROM query_history WHERE timestamp > ?',
                (week_ago,)
            ).fetchone()
            previous_row = conn.execute(
                'SELECT AVG(success_rate) AS avg FROM query_history WHERE timestamp > ? AND timestamp <= ?',
                (two_weeks_ago, week_ago)
            ).fetchone()

        recent_success = recent_row['avg'] or 0.0
        previous_success = previous_row['avg'] or 0.0

        if recent_success > previous_success + 0.05:
            return 'improving'
        elif recent_success < previous_success - 0.05:
            return 'declining'
        return 'stable'

    def get_agent_recommendations(self) -> List[str]:
        """Generate up to 5 recommendations based on current system performance."""
        recommendations = []
        insights = self.get_system_insights()

        for agent, perf in insights['agent_performance'].items():
            if perf['success_rate'] < 0.6:
                recommendations.append(f"Review {agent} — low success rate detected")
            if perf['avg_response_time'] > 5.0:
                recommendations.append(f"Optimise {agent} — high average response time detected")

        if insights['common_compliance_issues']:
            top_issue = insights['common_compliance_issues'][0]
            recommendations.append(f"Address frequent '{top_issue['type']}' compliance violations")

        if insights['system_health'] in ('fair', 'poor'):
            recommendations.append("System performance needs attention — review logs and metrics")

        return recommendations[:5]

    @staticmethod
    def _hash_query(query: str) -> str:
        """Return a SHA-256 hex digest of the query string for deduplication."""
        return hashlib.sha256(query.encode()).hexdigest()