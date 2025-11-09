from base_agent import BaseAgent

cardio_template = """
You are a highly skilled cardiologist. 
Analyze the following patient report and identify potential heart-related issues.
Provide detailed reasoning and possible next steps.

Medical Report:
{medical_report}
"""

agent = BaseAgent("Cardiologist", cardio_template)

report = """
Patient reports chest discomfort for 3 days, shortness of breath on exertion,
mild swelling in ankles, and dizziness. ECG shows ST-segment changes.
"""

response = agent.run(report)
print("\n🧠 Cardiologist Analysis:\n", response)
