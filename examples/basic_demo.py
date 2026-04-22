"""
Basic Demo - Introduction to Agentic AI Performance Engineering
"""
import sys
sys.path.append('..')
from agents.crew_manager import PerformanceEngineeringCrew

def basic_demo():
    """Run basic demo showing agent interactions"""
    print("="*70)
    print("AGENTIC AI & CREWAI: PERFORMANCE ENGINEERING DEMO")
    print("="*70)
    
    # Initialize crew
    crew = PerformanceEngineeringCrew()
    
    # Run performance engineering cycle
    print("\nStarting Performance Engineering Cycle...")
    report = crew.generate_report(cycles=1)
    
    # Display results
    print("\n" + "="*70)
    print("CYCLE SUMMARY")
    print("="*70)
    summary = report["summary"]
    print(f"Anomalies Detected: {summary.get('total_anomalies_detected', 0)}")
    print(f"Recommendations: {summary.get('total_recommendations', 0)}")
    print(f"Status: {summary.get('execution_status', 'unknown')}")
    
    # Save results
    crew.save_report()
    print("\nDemo completed!")


if __name__ == "__main__":
    basic_demo()
