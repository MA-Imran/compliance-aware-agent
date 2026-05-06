# run_system.py
#!/usr/bin/env python3
"""
Main entry point for the Compliance-Aware Multi-Agent System
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import EnhancedComplianceAwareAgentSystem

def main():
    """Main function to run the system"""
    print("🚀 Compliance-Aware Multi-Agent System")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "demo":
            run_demo()
        elif command == "examples":
            run_examples()
        elif command == "interactive":
            run_interactive_mode()
        else:
            print("Usage: python run_system.py [demo|examples|interactive]")
    else:
        # Default: run examples
        run_examples()


def run_demo():
    """Run comprehensive demo"""
    try:
        from examples.enhanced_demo import run_comprehensive_demo
        run_comprehensive_demo()
    except ImportError as e:
        print(f"Demo module not available: {e}")
        print("Please make sure all example files are created.")

def run_examples():
    """Run example queries"""
    from examples.example_queries import demonstrate_example_queries
    demonstrate_example_queries()

def run_interactive_mode():
    """Run system in interactive mode"""
    system = EnhancedComplianceAwareAgentSystem()
    print("\n💬 Interactive Mode - Type 'quit' to exit")
    print("Enter your queries below:")
    
    while True:
        try:
            query = input("\n🔍 Query: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                break
            if query:
                result = system.process_query(query)
                display_interactive_result(result)
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def display_interactive_result(result):
    """Display result in interactive mode"""
    if result['success']:
        print("✅ Success!")
        insights = result['insights']['structured_insights']
        print(f"📊 Response: {insights['query_response']}")
        
        compliance = result['compliance_check']
        status = "🟢 COMPLIANT" if compliance['overall_compliant'] else "🔴 NON-COMPLIANT"
        print(f"🛡️ Compliance: {status}")
        
        metrics = result['performance_metrics']
        print(f"⏱️ Processing Time: {metrics['total_processing_time']:.2f}s")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()