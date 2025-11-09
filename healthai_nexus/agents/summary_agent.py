from .base_agent import BaseAgent

class SummaryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Summary Doctor",
            template="""
            You are a Chief Medical Officer AI combining multiple specialist reports.
            Summarize all key findings clearly:
            - Possible diagnoses
            - Treatment or lifestyle suggestions
            - Urgency (if any)
            Present the report in a patient-friendly tone.
            Specialist Reports: {medical_report}
            """
        )
