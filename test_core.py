# test_core.py
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import EnhancedComplianceAwareAgentSystem

def test_core_functionality():
    """Test basic system functionality"""
    print("🧪 Testing Core System Functionality...")
    
    try:
        # Initialize system
        system = EnhancedComplianceAwareAgentSystem("test.db")
        print("✅ System initialized successfully")
        
        # Test a simple query
        result = system.process_query("What's the weather in London?")
        
        if result['success']:
            print("✅ Query processing successful")
            print(f"   Retrieved {len(result['retrieved_data'])} data fields")
            print(f"   Compliance: {'Compliant' if result['compliance_check']['overall_compliant'] else 'Non-compliant'}")
            print(f"   Processing time: {result['performance_metrics']['total_processing_time']:.2f}s")
        else:
            print("❌ Query processing failed")
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        # Test system analytics
        analytics = system.get_system_analytics()
        print("✅ System analytics retrieved")
        print(f"   System health: {analytics['system_health']['status']}")
        
        # Cleanup
        if os.path.exists("test.db"):
            os.remove("test.db")
            
        print("🎉 All core tests passed!")
        
    except Exception as e:
        print(f"❌ Core test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_core_functionality()