import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from services.drug_interaction_checker import DrugInteractionChecker
import json

load_dotenv()

class TreatmentRecommender:
    """Personalized treatment and medication recommendations"""
    
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.3,
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.drug_checker = DrugInteractionChecker()
    
    def recommend_treatment(self, diagnosis, patient_profile):
        """Generate personalized treatment plan"""
        age = patient_profile.get('age', 'adult')
        weight = patient_profile.get('weight', 'average')
        allergies = patient_profile.get('allergies', [])
        current_meds = patient_profile.get('current_medications', [])
        
        prompt = f"""Create a personalized treatment plan for:

Diagnosis/Condition: {diagnosis}

Patient Profile:
- Age: {age}
- Weight: {weight}
- Allergies: {', '.join(allergies) if allergies else 'None'}
- Current Medications: {', '.join(current_meds) if current_meds else 'None'}

Provide:
1. Recommended medications (generic names)
2. Dosage based on age/weight
3. Treatment duration
4. Non-pharmacological treatments
5. Monitoring requirements

Return as JSON:
{{
    "medications": [{{"name": "", "dosage": "", "frequency": "", "duration": ""}}],
    "non_pharmacological": [],
    "monitoring": [],
    "precautions": []
}}"""
        
        try:
            response = self.llm.invoke(prompt)
            content = response.content
            
            if '{' in content and '}' in content:
                start = content.index('{')
                end = content.rindex('}') + 1
                treatment_plan = json.loads(content[start:end])
                
                # Check drug safety for each medication
                if 'medications' in treatment_plan:
                    for med in treatment_plan['medications']:
                        safety = self.drug_checker.check_drug_safety(
                            med.get('name', ''),
                            patient_profile
                        )
                        med['safety_check'] = safety
                
                return treatment_plan
        except:
            pass
        
        return {
            "medications": [],
            "non_pharmacological": ["Consult healthcare provider for treatment plan"],
            "monitoring": [],
            "precautions": []
        }
    
    def get_medication_details(self, medication_name):
        """Get detailed information about a medication"""
        prompt = f"""Provide comprehensive information about: {medication_name}

Include:
1. What it treats
2. How it works
3. Common side effects
4. Serious side effects
5. Food/drug interactions
6. Storage instructions

Be concise and patient-friendly."""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except:
            return "Information not available"
