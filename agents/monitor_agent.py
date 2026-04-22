"""
Monitor Agent - Collects system performance metrics
"""
from typing import Dict, Any
from datetime import datetime
import sys
sys.path.append('..')
from src.tools import get_cpu_metrics, get_memory_usage, get_disk_performance, get_system_health

class MonitorAgent:
    """Monitor Agent - Data Collector"""
    
    def __init__(self):
        self.name = "Monitor Agent"
        self.role = "Data Collector"
        self.goal = "Continuously monitor system performance and collect real-time metrics"
        self.metrics_history = []
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu": get_cpu_metrics(),
            "memory": get_memory_usage(),
            "disk": get_disk_performance(),
        }
        self.metrics_history.append(metrics)
        return metrics
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system health status"""
        return get_system_health()
    
    def get_metrics_summary(self, window_size: int = 10) -> Dict[str, Any]:
        """Get aggregated metrics summary"""
        recent_metrics = self.metrics_history[-window_size:]
        if not recent_metrics:
            return {"error": "No metrics available"}
        
        cpu_values = [m["cpu"]["cpu_percent"] for m in recent_metrics]
        mem_values = [m["memory"]["percent"] for m in recent_metrics]
        
        return {
            "collection_count": len(recent_metrics),
            "cpu_avg": sum(cpu_values) / len(cpu_values),
            "cpu_max": max(cpu_values),
            "cpu_min": min(cpu_values),
            "memory_avg": sum(mem_values) / len(mem_values),
            "memory_max": max(mem_values),
            "memory_min": min(mem_values),
        }
    
    def execute(self, task: str) -> Dict[str, Any]:
        """Execute monitor tasks"""
        if task == "collect_metrics":
            return self.collect_metrics()
        elif task == "system_status":
            return self.get_system_status()
        elif task == "metrics_summary":
            return self.get_metrics_summary()
        return {"error": f"Unknown task: {task}"}
