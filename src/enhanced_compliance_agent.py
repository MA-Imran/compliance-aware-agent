import re
import json
import logging
from collections import Counter
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Maximum number of compliance check records kept in memory
_MAX_LOG_SIZE = 1000


class EnhancedComplianceAgent:
    def __init__(self):
        # Pre-compile all regex patterns once to avoid repeated compilation overhead
        self._hipaa_patterns = {
            'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            'medical_terms': re.compile(
                r'\b(cancer|diabetes|HIV|AIDS|treatment|diagnosis|hypertension)\b',
                re.IGNORECASE
            ),
            'healthcare_facilities': re.compile(
                r'\b(hospital|clinic|medical center|physician|doctor)\b',
                re.IGNORECASE
            ),
        }
        self._gdpr_patterns = {
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
            'phone': re.compile(r'\b(\+?(\d{1,3})?[\s-]?)?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}\b'),
            'ip_address': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
        }

        self.compliance_rules = {
            'hipaa': self._check_hipaa_compliance,
            'gdpr': self._check_gdpr_compliance,
            'data_retention': self._check_data_retention,
        }
        self.compliance_log: List[Dict[str, Any]] = []

    def _check_hipaa_compliance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for HIPAA (Protected Health Information) violations."""
        violations: List[str] = []
        warnings: List[str] = []

        for field_name, field_value in data.items():
            if isinstance(field_value, str):
                if self._hipaa_patterns['ssn'].search(field_value):
                    violations.append(f"Potential SSN found in field '{field_name}'")

                if self._hipaa_patterns['medical_terms'].search(field_value):
                    warnings.append(f"Medical terminology found in field '{field_name}'")

                if self._hipaa_patterns['healthcare_facilities'].search(field_value):
                    warnings.append(f"Healthcare facility mention in field '{field_name}'")

            # Flag patient-related identifier fields (excluding allowed vital-sign fields)
            _vital_sign_fields = {'temperature', 'heart_rate', 'blood_pressure'}
            if (
                any(term in field_name.lower() for term in ('patient', 'medical', 'health'))
                and field_value
                and field_name not in _vital_sign_fields
            ):
                warnings.append(f"Potential patient identifier in field '{field_name}'")

        return {
            'is_compliant': len(violations) == 0,
            'violations': _dedup(violations),
            'warnings': _dedup(warnings),
            'rule_applied': 'HIPAA',
        }

    def _check_gdpr_compliance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for GDPR (personal data) violations."""
        violations: List[str] = []
        warnings: List[str] = []

        data_str = json.dumps(data)

        for data_type, pattern in self._gdpr_patterns.items():
            if pattern.search(data_str):
                violations.append(f"Potential {data_type.upper()} found in data")

        # Data minimisation check
        data_size = len(data_str)
        if data_size > 2000:
            violations.append("Data payload exceeds minimisation principles (>2 000 chars)")
        elif data_size > 1000:
            warnings.append("Large data payload — consider applying data minimisation")

        # Explicit consent field validation
        consent_keys = [k for k in data if 'consent' in k.lower()]
        for key in consent_keys:
            if not data.get(key):
                violations.append(f"Missing or falsy consent value in field '{key}'")

        return {
            'is_compliant': len(violations) == 0,
            'violations': _dedup(violations),
            'warnings': _dedup(warnings),
            'rule_applied': 'GDPR',
        }

    def _check_data_retention(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check whether any timestamp fields exceed the configured retention period."""
        violations: List[str] = []
        warnings: List[str] = []
        retention_period_days = 30

        _time_keywords = ('date', 'timestamp', 'time', 'created', 'last')

        for key, value in data.items():
            if not isinstance(value, str):
                continue
            if not any(kw in key.lower() for kw in _time_keywords):
                continue

            try:
                date_str = value.replace('Z', '+00:00').split('.')[0]
                data_date = datetime.fromisoformat(date_str)
                # Make both naive for comparison
                if data_date.tzinfo is not None:
                    data_date = data_date.replace(tzinfo=None)
                days_diff = (datetime.now() - data_date).days

                if days_diff > retention_period_days:
                    violations.append(
                        f"Field '{key}' exceeds retention period ({days_diff} days old)"
                    )
                elif days_diff > retention_period_days * 0.7:
                    warnings.append(
                        f"Field '{key}' approaching retention limit ({days_diff} days old)"
                    )
            except (ValueError, TypeError):
                continue

        return {
            'is_compliant': len(violations) == 0,
            'violations': _dedup(violations),
            'warnings': _dedup(warnings),
            'rule_applied': 'DATA_RETENTION',
        }

    def validate_compliance(self, data: Dict[str, Any], regulations: List[str] = None) -> Dict[str, Any]:
        """Run all requested regulation checks and return a consolidated result."""
        if regulations is None:
            regulations = ['hipaa', 'gdpr']

        results: Dict[str, Any] = {}
        overall_compliant = True
        all_violations: List[str] = []
        all_warnings: List[str] = []

        for regulation in regulations:
            checker = self.compliance_rules.get(regulation)
            if checker is None:
                logger.warning("Unknown regulation '%s' requested — skipping.", regulation)
                continue

            result = checker(data)
            results[regulation] = result

            if not result['is_compliant']:
                overall_compliant = False

            all_violations.extend(result['violations'])
            all_warnings.extend(result['warnings'])

        # Store compliance record; cap log to avoid unbounded memory growth
        record = {
            'timestamp': datetime.now().isoformat(),
            'data_sample': {k: str(v)[:100] for k, v in list(data.items())[:3]},
            'results': results,
            'overall_compliant': overall_compliant,
            'total_violations': len(all_violations),
            'total_warnings': len(all_warnings),
        }
        self.compliance_log.append(record)
        if len(self.compliance_log) > _MAX_LOG_SIZE:
            self.compliance_log = self.compliance_log[-_MAX_LOG_SIZE:]

        return {
            'overall_compliant': overall_compliant,
            'regulation_results': results,
            'compliance_id': f"COMP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'summary': {
                'total_violations': len(all_violations),
                'total_warnings': len(all_warnings),
                'violations': _dedup(all_violations)[:5],
                'warnings': _dedup(all_warnings)[:5],
            },
        }

    def get_compliance_stats(self) -> Dict[str, Any]:
        """Return aggregate compliance statistics from the in-memory log."""
        if not self.compliance_log:
            return {"total_checks": 0, "compliance_rate": 1.0}

        total_checks = len(self.compliance_log)
        compliant_checks = sum(1 for r in self.compliance_log if r['overall_compliant'])

        return {
            "total_checks": total_checks,
            "compliance_rate": compliant_checks / total_checks,
            "recent_checks": self.compliance_log[-5:],
            "most_common_violation": self._get_most_common_violation(),
        }

    def _get_most_common_violation(self) -> str:
        """Return the most frequently occurring violation keyword across all log entries."""
        all_violations: List[str] = []
        for record in self.compliance_log:
            for reg_result in record['results'].values():
                all_violations.extend(reg_result.get('violations', []))

        if not all_violations:
            return "none"

        # Use the first word of each violation as a simple category key
        counter = Counter(v.split()[0] for v in all_violations)
        return counter.most_common(1)[0][0]

def _dedup(items: List[str]) -> List[str]:
    """Deduplicate a list while preserving insertion order."""
    return list(dict.fromkeys(items))