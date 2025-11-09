from .base_agent import BaseAgent

class SleepAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Sleep Advisor",
            template="""
            You are a Sleep Specialist AI.
            Analyze sleep-related problems, stress, or fatigue issues.
            Suggest sleep hygiene practices and bedtime routines.
            Mention if medical evaluation for sleep apnea or insomnia is needed.
            Patient Report: {medical_report}
            """
        )
