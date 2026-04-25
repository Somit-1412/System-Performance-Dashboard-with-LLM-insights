"""
Crew Manager - Orchestrates agents for performance engineering
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import json
import sys
sys.path.append('..')
from agents.monitor_agent import MonitorAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.optimizer_agent import OptimizerAgent

class PerformanceEngineeringCrew:
    """Main orchestrator for performance engineering workflow"""
    
    def __init__(self):
        self.monitor_agent = MonitorAgent()
        self.analyzer_agent = AnalyzerAgent()
        self.optimizer_agent = OptimizerAgent()
        
        self.agents = [self.monitor_agent, self.analyzer_agent, self.optimizer_agent]
        self.execution_history = []
        self.final_report = None
    
    def execute_cycle(self) -> Dict[str, Any]:
        print("EXECUTE_CYCLE CALLED")
        """Execute one complete performance engineering cycle"""
        cycle_report = {
            "cycle_id": f"CYCLE-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "stages": {}
        }
        
        # Stage 1: Monitoring
        print("[1/3] Collecting metrics...")
        metrics = self.monitor_agent.collect_metrics()
        cycle_report["stages"]["monitoring"] = {
            "status": "completed",
            "metrics_collected": metrics,
            "history_size": len(self.monitor_agent.metrics_history)
        }
        
        # Stage 2: Analysis
        print("[2/3] Analyzing metrics...")

        metrics_history = self.monitor_agent.metrics_history[-10:] if len(self.monitor_agent.metrics_history) > 0 else []
        analysis = self.analyzer_agent.analyze_metrics(metrics_history)

        cycle_report["stages"]["analysis"] = {
            "status": "completed",
            "anomalies_detected": len(analysis.get("anomalies", [])),
            "primary_bottleneck": analysis.get("bottleneck", {}).get("primary_bottleneck", "unknown"),
            "explanation": analysis.get("explanation", "No explanation available")
        }
        
        # Stage 3: Optimization
        print("[3/3] Generating recommendations...")

        recommendations = self.optimizer_agent.generate_recommendations(analysis)

        cycle_report["stages"]["optimization"] = {
            "status": "completed",
            "recommendations_generated": len(recommendations),
            "recommendations": recommendations
        }

        if recommendations:
            action_plan = self.optimizer_agent.create_plan(recommendations)
            cycle_report["stages"]["optimization"]["action_plan"] = action_plan

        self.execution_history.append(cycle_report)
        return cycle_report
    
    def generate_report(self, cycles: int = 1) -> Dict[str, Any]:
        """Generate comprehensive performance engineering report"""
        print(f"\nExecuting {cycles} performance engineering cycle(s)...")
        
        for i in range(cycles):
            print(f"\n=== Cycle {i+1}/{cycles} ===")
            cycle = self.execute_cycle()
        
        report = {
            "report_id": f"REPORT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "total_cycles": len(self.execution_history),
            "summary": self._generate_summary(),
            "execution_history": self.execution_history
        }
        
        self.final_report = report
        return report
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        if not self.execution_history:
            return {"message": "No execution history"}
        
        total_anomalies = sum(
            cycle["stages"]["analysis"].get("anomalies_detected", 0)
            for cycle in self.execution_history
        )
        
        total_recommendations = sum(
            cycle["stages"]["optimization"].get("recommendations_generated", 0)
            for cycle in self.execution_history
        )
        
        return {
            "total_anomalies_detected": total_anomalies,
            "total_recommendations": total_recommendations,
            "average_recommendations_per_cycle": total_recommendations / len(self.execution_history) if self.execution_history else 0,
            "execution_status": "completed"
        }
    
    def save_report(self, filename: Optional[str] = None) -> str:
        """Save report to file"""
        if filename is None:
            filename = f"results/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        Path("results").mkdir(exist_ok=True)
        with open(filename, "w") as f:
            json.dump(self.final_report or self.execution_history, f, indent=2)
        
        print(f"Report saved to {filename}")
        return filename


def main():
    """Main entry point"""
    crew = PerformanceEngineeringCrew()
    report = crew.generate_report(cycles=1)
    crew.save_report()
    
    print("\n" + "="*60)
    print("PERFORMANCE ENGINEERING CREW REPORT")
    print("="*60)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
