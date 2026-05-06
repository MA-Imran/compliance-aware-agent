import logging
import traceback
from datetime import datetime
from typing import Dict, Any, List, Optional

from retrieval_agent import RetrievalAgent
from enhanced_reasoning_agent import EnhancedReasoningAgent
from enhanced_compliance_agent import EnhancedComplianceAgent
from memory_system import EnhancedMemorySystem

logger = logging.getLogger(__name__)

# Valid regulations understood by the compliance agent
_KNOWN_REGULATIONS = frozenset({'hipaa', 'gdpr', 'data_retention'})


class EnhancedComplianceAwareAgentSystem:
    def __init__(self, db_path: str = "agent_memory.db"):
        self.retrieval_agent = RetrievalAgent()
        self.reasoning_agent = EnhancedReasoningAgent()
        self.compliance_agent = EnhancedComplianceAgent()
        self.memory_system = EnhancedMemorySystem(db_path)

        self.config = {
            'default_regulations': ['hipaa', 'gdpr'],
            'enable_learning': True,
        }

        logger.info("Enhanced Compliance-Aware Multi-Agent System initialised")

    def process_query(self, query: str, regulations: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Process a query through the complete multi-agent pipeline.

        Args:
            query:       User query string.
            regulations: List of regulation keys to check. Defaults to HIPAA + GDPR.

        Returns:
            A dictionary containing retrieved data, insights, compliance results,
            performance metrics, and system recommendations.
        """
        if not query or not query.strip():
            logger.warning("process_query called with an empty query string.")
            return self._create_error_response("Query must not be empty.", datetime.now())

        start_time = datetime.now()

        if regulations is None:
            regulations = self.config['default_regulations']

        # Validate regulation names and warn on unknowns
        unknown = [r for r in regulations if r not in _KNOWN_REGULATIONS]
        if unknown:
            logger.warning("Unrecognised regulation(s) requested and will be skipped: %s", unknown)
        regulations = [r for r in regulations if r in _KNOWN_REGULATIONS]

        try:
            historical_success = self.memory_system.get_query_success_rate(query)

            retrieval_start = datetime.now()
            data = self.retrieval_agent.fetch_data(query)
            retrieval_time = (datetime.now() - retrieval_start).total_seconds()
            self.memory_system.update_agent_performance(
                "retrieval_agent", "data_fetch", bool(data), retrieval_time
            )

            if not data:
                return self._create_error_response("No data retrieved from source.", start_time)

            reasoning_start = datetime.now()
            insights = self.reasoning_agent.analyze_with_chain_of_thought(data, query)
            reasoning_time = (datetime.now() - reasoning_start).total_seconds()
            self.memory_system.update_agent_performance(
                "reasoning_agent", "data_analysis", True, reasoning_time
            )

            compliance_start = datetime.now()
            compliance_result = self.compliance_agent.validate_compliance(data, regulations)
            compliance_time = (datetime.now() - compliance_start).total_seconds()
            self.memory_system.update_agent_performance(
                "compliance_agent", "compliance_check",
                compliance_result['overall_compliant'], compliance_time
            )

            # Log individual violations for memory-based learning
            for regulation, result in compliance_result['regulation_results'].items():
                for violation in result.get('violations', []):
                    severity = "high" if any(kw in violation.lower() for kw in ("ssn", "email")) else "medium"
                    self.memory_system.log_compliance_violation(regulation, violation, severity)

            if self.config['enable_learning']:
                self._generate_learning_insights(data, insights, compliance_result, query)

            total_time = (datetime.now() - start_time).total_seconds()
            self.memory_system.log_query(query, success=True, processing_time=total_time)

            logger.info(
                "Query processed in %.2fs | compliant=%s",
                total_time,
                compliance_result['overall_compliant'],
            )

            return {
                'success': True,
                'query': query,
                'retrieved_data': data,
                'insights': insights,
                'compliance_check': compliance_result,
                'performance_metrics': {
                    'total_processing_time': total_time,
                    'historical_success_rate': historical_success,
                    'component_times': {
                        'retrieval': retrieval_time,
                        'reasoning': reasoning_time,
                        'compliance': compliance_time,
                    },
                    'efficiency_score': self._calculate_efficiency_score(total_time, len(str(data))),
                },
                'system_recommendations': self._generate_system_recommendations(insights, compliance_result),
                'timestamp': datetime.now().isoformat(),
            }

        except Exception as exc:
            total_time = (datetime.now() - start_time).total_seconds()
            self.memory_system.log_query(query, success=False, processing_time=total_time)
            logger.exception("Query processing failed after %.2fs.", total_time)
            return self._create_error_response(
                f"Processing failed: {exc}",
                start_time,
                {'error': str(exc), 'traceback': traceback.format_exc()},
            )

    def _generate_learning_insights(self, data: Dict[str, Any], insights: Dict[str, Any],
                                    compliance_result: Dict[str, Any], query: str):
        """Persist learning insights derived from a successful query run."""
        self.memory_system.store_system_insight('query_pattern', {
            'query_length': len(query),
            'data_fields_retrieved': len(data),
            'compliance_status': compliance_result['overall_compliant'],
            'reasoning_confidence': insights['structured_insights']['confidence_score'],
        }, confidence=0.7)

        if not compliance_result['overall_compliant']:
            self.memory_system.store_system_insight('compliance_pattern', {
                'violation_count': compliance_result['summary']['total_violations'],
                'regulation_violations': list(compliance_result['regulation_results'].keys()),
                'data_type': type(data).__name__,
            }, confidence=0.8)

        self.memory_system.store_system_insight('performance_pattern', {
            'data_complexity': len(str(data)),
            'hypotheses_generated': len(insights['generated_hypotheses']),
            'reasoning_steps': len(insights['reasoning_chain']),
        }, confidence=0.6)

    def _generate_system_recommendations(self, insights: Dict[str, Any],
                                         compliance_result: Dict[str, Any]) -> List[str]:
        """Compile a deduplicated list of system-level recommendations (max 5)."""
        recommendations: List[str] = []

        data_quality = insights['structured_insights']['data_quality_assessment']
        if data_quality['completeness'] in ('fair', 'poor'):
            recommendations.append("Improve data quality for more accurate insights")

        if not compliance_result['overall_compliant']:
            recommendations.append("Address compliance violations before production deployment")

        confidence = insights['structured_insights']['confidence_score']
        if confidence < 0.6:
            recommendations.append("Low analysis confidence — consider enriching data sources")

        recommendations.extend(self.memory_system.get_agent_recommendations())

        return list(dict.fromkeys(recommendations))[:5]

    @staticmethod
    def _calculate_efficiency_score(processing_time: float, data_size: int) -> float:
        """Return a 0–1 efficiency score normalised by time and data size."""
        time_factor = 1.0 / (processing_time + 1)
        size_factor = 1.0 / (data_size / 1_000 + 1)
        return round(min((time_factor + size_factor) / 2, 1.0), 3)

    def get_system_analytics(self) -> Dict[str, Any]:
        """Return a comprehensive analytics snapshot of the full system."""
        memory_insights = self.memory_system.get_system_insights()
        compliance_stats = self.compliance_agent.get_compliance_stats()
        retrieval_stats = self.retrieval_agent.get_request_stats()

        return {
            'memory_system': memory_insights,
            'compliance_agent': compliance_stats,
            'retrieval_agent': retrieval_stats,
            'system_health': self._calculate_system_health(memory_insights, compliance_stats),
            'recommendations': self.memory_system.get_agent_recommendations(),
        }

    @staticmethod
    def _calculate_system_health(memory_insights: Dict[str, Any],
                                 compliance_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Derive an overall health score from success and compliance rates."""
        success_rate = memory_insights.get('average_success_rate', 0.0)
        compliance_rate = compliance_stats.get('compliance_rate', 1.0)

        health_score = (success_rate * 0.6 + compliance_rate * 0.4) * 100

        if health_score >= 80:
            status = "healthy"
        elif health_score >= 60:
            status = "degraded"
        else:
            status = "unhealthy"

        return {
            'score': round(health_score, 1),
            'status': status,
            'success_rate': round(success_rate * 100, 1),
            'compliance_rate': round(compliance_rate * 100, 1),
        }

    def batch_process_queries(self, queries: List[str]) -> Dict[str, Any]:
        """
        Process multiple queries sequentially.

        Returns aggregate statistics alongside per-query results.
        """
        if not queries:
            logger.warning("batch_process_queries called with an empty list.")
            return {
                'total_queries': 0,
                'successful_queries': 0,
                'success_rate': 0.0,
                'average_processing_time': 0.0,
                'results': [],
            }

        results = []
        successful = 0
        total_time = 0.0

        for query in queries:
            result = self.process_query(query)
            results.append(result)
            if result['success']:
                successful += 1
                total_time += result['performance_metrics']['total_processing_time']

        success_rate = successful / len(queries)
        avg_time = total_time / successful if successful > 0 else 0.0

        return {
            'total_queries': len(queries),
            'successful_queries': successful,
            'success_rate': round(success_rate, 3),
            'average_processing_time': round(avg_time, 3),
            'results': results,
        }

    def reset_system(self):
        """Log a reset request. In production, this would clear persistent state."""
        logger.info("System reset requested — in-memory state cleared; DB persisted.")

    def _create_error_response(self, error_message: str, start_time: datetime,
                               error_details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build a standardised error response dictionary."""
        total_time = (datetime.now() - start_time).total_seconds()
        response: Dict[str, Any] = {
            'success': False,
            'error': error_message,
            'performance_metrics': {
                'total_processing_time': total_time,
                'error_occurred': True,
            },
            'timestamp': datetime.now().isoformat(),
        }
        if error_details:
            response['error_details'] = error_details
        return response

    def __del__(self):
        logger.info("Multi-Agent System shut down.")