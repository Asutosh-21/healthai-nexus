from .base_agent import BaseAgent

class NutritionistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Nutritionist",
            template="""
            You are a clinical Nutritionist AI.
            Based on the patient's condition and report, provide:
            - Recommended daily diet plan
            - Foods to include/avoid
            - Hydration & supplement advice
            Keep it evidence-based.
            Patient Report: {medical_report}
            """
        )
