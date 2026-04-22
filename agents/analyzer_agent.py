"""
Analyzer Agent - Analyzes performance data and detects anomalies
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
sys.path.append('..')
from src.tools import detect_anomalies, find_correlation, trace_root_cause, analyze_bottleneck

class AnalyzerAgent:
    """Analyzer Agent - Problem Solver"""
    
    def __init__(self):
        self.name = "Analyzer Agent"
        self.role = "Performance Analyst"
        self.goal = "Detect anomalies, analyze patterns, and identify bottlenecks"
        self.analysis_results = []
    
    def analyze_metrics(self, metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comprehensive analysis on metrics"""
        if not metrics:
            return {"error": "No metrics to analyze"}
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "anomalies": detect_anomalies(metrics),
            "bottleneck": analyze_bottleneck(metrics),
            "correlations": find_correlation(metrics),
        }
        self.analysis_results.append(analysis)
        return analysis
    
    def trace_issues(self, anomalies: List[Dict[str, Any]], metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Trace root causes of issues"""
        return trace_root_cause({"anomalies": anomalies, "metrics": metrics})
    
    def execute(self, task: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute analyzer tasks"""
        if not data:
            return {"error": "No data provided"}
        if task == "analyze_metrics":
            return self.analyze_metrics(data.get("metrics", []))
        elif task == "trace_root_cause":
            return self.trace_issues(data.get("anomalies", []), data.get("metrics", []))
        return {"error": f"Unknown task: {task}"}
