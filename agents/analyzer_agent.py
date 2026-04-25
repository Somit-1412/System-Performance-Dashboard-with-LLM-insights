"""
Analyzer Agent - Analyzes performance data and detects anomalies
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os
from openai import OpenAI
from google import genai
import anthropic
from groq import Groq
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
        if not metrics:
            return {"error": "No metrics to analyze"}

        anomalies = detect_anomalies(metrics)
        bottleneck = analyze_bottleneck(metrics)
        correlations = find_correlation(metrics)

        explanation = self.generate_explanation(metrics, anomalies, bottleneck)

        analysis = {
            "timestamp": datetime.now().isoformat(),
            "anomalies": anomalies,
            "bottleneck": bottleneck,
            "correlations": correlations,
            "explanation": explanation
        }

        self.analysis_results.append(analysis)
        return analysis
    def generate_explanation(self, metrics, anomalies, bottleneck):
    
        model = os.getenv("LLM_MODEL")

        latest = metrics[-1]

        prompt = f"""
            You are a system performance analysis expert.

            System metrics:
            CPU: {latest['cpu']['cpu_percent']}%
            Memory: {latest['memory']['percent']}%
            Disk: {latest['disk']['percent']}%

            Anomalies: {anomalies}
            Bottleneck: {bottleneck}

            Explain:
            1. Current system health (Healthy / Warning / Critical)
            2. Why the system is in this state
            3. What is the main concern (if any)

            Keep it concise and technical.
            """

        # ---------- OpenAI ----------
        if "gpt" in model.lower():
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )

            return response.choices[0].message.content

        # ---------- Anthropic ----------
        elif "claude" in model.lower():
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            response = client.messages.create(
                model=model,
                max_tokens=200,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text
        
        # -------- Gemini --------
        elif "gemini" in model.lower():
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

            response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
            )

            return response.text
        
        # -------- Groq --------
        elif "groq" in model.lower():
           
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))

            response = client.chat.completions.create(
                model=os.getenv("GROQ_MODEL"),
                messages=[
                    {"role": "system", "content": "You are a performance analysis expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )

            return response.choices[0].message.content

        # ---------- Fallback ----------
        else:
            return "No valid LLM model configured"
    
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
