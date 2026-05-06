# tests/test_integration.py
import unittest
import tempfile
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import EnhancedComplianceAwareAgentSystem

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.system = EnhancedComplianceAwareAgentSystem(self.temp_db.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_complete_workflow_clean_data(self):
        """Test complete workflow with clean, compliant data"""
        query = "What's the weather in Berlin with temperature and humidity?"
        
        result = self.system.process_query(query)
        
        # Verify successful processing
        self.assertTrue(result['success'])
        
        # Verify all components executed
        self.assertIn('retrieved_data', result)
        self.assertIn('insights', result)
        self.assertIn('compliance_check', result)
        
        # Verify compliance for clean data
        self.assertTrue(result['compliance_check']['overall_compliant'])
    
    def test_batch_processing(self):
        """Test batch processing of multiple queries"""
        queries = [
            "Weather in London",
            "Temperature in Paris", 
            "Humidity in Tokyo"
        ]
        
        batch_result = self.system.batch_process_queries(queries)
        
        self.assertEqual(batch_result['total_queries'], 3)
        self.assertEqual(batch_result['successful_queries'], 3)
        self.assertEqual(batch_result['success_rate'], 1.0)

if __name__ == '__main__':
    unittest.main(verbosity=2)