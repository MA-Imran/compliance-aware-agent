# tests/test_enhanced_system.py
import unittest
import json
import os
import tempfile
from datetime import datetime, timedelta

# Add src to path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_compliance_agent import EnhancedComplianceAgent
from enhanced_reasoning_agent import EnhancedReasoningAgent
from memory_system import EnhancedMemorySystem
from main import EnhancedComplianceAwareAgentSystem

class TestEnhancedComplianceAgent(unittest.TestCase):
    def setUp(self):
        self.compliance_agent = EnhancedComplianceAgent()
    
    def test_hipaa_compliance_clean_data(self):
        """Test HIPAA compliance with clean data"""
        data = {
            "temperature": 25,
            "humidity": 60,
            "location": "New York",
            "timestamp": "2024-01-15T10:30:00Z"
        }
        
        result = self.compliance_agent.validate_compliance(data, ['hipaa'])
        self.assertTrue(result['overall_compliant'])
        self.assertEqual(len(result['regulation_results']['hipaa']['violations']), 0)
    
    def test_hipaa_compliance_phi_detection(self):
        """Test HIPAA compliance with PHI detection"""
        data = {
            "patient_name": "John Doe",
            "diagnosis": "cancer treatment",
            "ssn": "123-45-6789",
            "hospital": "General Hospital",
            "temperature": 98.6
        }
        
        result = self.compliance_agent.validate_compliance(data, ['hipaa'])
        self.assertFalse(result['overall_compliant'])
        violations = result['regulation_results']['hipaa']['violations']
        self.assertTrue(any("SSN" in violation for violation in violations))
    
    def test_gdpr_compliance_personal_data(self):
        """Test GDPR compliance with personal data"""
        data = {
            "user_email": "john.doe@example.com",
            "user_ip": "192.168.1.1",
            "phone_number": "+1-555-0123",
            "weather_data": "sunny"
        }
        
        result = self.compliance_agent.validate_compliance(data, ['gdpr'])
        self.assertFalse(result['overall_compliant'])
        self.assertTrue(len(result['regulation_results']['gdpr']['violations']) > 0)

class TestEnhancedReasoningAgent(unittest.TestCase):
    def setUp(self):
        self.reasoning_agent = EnhancedReasoningAgent()
    
    def test_chain_of_thought_reasoning(self):
        """Test multi-step reasoning with chain of thought"""
        data = {
            "temp": 35,
            "humidity": 85,
            "pressure": 1013,
            "weather": "cloudy"
        }
        
        query = "What are the weather conditions?"
        
        result = self.reasoning_agent.analyze_with_chain_of_thought(data, query)
        
        # Verify reasoning chain exists
        self.assertIn('reasoning_chain', result)
        self.assertGreater(len(result['reasoning_chain']), 0)
        
        # Verify hypotheses were generated
        self.assertIn('generated_hypotheses', result)
        self.assertIsInstance(result['generated_hypotheses'], list)

class TestEnhancedMemorySystem(unittest.TestCase):
    def setUp(self):
        # Use temporary database for tests
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.memory_system = EnhancedMemorySystem(self.temp_db.name)
    
    def tearDown(self):
        # Clean up temporary database
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_query_logging_and_learning(self):
        """Test query logging and success rate calculation"""
        query = "What's the weather in London?"
        
        # Log successful query multiple times
        for i in range(3):
            self.memory_system.log_query(query, success=True)
        
        # Log one failure
        self.memory_system.log_query(query, success=False)
        
        success_rate = self.memory_system.get_query_success_rate(query)
        self.assertEqual(success_rate, 0.75)  # 3 success / 4 total

class TestEndToEndSystem(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.system = EnhancedComplianceAwareAgentSystem(self.temp_db.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_successful_weather_query(self):
        """Test end-to-end successful weather query"""
        query = "What's the weather like in Paris?"
        
        result = self.system.process_query(query)
        
        self.assertTrue(result['success'])
        self.assertIn('retrieved_data', result)
        self.assertIn('insights', result)
        self.assertIn('compliance_check', result)
        self.assertIn('performance_metrics', result)

if __name__ == '__main__':
    unittest.main(verbosity=2)