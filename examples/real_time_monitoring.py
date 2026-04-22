"""
Real-time Monitoring Example
"""
import sys
import time
sys.path.append('..')
from agents.monitor_agent import MonitorAgent

def real_time_monitoring():
    """Demonstrate real-time monitoring capabilities"""
    print("Real-Time System Monitoring")
    print("-" * 50)
    
    monitor = MonitorAgent()
    
    # Collect metrics for 5 cycles
    print("\nCollecting metrics (5 iterations)...")
    for i in range(5):
        print(f"\nIteration {i+1}:")
        metrics = monitor.collect_metrics()
        
        cpu_pct = metrics["cpu"]["cpu_percent"]
        mem_pct = metrics["memory"]["percent"]
        disk_pct = metrics["disk"]["percent"]
        
        print(f"  CPU:    {cpu_pct:.1f}%")
        print(f"  Memory: {mem_pct:.1f}%")
        print(f"  Disk:   {disk_pct:.1f}%")
        
        time.sleep(2)
    
    # Display summary
    print("\n" + "="*50)
    print("Metrics Summary")
    print("="*50)
    summary = monitor.get_metrics_summary(window_size=5)
    print(f"CPU Avg:    {summary['cpu_avg']:.1f}%")
    print(f"CPU Max:    {summary['cpu_max']:.1f}%")
    print(f"Memory Avg: {summary['memory_avg']:.1f}%")
    print(f"Memory Max: {summary['memory_max']:.1f}%")


if __name__ == "__main__":
    real_time_monitoring()
