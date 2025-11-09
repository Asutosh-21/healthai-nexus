from .base_agent import BaseAgent

class NeurologistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Neurologist",
            template="""
            You are an AI Neurologist.
            Evaluate possible brain or nerve-related causes based on the patient's symptoms.
            Mention signs that indicate migraines, neural disorders, or cognitive issues.
            Suggest MRI/EEG or referrals if required.
            Patient Report: {medical_report}
            """
        )
