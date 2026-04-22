"""
Performance Analysis Example
"""
import sys
sys.path.append('..')
from agents.monitor_agent import MonitorAgent
from agents.analyzer_agent import AnalyzerAgent

def performance_analysis():
    """Demonstrate analysis capabilities"""
    print("Performance Analysis Example")
    print("="*60)
    
    # Collect metrics
    monitor = MonitorAgent()
    analyzer = AnalyzerAgent()
    
    print("\nCollecting metrics...")
    for _ in range(3):
        monitor.collect_metrics()
    
    # Analyze metrics
    print("Analyzing metrics...")
    metrics_history = monitor.metrics_history
    analysis = analyzer.analyze_metrics(metrics_history)
    
    # Display results
    print("\n" + "="*60)
    print("ANALYSIS RESULTS")
    print("="*60)
    print(f"Anomalies Detected: {len(analysis.get('anomalies', []))}")
    for anomaly in analysis.get("anomalies", []):
        print(f"  - {anomaly['type']}: {anomaly['severity']} ({anomaly['value']:.1f}%)")
    
    bottleneck = analysis.get("bottleneck", {})
    print(f"\nBottleneck: {bottleneck.get('primary_bottleneck', 'None')}")
    print(f"Utilization:")
    for resource, util in bottleneck.get("utilization", {}).items():
        print(f"  - {resource}: {util:.1f}%")


if __name__ == "__main__":
    performance_analysis()
