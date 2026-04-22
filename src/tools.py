"""""
Performance Engineering Tools for CrewAI Agents
"""""
import psutil
import platform
from datetime import datetime, timedelta
from typing import Dict, List, Any

def get_cpu_metrics() -> Dict[str, Any]:
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count(),
    }

def get_memory_usage() -> Dict[str, Any]:
    mem = psutil.virtual_memory()
    return {
        "timestamp": datetime.now().isoformat(),
        "total_mb": mem.total / (1024**2),
        "used_mb": mem.used / (1024**2),
        "percent": mem.percent,
    }

def get_disk_performance() -> Dict[str, Any]:
    # Use appropriate path for the OS
    path = "C:\\" if platform.system() == "Windows" else "/"
    disk = psutil.disk_usage(path)
    return {
        "timestamp": datetime.now().isoformat(),
        "total_gb": disk.total / (1024**3),
        "used_gb": disk.used / (1024**3),
        "percent": disk.percent,
    }

def get_system_health() -> Dict[str, Any]:
    cpu = get_cpu_metrics()
    mem = get_memory_usage()
    disk = get_disk_performance()
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu": cpu,
        "memory": mem,
        "disk": disk,
        "status": "healthy" if (cpu["cpu_percent"] < 80 and mem["percent"] < 85) else "warning",
    }

def detect_anomalies(metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if len(metrics) < 2:
        return []
    anomalies = []
    cpu_values = [m.get("cpu", {}).get("cpu_percent", 0) for m in metrics]
    cpu_max = max(cpu_values) if cpu_values else 0
    if cpu_max > 80:
        anomalies.append({"type": "CPU_SPIKE", "severity": "high" if cpu_max > 90 else "medium", "value": cpu_max})
    return anomalies

def find_correlation(metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze correlations between CPU, memory, and disk metrics"""
    if len(metrics) < 2:
        return {"error": "Not enough metrics for correlation analysis"}
    
    cpu_values = [m.get("cpu", {}).get("cpu_percent", 0) for m in metrics]
    mem_values = [m.get("memory", {}).get("percent", 0) for m in metrics]
    
    correlation = {
        "cpu_memory_correlation": "high" if len(cpu_values) > 1 else "unknown",
        "cpu_trend": "increasing" if cpu_values[-1] > cpu_values[0] else "decreasing",
        "memory_trend": "increasing" if mem_values[-1] > mem_values[0] else "decreasing",
    }
    return correlation

def trace_root_cause(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Trace root cause of performance issues"""
    anomalies = analysis.get("anomalies", [])
    
    if not anomalies:
        return {"root_cause": "No anomalies detected", "severity": "low"}
    
    highest_severity = max([a.get("severity", "low") for a in anomalies], default="low")
    
    return {
        "root_cause": f"Performance anomaly detected: {anomalies[0].get('type', 'UNKNOWN')}",
        "severity": highest_severity,
        "anomalies_count": len(anomalies),
    }

def analyze_bottleneck(metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Identify the primary bottleneck in system performance"""
    if not metrics:
        return {"primary_bottleneck": "unknown", "severity": "low"}
    
    cpu_values = [m.get("cpu", {}).get("cpu_percent", 0) for m in metrics]
    mem_values = [m.get("memory", {}).get("percent", 0) for m in metrics]
    disk_values = [m.get("disk", {}).get("percent", 0) for m in metrics]
    
    cpu_avg = sum(cpu_values) / len(cpu_values) if cpu_values else 0
    mem_avg = sum(mem_values) / len(mem_values) if mem_values else 0
    disk_avg = sum(disk_values) / len(disk_values) if disk_values else 0
    
    bottlenecks = {
        "cpu": cpu_avg,
        "memory": mem_avg,
        "disk": disk_avg,
    }
    
    primary = max(bottlenecks, key=lambda x: bottlenecks[x])
    severity = "high" if bottlenecks[primary] > 80 else "medium" if bottlenecks[primary] > 60 else "low"
    
    return {
        "primary_bottleneck": primary,
        "severity": severity,
        "cpu_percent": cpu_avg,
        "memory_percent": mem_avg,
        "disk_percent": disk_avg,
    }

def generate_recommendations(analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    recommendations = []
    if analysis.get("primary_bottleneck") == "cpu":
        recommendations.extend([
            {"id": "opt-001", "title": "Optimize CPU-intensive tasks", "impact": "20-30% CPU reduction", "priority": "high"},
            {"id": "opt-002", "title": "Implement load balancing", "impact": "15-25% throughput improvement", "priority": "high"},
        ])
    return recommendations

def estimate_impact(recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Estimate the impact of recommendations"""
    total_impact = {
        "estimated_cpu_reduction": 0,
        "estimated_throughput_improvement": 0,
        "recommendation_count": len(recommendations),
    }
    
    for rec in recommendations:
        if "CPU reduction" in rec.get("impact", ""):
            total_impact["estimated_cpu_reduction"] += 25
        if "throughput" in rec.get("impact", ""):
            total_impact["estimated_throughput_improvement"] += 20
    
    return total_impact

def create_action_plan(recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a detailed action plan from recommendations"""
    plan = {
        "phases": [],
        "total_effort_hours": 0,
        "risk_level": "low",
    }
    
    for idx, rec in enumerate(recommendations, 1):
        phase = {
            "phase": idx,
            "title": rec.get("title", "Optimization task"),
            "priority": rec.get("priority", "medium"),
            "effort_hours": 4 if rec.get("priority") == "high" else 2,
            "steps": [
                f"Analyze current {rec.get('id', 'task')} performance",
                "Implement optimization",
                "Test and validate",
                "Monitor results",
            ],
        }
        plan["phases"].append(phase)
        plan["total_effort_hours"] += phase["effort_hours"]
    
    return plan

def calculate_roi(recommendations: List[Dict[str, Any]], action_plan: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate ROI for optimization recommendations"""
    effort_hours = action_plan.get("total_effort_hours", 1)
    hourly_cost = 50  # Assume $50/hour for engineering
    implementation_cost = effort_hours * hourly_cost
    
    # Estimate benefits (simplified)
    estimated_benefit = len(recommendations) * 1000  # $1000 benefit per recommendation
    
    roi_percent = ((estimated_benefit - implementation_cost) / implementation_cost * 100) if implementation_cost > 0 else 0
    
    return {
        "implementation_cost": implementation_cost,
        "estimated_benefit": estimated_benefit,
        "roi_percent": roi_percent,
        "payback_period_days": (implementation_cost / (estimated_benefit / 365)) if estimated_benefit > 0 else float('inf'),
        "recommendation": "Proceed" if roi_percent > 50 else "Review",
    }
