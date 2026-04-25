from flask import Flask, render_template, jsonify
from agents.crew_manager import PerformanceEngineeringCrew
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
crew = PerformanceEngineeringCrew()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_cycle():
    report = crew.generate_report(cycles=1)
    return jsonify(report)

@app.route("/history")
def history():
    return jsonify(crew.execution_history)

if __name__ == "__main__":
    app.run(debug=True)