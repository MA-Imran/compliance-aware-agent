# examples/enhanced_demo.py
import json
import time
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import EnhancedComplianceAwareAgentSystem
from enhanced_compliance_agent import EnhancedComplianceAgent
from enhanced_reasoning_agent import EnhancedReasoningAgent
from memory_system import EnhancedMemorySystem

def demo_enhanced_compliance_checks():
    """Demonstrate enhanced compliance checking capabilities"""
    print("=== ENHANCED COMPLIANCE CHECKS DEMO ===")
    
    compliance_agent = EnhancedComplianceAgent()
    
    # Example 1: Clean weather data
    print("\n1. ✅ Clean Weather Data:")
    clean_data = {
        "temperature": 25.5,
        "humidity": 65,
        "pressure": 1013,
        "location": "Berlin",
        "timestamp": datetime.now().isoformat()
    }
    
    result = compliance_agent.validate_compliance(clean_data, ['hipaa', 'gdpr'])
    print(f"   Overall Compliant: {result['overall_compliant']}")
    for regulation, check_result in result['regulation_results'].items():
        print(f"   {regulation.upper()}: {len(check_result['violations'])} violations")
    
    # Example 2: Data with potential PHI
    print("\n2. ⚠️  Data with Potential PHI:")
    phi_data = {
        "patient_temperature": 38.2,
        "diagnosis_notes": "Patient shows symptoms of diabetes",
        "contact_ssn": "123-45-6789",
        "hospital_name": "City General Hospital",
        "visit_date": "2024-01-15"
    }
    
    result = compliance_agent.validate_compliance(phi_data, ['hipaa', 'gdpr'])
    print(f"   Overall Compliant: {result['overall_compliant']}")
    for regulation, check_result in result['regulation_results'].items():
        print(f"   {regulation.upper()}:")
        for violation in check_result['violations'][:2]:  # Show first 2
            print(f"     - {violation}")
        for warning in check_result['warnings'][:2]:  # Show first 2
            print(f"     ! {warning}")
    
    # Example 3: Data with personal information
    print("\n3. 🔒 Data with Personal Information:")
    personal_data = {
        "user_email": "john.doe@company.com",
        "user_ip": "192.168.1.100",
        "phone_number": "+49-123-456789",
        "weather_preference": "sunny"
    }
    
    result = compliance_agent.validate_compliance(personal_data, ['gdpr'])
    print(f"   GDPR Compliant: {result['overall_compliant']}")
    for violation in result['regulation_results']['gdpr']['violations']:
        print(f"   - {violation}")
    
    return compliance_agent

def demo_enhanced_reasoning():
    """Demonstrate enhanced reasoning capabilities"""
    print("\n=== ENHANCED REASONING DEMO ===")
    
    reasoning_agent = EnhancedReasoningAgent()
    
    # Example 1: Weather analysis with chain of thought
    print("\n1. 🌤️  Weather Analysis with Chain of Thought:")
    weather_data = {
        "temp": -2,
        "humidity": 95,
        "wind_speed": 25,
        "precipitation": 5.2,
        "condition": "snow",
        "visibility": 2,
        "timestamp": "2024-01-15T08:00:00Z"
    }
    
    result = reasoning_agent.analyze_with_chain_of_thought(
        weather_data, 
        "Analyze current winter weather conditions and potential impacts"
    )
    
    print("   Reasoning Chain:")
    for step in result['reasoning_chain'][:3]:  # Show first 3 steps
        print(f"     Step {step['step']}: {step['type']} - {step['description']}")
    
    print("\n   Generated Hypotheses:")
    for i, hypothesis in enumerate(result['generated_hypotheses'][:3], 1):
        print(f"     {i}. {hypothesis}")
    
    print("\n   Structured Insights:")
    insights = result['structured_insights']
    print(f"     Response: {insights['query_response']}")
    print(f"     Confidence: {insights['confidence_score']:.2f}")
    print(f"     Data Quality: {insights['data_quality_assessment']['assessment']}")
    
    # Example 2: Business data analysis
    print("\n2. 📊 Business Data Analysis:")
    business_data = {
        "sales_volume": 15000,
        "customer_count": 450,
        "avg_transaction": 33.33,
        "peak_hour": "14:00",
        "weekday": "Monday"
    }
    
    result = reasoning_agent.analyze_with_chain_of_thought(
        business_data,
        "Analyze sales performance and customer patterns"
    )
    
    print("   Identified Patterns:")
    for pattern in result['identified_patterns']['correlations']:
        print(f"     - {pattern}")

def demo_memory_and_learning():
    """Demonstrate memory system learning capabilities"""
    print("\n=== MEMORY AND LEARNING DEMO ===")
    
    memory_system = EnhancedMemorySystem("demo_memory.db")
    
    # Simulate some system usage
    queries = [
        ("What's the weather in London?", True),
        ("Temperature in Tokyo?", True),
        ("Get patient medical data", False),  # Might fail due to compliance
        ("Humidity levels in Berlin?", True),
        ("Fetch user personal information", False),  # Compliance violation
    ]
    
    print("Simulating query history...")
    for query, success in queries:
        memory_system.log_query(query, success)
        # Add some performance metrics
        memory_system.update_agent_performance("retrieval_agent", "data_fetch", success, 1.5)
        memory_system.update_agent_performance("reasoning_agent", "analysis", success, 2.0)
    
    # Log some compliance violations
    compliance_issues = [
        ("hipaa", "SSN detected in patient records", "high"),
        ("gdpr", "Email collection without proper consent", "medium"),
        ("hipaa", "Medical diagnosis in unencrypted field", "high"),
        ("data_retention", "User data older than 2 years found", "low")
    ]
    
    for violation_type, description, severity in compliance_issues:
        memory_system.log_compliance_violation(violation_type, description, severity)
    
    # Store some system insights
    memory_system.store_system_insight('performance', {'avg_response_time': 1.2, 'success_rate': 0.85}, 0.9)
    memory_system.store_system_insight('compliance', {'common_violation': 'hipaa', 'trend': 'decreasing'}, 0.7)
    
    # Demonstrate learning capabilities
    print("\n📈 System Insights:")
    insights = memory_system.get_system_insights()
    print(f"   Total Queries Processed: {insights['total_queries_processed']}")
    print(f"   Average Success Rate: {insights['average_success_rate']:.2f}")
    print(f"   System Health: {insights['system_health']}")
    print(f"   Performance Trend: {insights['performance_trend']}")
    
    print("\n   Common Compliance Issues:")
    for issue in insights['common_compliance_issues'][:3]:
        print(f"     {issue['type']}: {issue['count']} occurrences ({issue['severity']} severity)")
    
    print("\n   Agent Performance:")
    for agent, performance in insights['agent_performance'].items():
        print(f"     {agent}: {performance['success_rate']:.2f} success rate, {performance['avg_response_time']:.2f}s avg time")
    
    # Demonstrate predictive capabilities
    test_query = "What's the weather in London?"
    success_probability = memory_system.get_query_success_rate(test_query)
    print(f"\n   Historical success probability for similar queries: {success_probability:.2f}")
    
    # Show recent insights
    print("\n   Recent System Insights:")
    recent_insights = memory_system.get_recent_insights(limit=2)
    for insight in recent_insights:
        print(f"     {insight['type']}: {insight['data']} (confidence: {insight['confidence']:.2f})")

def demo_end_to_end_system():
    """Demonstrate complete system operation"""
    print("\n=== END-TO-END SYSTEM DEMO ===")
    
    system = EnhancedComplianceAwareAgentSystem("e2e_demo.db")
    
    # Example queries demonstrating different scenarios
    demo_queries = [
        "What's the current weather in Paris?",
        "Get temperature and humidity data for Berlin",
        "Analyze weather patterns for outdoor event planning",
        "Review patient health monitoring data",
        "Provide customer behavior insights from sales data"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n--- Query {i}: {query} ---")
        
        start_time = time.time()
        result = system.process_query(query)
        processing_time = time.time() - start_time
        
        if result['success']:
            print("✅ Query processed successfully")
            print(f"   Retrieved {len(result['retrieved_data'])} data fields")
            
            # Show reasoning insights
            insights = result['insights']['structured_insights']
            print(f"   Confidence: {insights['confidence_score']:.2f}")
            print(f"   Response: {insights['query_response']}")
            
            # Show compliance results
            compliance = result['compliance_check']
            status = "🟢 COMPLIANT" if compliance['overall_compliant'] else "🔴 NON-COMPLIANT"
            print(f"   Compliance: {status}")
            
            if not compliance['overall_compliant']:
                print(f"   Violations: {compliance['summary']['total_violations']}")
            
            # Show performance metrics
            metrics = result['performance_metrics']
            print(f"   Processing time: {metrics['total_processing_time']:.2f}s")
            print(f"   Efficiency score: {metrics['efficiency_score']:.2f}")
            
            # Show recommendations
            if result['system_recommendations']:
                print(f"   Recommendations: {result['system_recommendations'][0]}")
        else:
            print("❌ Query failed")
            print(f"   Error: {result.get('error', 'Unknown error')}")
    
    # Show system analytics after processing
    print("\n=== SYSTEM ANALYTICS ===")
    analytics = system.get_system_analytics()
    
    print(f"Overall System Health: {analytics['system_health']['status']} ({analytics['system_health']['score']}/100)")
    print(f"Success Rate: {analytics['system_health']['success_rate']}%")
    print(f"Compliance Rate: {analytics['system_health']['compliance_rate']}%")
    
    print("\nTop Recommendations:")
    for i, recommendation in enumerate(analytics['recommendations'][:3], 1):
        print(f"  {i}. {recommendation}")

def run_comprehensive_demo():
    """Run all demonstration scenarios"""
    print("🚀 COMPREHENSIVE ENHANCED MULTI-AGENT SYSTEM DEMO")
    print("=" * 60)
    
    # Run individual demos
    demo_enhanced_compliance_checks()
    demo_enhanced_reasoning()
    demo_memory_and_learning()
    demo_end_to_end_system()
    
    print("\n" + "=" * 60)
    print("🎉 DEMONSTRATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    run_comprehensive_demo()