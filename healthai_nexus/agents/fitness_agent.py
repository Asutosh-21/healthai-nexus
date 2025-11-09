from .base_agent import BaseAgent

class FitnessAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Fitness Coach",
            template="""
            You are a certified Fitness & Rehabilitation Coach AI.
            Based on the patient's symptoms, suggest:
            - Appropriate exercises
            - Physical activity levels
            - Safety precautions for cardiac or mobility issues
            Patient Report: {medical_report}
            """
        )
