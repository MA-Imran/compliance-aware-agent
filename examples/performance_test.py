# examples/performance_test.py
"""
Performance Testing and Benchmarking Script
"""

import time
import statistics
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import EnhancedComplianceAwareAgentSystem

def run_performance_tests():
    """Run comprehensive performance tests"""
    print("🔧 PERFORMANCE TESTING SUITE")
    print("=" * 60)
    
    # Initialize system with test database
    system = EnhancedComplianceAwareAgentSystem("performance_test.db")
    
    # Test queries covering different scenarios
    test_queries = [
        "Weather in London",
        "Temperature in Paris",
        "Analyze weather patterns for outdoor events",
        "Patient health monitoring analysis",
    ]
    
    print(f"Running performance tests with {len(test_queries)} queries...")
    print()
    
    # Test individual query performance
    individual_results = test_individual_queries(system, test_queries)
    
    # Test batch processing performance
    batch_results = test_batch_processing(system, test_queries)
    
    # Generate performance report
    generate_performance_report(individual_results, batch_results)
    
    # Cleanup
    if os.path.exists("performance_test.db"):
        os.remove("performance_test.db")

def test_individual_queries(system, queries):
    """Test performance of individual queries"""
    print("📊 INDIVIDUAL QUERY PERFORMANCE")
    print("-" * 40)
    
    results = {
        'times': [],
        'success_rates': [],
        'compliance_rates': [],
    }
    
    for i, query in enumerate(queries, 1):
        print(f"  Query {i}: {query[:40]}...")
        
        start_time = time.time()
        result = system.process_query(query)
        end_time = time.time()
        
        processing_time = end_time - start_time
        results['times'].append(processing_time)
        
        if result['success']:
            results['success_rates'].append(1)
            results['compliance_rates'].append(
                1 if result['compliance_check']['overall_compliant'] else 0
            )
            status = "✅"
        else:
            results['success_rates'].append(0)
            results['compliance_rates'].append(0)
            status = "❌"
        
        print(f"    {status} {processing_time:.2f}s")
    
    return results

def test_batch_processing(system, queries):
    """Test batch processing performance"""
    print(f"\n🔄 BATCH PROCESSING PERFORMANCE")
    print("-" * 40)
    
    start_time = time.time()
    batch_result = system.batch_process_queries(queries)
    end_time = time.time()
    
    batch_time = end_time - start_time
    avg_batch_time = batch_time / len(queries) if queries else 0
    
    print(f"  Total Queries: {len(queries)}")
    print(f"  Batch Time: {batch_time:.2f}s")
    print(f"  Average per Query: {avg_batch_time:.2f}s")
    print(f"  Success Rate: {batch_result['success_rate']:.2%}")
    
    return {
        'total_time': batch_time,
        'avg_time_per_query': avg_batch_time,
        'success_rate': batch_result['success_rate']
    }

def generate_performance_report(individual_results, batch_results):
    """Generate comprehensive performance report"""
    print(f"\n📈 PERFORMANCE REPORT")
    print("=" * 60)
    
    # Individual query statistics
    if individual_results['times']:
        avg_time = statistics.mean(individual_results['times'])
        max_time = max(individual_results['times'])
        min_time = min(individual_results['times'])
        success_rate = statistics.mean(individual_results['success_rates'])
        compliance_rate = statistics.mean(individual_results['compliance_rates'])
        
        print("INDIVIDUAL QUERY STATISTICS:")
        print(f"  Average Time: {avg_time:.2f}s")
        print(f"  Maximum Time: {max_time:.2f}s")
        print(f"  Minimum Time: {min_time:.2f}s")
        print(f"  Success Rate: {success_rate:.2%}")
        print(f"  Compliance Rate: {compliance_rate:.2%}")
    
    # Batch processing statistics
    print(f"\nBATCH PROCESSING STATISTICS:")
    print(f"  Average Time per Query: {batch_results['avg_time_per_query']:.2f}s")
    print(f"  Batch Success Rate: {batch_results['success_rate']:.2%}")
    
    # Performance ratings
    print(f"\n🎯 PERFORMANCE RATINGS:")
    
    # Speed rating
    if avg_time < 1.0:
        speed_rating = "⭐ EXCELLENT"
    elif avg_time < 2.0:
        speed_rating = "✅ GOOD"
    elif avg_time < 3.0:
        speed_rating = "⚠️ ACCEPTABLE"
    else:
        speed_rating = "🐌 SLOW"
    print(f"  Speed: {speed_rating} ({avg_time:.2f}s)")
    
    # Reliability rating
    if success_rate > 0.95:
        reliability_rating = "⭐ EXCELLENT"
    elif success_rate > 0.85:
        reliability_rating = "✅ GOOD"
    elif success_rate > 0.70:
        reliability_rating = "⚠️ ACCEPTABLE"
    else:
        reliability_rating = "❌ POOR"
    print(f"  Reliability: {reliability_rating} ({success_rate:.2%})")

if __name__ == "__main__":
    print("🚀 Starting Performance Tests")
    print("=" * 60)
    
    try:
        run_performance_tests()
        
        print(f"\n{'='*60}")
        print("🎉 PERFORMANCE TESTING COMPLETED SUCCESSFULLY!")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"❌ Performance testing failed: {e}")
        import traceback
        traceback.print_exc()