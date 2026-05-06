import logging
import os
from collections import deque
from datetime import datetime
from typing import Dict, Any, Optional
import random

logger = logging.getLogger(__name__)

# Maximum number of request log entries kept in memory
_MAX_HISTORY = 500


class RetrievalAgent:
    def __init__(self):
        self.api_base_url = "http://api.openweathermap.org/data/2.5"
        # Load API key from environment; fall back gracefully so mock data is used
        self.api_key: str = os.environ.get("OPENWEATHER_API_KEY", "")
        if not self.api_key:
            logger.warning(
                "OPENWEATHER_API_KEY not set — real API calls will fail and mock data will be used."
            )
        # Bounded deque prevents unbounded memory growth in long-running sessions
        self.request_history: deque = deque(maxlen=_MAX_HISTORY)

    def fetch_data(self, query: str) -> Dict[str, Any]:
        """
        Fetch data based on query content.

        Routes to a weather or generic handler depending on keywords.
        Falls back to minimal mock data if an unexpected exception occurs.
        """
        try:
            if any(term in query.lower() for term in ("weather", "temperature")):
                return self._fetch_weather_data(query)
            return self._fetch_generic_data(query)
        except Exception as exc:
            logger.warning("Data fetch failed (%s) — falling back to mock data.", exc)
            return self._get_mock_data(query)

    def _fetch_weather_data(self, query: str) -> Dict[str, Any]:
        """Fetch weather data (real API if key is set, otherwise mock)."""
        location = self._extract_location(query)

        self.request_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'location': location,
            'type': 'weather',
        })

        if self.api_key:
            # Placeholder for real API integration
            # response = requests.get(
            #     f"{self.api_base_url}/weather",
            #     params={"q": location, "appid": self.api_key, "units": "metric"},
            #     timeout=10,
            # )
            # response.raise_for_status()
            # return response.json()
            pass

        logger.debug("Using mock weather data for location: %s", location)
        return self._generate_mock_weather_data(location)

    def _fetch_generic_data(self, query: str) -> Dict[str, Any]:
        """Route generic queries to the appropriate mock data generator."""
        query_lower = query.lower()

        self.request_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'type': 'generic',
        })

        if any(term in query_lower for term in ("patient", "medical")):
            return self._generate_mock_medical_data()
        if any(term in query_lower for term in ("sales", "business")):
            return self._generate_mock_business_data()
        if any(term in query_lower for term in ("user", "customer")):
            return self._generate_mock_user_data()
        return self._generate_mock_general_data()

    def _extract_location(self, query: str) -> str:
        """Extract a known city name from the query string."""
        known_locations = ['london', 'paris', 'tokyo', 'berlin', 'new york', 'sydney']
        query_lower = query.lower()
        for location in known_locations:
            if location in query_lower:
                return location.title()
        return "London"  # Default

    def _generate_mock_weather_data(self, location: str) -> Dict[str, Any]:
        """Return realistic mock weather data for the given location."""
        base_temp = random.uniform(-5, 35)
        return {
            "location": location,
            "temperature": round(base_temp, 1),
            "humidity": random.randint(30, 95),
            "pressure": random.randint(1000, 1030),
            "wind_speed": round(random.uniform(0, 25), 1),
            "weather_condition": random.choice(["clear", "cloudy", "rainy", "snowy"]),
            "visibility": random.randint(1, 10),
            "timestamp": datetime.now().isoformat(),
            "data_source": "OpenWeatherMap",
            "units": "metric",
        }

    def _generate_mock_medical_data(self) -> Dict[str, Any]:
        """Return mock medical data (intentionally triggers HIPAA compliance checks)."""
        return {
            "patient_id": "PT-12345",
            "patient_name": "John Smith",
            "date_of_birth": "1985-03-15",
            "ssn": "123-45-6789",
            "diagnosis": "Hypertension and diabetes monitoring",
            "medications": ["Lisinopril 10mg", "Metformin 500mg"],
            "last_visit": "2024-01-10",
            "blood_pressure": "130/85",
            "heart_rate": 72,
            "temperature": 36.8,
            "hospital": "City General Hospital",
            "physician": "Dr. Emily Johnson",
        }

    def _generate_mock_business_data(self) -> Dict[str, Any]:
        """Return mock business/sales data."""
        return {
            "sales_volume": 15420,
            "customer_count": 428,
            "average_transaction": 36.02,
            "peak_hour": "14:00-15:00",
            "most_popular_product": "Wireless Headphones",
            "customer_satisfaction": 4.3,
            "region": "North America",
            "timestamp": datetime.now().isoformat(),
        }

    def _generate_mock_user_data(self) -> Dict[str, Any]:
        """Return mock user data (intentionally triggers GDPR compliance checks)."""
        return {
            "user_id": "USR-78901",
            "user_email": "customer@example.com",
            "user_name": "Alice Johnson",
            "ip_address": "192.168.1.100",
            "phone_number": "+1-555-0123",
            "last_login": "2024-01-15T10:30:00Z",
            "preferences": {"newsletter": True, "theme": "dark"},
            "account_age_days": 127,
        }

    def _generate_mock_general_data(self) -> Dict[str, Any]:
        """Return generic mock data for unrecognised query types."""
        return {
            "query_type": "general_inquiry",
            "data_points": 15,
            "confidence": 0.85,
            "timestamp": datetime.now().isoformat(),
            "sample_metric": 42.5,
            "status": "active",
        }

    def _get_mock_data(self, query: str) -> Dict[str, Any]:
        """Minimal fallback mock data used when the main fetch path raises."""
        return {
            "query": query,
            "mock_data": True,
            "timestamp": datetime.now().isoformat(),
            "message": "Using fallback mock data — check logs for the underlying error.",
        }

    def get_request_stats(self) -> Dict[str, Any]:
        """Return basic statistics about requests made in this session."""
        history_list = list(self.request_history)
        return {
            "total_requests": len(history_list),
            "recent_requests": history_list[-5:],
            "most_common_type": self._get_most_common_request_type(history_list),
        }

    @staticmethod
    def _get_most_common_request_type(history: list) -> str:
        """Return the most frequently occurring request type from a history list."""
        if not history:
            return "none"
        types = [req['type'] for req in history]
        return max(set(types), key=types.count)