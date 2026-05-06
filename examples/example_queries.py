# examples/example_queries.py
"""
Enhanced Example Queries for Compliance-Aware Multi-Agent System

This file demonstrates three comprehensive end-to-end queries showing:
1. Retrieval from real API
2. Multi-step reasoning with chain-of-thought
3. Comprehensive compliance checks
4. Memory system learning
"""

import json
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import EnhancedComplianceAwareAgentSystem

def demonstrate_example_queries():
    """Demonstrate the system with three comprehensive example queries"""
    system = EnhancedComplianceAwareAgentSystem("example_queries.db")
    
    examples = [
        {
            "name": "Weather Analysis with Clean Data",
            "query": "What are the current weather conditions in Tokyo and potential impacts on outdoor activities?",
            "description": "Demonstrates successful retrieval, reasoning, and compliance with clean data",
            "regulations": ["hipaa", "gdpr"]
        },
        {
            "name": "Sensitive Healthcare Data Scenario", 
            "query": "Analyze patient vital signs data from hospital monitoring system for diabetes patients",
            "description": "Shows compliance violations when handling potentially sensitive healthcare data",
            "regulations": ["hipaa", "gdpr", "data_retention"]
        },
        {
            "name": "Business Intelligence with Customer Data",
            "query": "Provide insights on customer behavior patterns and sales correlations from our European user base",
            "description": "Demonstrates complex reasoning with business data and GDPR considerations",
            "regulations": ["gdpr", "data_retention"]
        }
    ]
    
    print("ENHANCED EXAMPLE QUERIES - END TO END DEMONSTRATION")
    print("=" * 70)
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'='*70}")
        print(f"EXAMPLE {i}: {example['name']}")
        print(f"{'='*70}")
        print(f"📝 Query: {example['query']}")
        print(f"📋 Description: {example['description']}")
        print(f"🛡️  Regulations: {', '.join(example['regulations'])}")
        print(f"\n🔄 Processing...")
        
        result = system.process_query(example['query'], example['regulations'])
        
        # Display comprehensive results
        display_enhanced_results(result, example)
        
        print(f"\n{'─'*70}")

def display_enhanced_results(result, example):
    """Display enhanced results in a structured format"""
    
    if not result['success']:
        print("❌ QUERY FAILED")
        print(f"Error: {result.get('error', 'Unknown error')}")
        return
    
    print("✅ QUERY SUCCESSFUL")
    
    # Retrieval Phase
    print(f"\n📊 RETRIEVAL PHASE")
    print(f"  ✅ Retrieved {len(result['retrieved_data'])} data fields")
    if result['retrieved_data']:
        sample_data = dict(list(result['retrieved_data'].items())[:4])
        print(f"  📋 Sample data: {json.dumps(sample_data, indent=2)}")
    
    # Reasoning Phase
    print(f"\n🤔 REASONING PHASE")
    insights = result['insights']
    print(f"  🔗 Reasoning Steps: {len(insights['reasoning_chain'])}")
    print(f"  💡 Generated Hypotheses: {len(insights['generated_hypotheses'])}")
    print(f"  🎯 Confidence Score: {insights['structured_insights']['confidence_score']:.2f}")
    
    # Show reasoning chain
    print(f"  🔄 Reasoning Chain Preview:")
    for step in insights['reasoning_chain'][:2]:  # First 2 steps
        print(f"     Step {step['step']}: {step['type']}")
        print(f"        {step['description']}")
    
    # Show key insights
    structured = insights['structured_insights']
    print(f"  📝 Key Response: {structured['query_response']}")
    
    if structured['key_findings']:
        print(f"  🔍 Key Findings:")
        for finding in structured['key_findings']:
            print(f"     • {finding}")
    
    # Compliance Phase
    print(f"\n🛡️ COMPLIANCE PHASE")
    compliance = result['compliance_check']
    status = "✅ COMPLIANT" if compliance['overall_compliant'] else "❌ NON-COMPLIANT"
    print(f"  📋 Overall Status: {status}")
    print(f"  🆔 Compliance ID: {compliance['compliance_id']}")
    
    for regulation, check in compliance['regulation_results'].items():
        status_icon = "✅" if check['is_compliant'] else "❌"
        violation_count = len(check['violations'])
        warning_count = len(check['warnings'])
        
        print(f"  📜 {regulation.upper()}: {status_icon} ({violation_count} violations, {warning_count} warnings)")
        
        if violation_count > 0:
            print(f"     Violations:")
            for violation in check['violations'][:2]:  # Show first 2
                print(f"       - {violation}")
        
        if warning_count > 0:
            print(f"     Warnings:")
            for warning in check['warnings'][:2]:  # Show first 2
                print(f"       ! {warning}")
    
    # Performance Metrics
    print(f"\n⚡ PERFORMANCE METRICS")
    metrics = result['performance_metrics']
    print(f"  ⏱️ Total Time: {metrics['total_processing_time']:.2f}s")
    print(f"  📈 Historical Success Rate: {metrics['historical_success_rate']:.2f}")
    print(f"  🎯 Efficiency Score: {metrics['efficiency_score']:.2f}")
    print(f"  🔧 Component Times:")
    for component, time in metrics['component_times'].items():
        print(f"     {component}: {time:.2f}s")
    
    # System Recommendations
    if result['system_recommendations']:
        print(f"\n💡 SYSTEM RECOMMENDATIONS")
        for i, recommendation in enumerate(result['system_recommendations'][:3], 1):
            print(f"  {i}. {recommendation}")

def run_system_analytics_demo():
    """Demonstrate system learning and analytics over multiple queries"""
    print("\n" + "="*70)
    print("SYSTEM LEARNING AND ANALYTICS DEMONSTRATION")
    print("="*70)
    
    system = EnhancedComplianceAwareAgentSystem("analytics_demo.db")
    
    # Run multiple queries to build up system memory
    test_queries = [
        "Weather in London with temperature and humidity",
        "Temperature and pressure in Tokyo for aviation", 
        "Patient health monitoring data with vital signs",
        "User activity patterns and behavior analysis",
        "Sales data correlation with weather conditions",
        "Medical diagnosis data for research purposes",
        "Customer personal information for marketing",
        "Business intelligence from European user data"
    ]
    
    print("Running multiple queries to build system memory...")
    for i, query in enumerate(test_queries, 1):
        print(f"  Query {i}: {query}")
        system.process_query(query)
        # Small delay to simulate real usage
        import time
        time.sleep(0.1)
    
    # Show comprehensive system analytics
    print("\n📈 COMPREHENSIVE SYSTEM ANALYTICS")
    analytics = system.get_system_analytics()
    
    print(f"\n🏥 System Health Overview:")
    health = analytics['system_health']
    print(f"  Overall Score: {health['score']}/100")
    print(f"  Status: {health['status'].upper()}")
    print(f"  Success Rate: {health['success_rate']}%")
    print(f"  Compliance Rate: {health['compliance_rate']}%")
    
    print(f"\n📊 Memory System Insights:")
    memory = analytics['memory_system']
    print(f"  Total Queries: {memory['total_queries_processed']}")
    print(f"  Average Success: {memory['average_success_rate']:.2%}")
    print(f"  System Health: {memory['system_health']}")
    print(f"  Performance Trend: {memory['performance_trend']}")
    
    print(f"\n🛡️ Compliance Statistics:")
    compliance = analytics['compliance_agent']
    print(f"  Total Checks: {compliance['total_checks']}")
    print(f"  Compliance Rate: {compliance['compliance_rate']:.2%}")
    print(f"  Most Common Issue: {compliance['most_common_violation']}")
    
    print(f"\n🔧 Agent Performance Summary:")
    agents = analytics['memory_system']['agent_performance']
    for agent, performance in agents.items():
        success_rate = performance['success_rate']
        avg_time = performance['avg_response_time']
        rating = "⭐ Excellent" if success_rate > 0.8 else "✅ Good" if success_rate > 0.6 else "⚠️ Needs Attention"
        print(f"  {agent}: {success_rate:.2%} success, {avg_time:.2f}s avg time - {rating}")
    
    print(f"\n🚨 Common Compliance Issues:")
    issues = analytics['memory_system']['common_compliance_issues']
    if issues:
        for issue in issues[:5]:
            print(f"  {issue['type']}: {issue['count']} occurrences ({issue['severity']} severity)")
    else:
        print("  No major compliance issues detected ✅")
    
    print(f"\n💡 Top Recommendations:")
    recommendations = analytics['recommendations']
    if recommendations:
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"  {i}. {rec}")
    else:
        print("  System operating optimally - no recommendations at this time ✅")

def performance_benchmark():
    """Run performance benchmarking"""
    print("\n" + "="*70)
    print("PERFORMANCE BENCHMARKING")
    print("="*70)
    
    system = EnhancedComplianceAwareAgentSystem("benchmark.db")
    
    # Test queries for benchmarking
    benchmark_queries = [
        "Simple weather query for London",
        "Complex medical data analysis",
        "Business intelligence with customer data",
        "Mixed data type analysis"
    ]
    
    import time
    times = []
    
    for query in benchmark_queries:
        start_time = time.time()
        result = system.process_query(query)
        end_time = time.time()
        
        processing_time = end_time - start_time
        times.append(processing_time)
        
        status = "✅" if result['success'] else "❌"
        print(f"  {status} {query}: {processing_time:.2f}s")
    
    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)
    
    print(f"\n📊 Benchmark Results:")
    print(f"  Average Time: {avg_time:.2f}s")
    print(f"  Minimum Time: {min_time:.2f}s") 
    print(f"  Maximum Time: {max_time:.2f}s")
    print(f"  Total Queries: {len(benchmark_queries)}")
    
    # Performance rating
    if avg_time < 1.0:
        rating = "⭐ Excellent"
    elif avg_time < 2.0:
        rating = "✅ Good"
    elif avg_time < 3.0:
        rating = "⚠️ Acceptable"
    else:
        rating = "🐌 Slow"
    
    print(f"  Performance Rating: {rating}")

if __name__ == "__main__":
    # Run the main example queries demonstration
    demonstrate_example_queries()
    
    # Run system analytics demonstration
    run_system_analytics_demo()
    
    # Run performance benchmarking
    performance_benchmark()
    
    print("\n" + "="*70)
    print("🎉 ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
    print("="*70)