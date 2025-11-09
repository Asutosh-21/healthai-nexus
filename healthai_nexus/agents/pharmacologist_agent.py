from .base_agent import BaseAgent

class PharmacologistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Pharmacologist",
            template="""
            You are a Pharmacologist AI.
            Review the patient's reported medications (if any) or symptoms.
            Detect possible drug interactions, contraindications, or unsafe combinations.
            Suggest safer alternatives and dosage advice.
            Patient Report: {medical_report}
            """
        )
