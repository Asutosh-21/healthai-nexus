from .base_agent import BaseAgent

class DermatologistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Dermatologist",
            template="""
            You are a Dermatologist AI.
            Evaluate the patient's skin or hair issues based on report or description.
            Identify likely causes (e.g., acne, eczema, infections).
            Suggest topical treatments or further dermatologist visits.
            Patient Report: {medical_report}
            """
        )
