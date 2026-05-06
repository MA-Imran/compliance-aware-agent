import logging
from collections import Counter
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class EnhancedReasoningAgent:
    def __init__(self):
        self.reasoning_steps: List[Dict[str, Any]] = []
        self.hypotheses: List[str] = []

    def analyze_with_chain_of_thought(self, data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Perform multi-step reasoning with a chain-of-thought approach."""
        self.reasoning_steps = []
        self.hypotheses = []

        logger.debug("Starting chain-of-thought analysis for query: %r", query)

        # Step 1: Data Understanding
        self._add_reasoning_step("DATA_UNDERSTANDING", "Analysing data structure and content")
        data_insights = self._understand_data_structure(data)

        # Step 2: Hypothesis Generation
        self._add_reasoning_step("HYPOTHESIS_GENERATION", "Generating potential insights from data patterns")
        hypotheses = self._generate_hypotheses(data, query)

        # Step 3: Pattern Recognition
        self._add_reasoning_step("PATTERN_RECOGNITION", "Identifying patterns and correlations in the data")
        patterns = self._identify_patterns(data)

        # Step 4: Context Analysis
        self._add_reasoning_step("CONTEXT_ANALYSIS", "Analysing data in the context of the query")
        context_analysis = self._analyze_context(data, query)

        # Step 5: Insight Synthesis
        self._add_reasoning_step("INSIGHT_SYNTHESIS", "Synthesising final insights from all analysis steps")
        final_insights = self._synthesize_insights(data_insights, hypotheses, patterns, context_analysis, query)

        logger.debug(
            "Chain-of-thought complete — %d steps, %d hypotheses, confidence=%.2f",
            len(self.reasoning_steps),
            len(hypotheses),
            final_insights.get('confidence_score', 0.0),
        )

        return {
            'structured_insights': final_insights,
            'reasoning_chain': self.reasoning_steps,
            'generated_hypotheses': hypotheses,
            'identified_patterns': patterns,
            'context_analysis': context_analysis,
            'timestamp': datetime.now().isoformat(),
        }

    # ------------------------------------------------------------------
    # Reasoning chain helpers
    # ------------------------------------------------------------------

    def _add_reasoning_step(self, step_type: str, description: str):
        """Append a timestamped step to the reasoning chain."""
        self.reasoning_steps.append({
            'step': len(self.reasoning_steps) + 1,
            'type': step_type,
            'description': description,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
        })

    # ------------------------------------------------------------------
    # Step implementations
    # ------------------------------------------------------------------

    def _understand_data_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse the structure and completeness of the incoming data."""
        numeric_count = 0
        string_count = 0
        null_count = 0
        field_types: Dict[str, str] = {}

        for key, value in data.items():
            field_types[key] = type(value).__name__
            if isinstance(value, (int, float)):
                numeric_count += 1
            elif isinstance(value, str):
                string_count += 1
            elif value is None:
                null_count += 1

        field_count = len(data)
        completeness_score = 1.0 - (null_count / field_count) if field_count else 1.0

        return {
            'data_type': type(data).__name__,
            'field_count': field_count,
            'fields': list(data.keys()),
            'field_types': field_types,
            'data_quality': {
                'numeric_fields': numeric_count,
                'text_fields': string_count,
                'null_fields': null_count,
                'completeness_score': completeness_score,
            },
        }

    def _generate_hypotheses(self, data: Dict[str, Any], query: str) -> List[str]:
        """Generate plausible hypotheses based on the data content and query intent."""
        hypotheses: List[str] = []
        query_lower = query.lower()

        # Weather-specific hypotheses
        if any(t in query_lower for t in ('weather', 'temperature', 'forecast')):
            temp = data.get('temperature')
            if isinstance(temp, (int, float)):
                if temp > 30:
                    hypotheses.append("High temperature conditions detected — potential heat-wave impact")
                elif temp < 0:
                    hypotheses.append("Freezing temperatures — risk of ice and winter conditions")
                elif 20 <= temp <= 26:
                    hypotheses.append("Comfortable temperature range — ideal for outdoor activities")

            humidity = data.get('humidity')
            if isinstance(humidity, (int, float)):
                if humidity > 80:
                    hypotheses.append("High humidity may affect comfort and equipment")
                elif humidity < 30:
                    hypotheses.append("Low humidity conditions — potential dehydration risk")

            condition = data.get('weather_condition', '')
            if 'rain' in condition.lower():
                hypotheses.append("Precipitation expected — consider indoor alternatives")
            elif 'snow' in condition.lower():
                hypotheses.append("Snow conditions — transportation and safety considerations apply")

        # Medical / health hypotheses
        if any(t in query_lower for t in ('patient', 'medical', 'health')):
            if 'blood_pressure' in data:
                hypotheses.append("Blood pressure data available for health monitoring")
            if 'heart_rate' in data:
                hypotheses.append("Heart rate monitoring provides vital health insights")

        # Business / sales hypotheses
        if any(t in query_lower for t in ('sales', 'business', 'customer')):
            if 'sales_volume' in data:
                hypotheses.append("Sales volume trends can inform business strategy")
            if 'customer_count' in data:
                hypotheses.append("Customer behaviour patterns may reveal growth opportunities")

        # Data-quality hypotheses
        if any(v is None for v in data.values()):
            hypotheses.append("Data completeness issues detected — may affect analysis accuracy")
        if len(data) < 3:
            hypotheses.append("Limited data fields available — consider enriching from additional sources")

        return hypotheses

    def _identify_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify numeric ranges, categorical values, correlations, and anomalies."""
        patterns: Dict[str, Any] = {
            'numeric_ranges': {},
            'categorical_values': {},
            'correlations': [],
            'anomalies': [],
            'trends': [],
        }

        numeric_fields: Dict[str, float] = {}

        for key, value in data.items():
            if isinstance(value, (int, float)):
                numeric_fields[key] = value
                patterns['numeric_ranges'][key] = {'value': value, 'type': 'numeric'}

                # Anomaly detection
                if key == 'temperature' and (value > 50 or value < -50):
                    patterns['anomalies'].append(f"Extreme temperature value detected: {value}")
                elif key == 'humidity' and not (0 <= value <= 100):
                    patterns['anomalies'].append(f"Invalid humidity value detected: {value}")

            elif isinstance(value, str):
                patterns['categorical_values'].setdefault(key, [])
                if value not in patterns['categorical_values'][key]:
                    patterns['categorical_values'][key].append(value)

        # Simple pairwise correlation hint when multiple numeric fields exist
        if len(numeric_fields) >= 2:
            field_names = list(numeric_fields.keys())[:3]
            patterns['correlations'].append(
                f"Potential relationship between '{field_names[0]}' and '{field_names[1]}'"
            )

        if 'timestamp' in data:
            patterns['trends'].append("Temporal data available — trend analysis is possible")

        return patterns

    def _analyze_context(self, data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Evaluate data relevance and derive actionable insights from the query context."""
        context: Dict[str, Any] = {
            'query_intent': self._infer_query_intent(query),
            'data_relevance': self._assess_data_relevance(data, query),
            'actionable_insights': [],
            'limitations': [],
        }

        if 'weather' in query.lower():
            temp = data.get('temperature')
            if isinstance(temp, (int, float)):
                if temp < 10:
                    context['actionable_insights'].append("Recommend warm clothing")
                elif temp > 25:
                    context['actionable_insights'].append("Recommend light clothing and adequate hydration")

        if len(data) < 5:
            context['limitations'].append("Limited data fields may restrict comprehensive analysis")
        if any(v is None for v in data.values()):
            context['limitations'].append("Missing values present in dataset")

        return context

    def _infer_query_intent(self, query: str) -> str:
        """Classify the high-level intent of the query string."""
        query_lower = query.lower()
        if any(t in query_lower for t in ('weather', 'temperature', 'forecast')):
            return "weather_inquiry"
        if any(t in query_lower for t in ('patient', 'medical', 'health')):
            return "health_analysis"
        if any(t in query_lower for t in ('sales', 'business', 'customer')):
            return "business_intelligence"
        if any(t in query_lower for t in ('analyse', 'analyze', 'insight', 'pattern')):
            return "data_analysis"
        return "general_inquiry"

    def _assess_data_relevance(self, data: Dict[str, Any], query: str) -> float:
        """Score how relevant the retrieved data is to the original query (0–1)."""
        relevance_score = 0.5  # Baseline

        query_terms = set(query.lower().split())
        data_text = str(data).lower()

        # Term-overlap boost (capped at 0.3)
        matching = sum(1 for term in query_terms if term in data_text)
        relevance_score += min(matching * 0.1, 0.3)

        # Domain-specific boost
        if 'weather' in query.lower() and any(f in data for f in ('temperature', 'humidity')):
            relevance_score += 0.2

        return min(relevance_score, 1.0)

    # ------------------------------------------------------------------
    # Synthesis
    # ------------------------------------------------------------------

    def _synthesize_insights(self, data_insights: Dict, hypotheses: List[str],
                             patterns: Dict, context: Dict, query: str) -> Dict[str, Any]:
        """Combine outputs from all reasoning steps into a final structured insight."""
        return {
            'query_response': self._generate_query_response(data_insights, hypotheses, patterns, context, query),
            'data_quality_assessment': self._assess_data_quality(data_insights),
            'recommendations': self._generate_recommendations(hypotheses, patterns, context),
            'confidence_score': self._calculate_confidence(data_insights, hypotheses, context),
            'key_findings': self._extract_key_findings(hypotheses, patterns),
        }

    def _generate_query_response(self, data_insights: Dict, hypotheses: List[str],
                                 patterns: Dict, context: Dict, query: str) -> str:
        """Compose a concise natural-language response to the original query."""
        response = f"Based on analysis of {data_insights['field_count']} data fields, "

        if hypotheses:
            response += f"the primary insight is: {hypotheses[0]}. "
        else:
            response += "the data appears consistent with expected patterns. "

        if context['actionable_insights']:
            response += f"Recommendation: {context['actionable_insights'][0]}. "

        if data_insights['data_quality']['completeness_score'] < 0.8:
            response += "Note: data quality considerations were identified. "

        return response.strip()

    def _assess_data_quality(self, data_insights: Dict) -> Dict[str, Any]:
        """Return a human-readable data quality assessment."""
        completeness = data_insights['data_quality']['completeness_score']

        if completeness > 0.9:
            quality_level = "excellent"
        elif completeness > 0.7:
            quality_level = "good"
        elif completeness > 0.5:
            quality_level = "fair"
        else:
            quality_level = "poor"

        return {
            'completeness': quality_level,
            'field_variety': 'good' if data_insights['field_count'] > 3 else 'limited',
            'assessment': f"Data quality is {quality_level} with {completeness:.1%} completeness",
            'numeric_fields': data_insights['data_quality']['numeric_fields'],
            'text_fields': data_insights['data_quality']['text_fields'],
        }

    def _generate_recommendations(self, hypotheses: List[str], patterns: Dict, context: Dict) -> List[str]:
        """Generate a deduplicated, capped list of actionable recommendations."""
        recommendations: List[str] = []

        recommendations.extend(context['actionable_insights'])

        if hypotheses:
            recommendations.append("Validate generated hypotheses against additional data sources")

        if patterns.get('correlations'):
            recommendations.append("Deeper analysis recommended for identified correlations")

        if patterns.get('anomalies'):
            recommendations.append("Review detected anomalies for potential data quality issues")

        recommendations.append("Schedule regular data quality validation")

        # Deduplicate and cap
        return list(dict.fromkeys(recommendations))[:5]

    def _extract_key_findings(self, hypotheses: List[str], patterns: Dict) -> List[str]:
        """Summarise the top findings from hypotheses and pattern analysis."""
        findings: List[str] = []

        findings.extend(hypotheses[:2])

        if patterns.get('anomalies'):
            findings.append("Data anomalies detected — manual review required")

        if patterns.get('correlations'):
            findings.append("Potential correlations identified in the data")

        return findings[:3]

    def _calculate_confidence(self, data_insights: Dict, hypotheses: List[str], context: Dict) -> float:
        """
        Calculate a bounded confidence score (0.1 – 1.0) for the analysis.

        Factors:
        - Base: 0.5
        - Data richness: +0.2 if more than 3 fields
        - Hypotheses generated: +0.2 if any
        - Data relevance: scaled contribution capped internally
        - Data quality: scaled contribution
        """
        confidence = 0.5

        if data_insights['field_count'] > 3:
            confidence += 0.2

        if hypotheses:
            confidence += 0.1  # Reduced from 0.2 to keep ceiling tighter

        # Relevance contribution: max ±0.15
        relevance_delta = (context['data_relevance'] - 0.5) * 0.3
        confidence += max(-0.15, min(relevance_delta, 0.15))

        # Quality contribution: max ±0.15
        quality_score = data_insights['data_quality']['completeness_score']
        quality_delta = (quality_score - 0.5) * 0.3
        confidence += max(-0.15, min(quality_delta, 0.15))

        return round(min(max(confidence, 0.1), 1.0), 3)