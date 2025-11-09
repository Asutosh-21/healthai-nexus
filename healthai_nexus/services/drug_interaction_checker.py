import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class DrugInteractionChecker:
    """Check drug interactions and safety using OpenFDA API"""
    
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.2,
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.openfda_base = "https://api.fda.gov/drug"
    
    def check_drug_safety(self, drug_name, patient_profile):
        """Check drug safety based on patient profile"""
        age = patient_profile.get('age', 'adult')
        allergies = patient_profile.get('allergies', [])
        current_meds = patient_profile.get('current_medications', [])
        conditions = patient_profile.get('conditions', [])
        
        # Query OpenFDA for drug info
        drug_info = self._query_openfda(drug_name)
        
        # Use LLM to analyze safety
        prompt = f"""Analyze drug safety for: {drug_name}

Patient Profile:
- Age: {age}
- Allergies: {', '.join(allergies) if allergies else 'None'}
- Current Medications: {', '.join(current_meds) if current_meds else 'None'}
- Medical Conditions: {', '.join(conditions) if conditions else 'None'}

Drug Information: {drug_info}

Provide:
1. Safety assessment (Safe/Caution/Contraindicated)
2. Drug-drug interactions
3. Allergy concerns
4. Dosage recommendations
5. Warnings

Return as JSON:
{{"safety": "Safe/Caution/Contraindicated", "interactions": [], "warnings": [], "dosage": ""}}"""
        
        try:
            response = self.llm.invoke(prompt)
            content = response.content
            if '{' in content and '}' in content:
                import json
                start = content.index('{')
                end = content.rindex('}') + 1
                return json.loads(content[start:end])
        except:
            pass
        
        return {
            "safety": "Unknown",
            "interactions": ["Unable to verify"],
            "warnings": ["Consult healthcare provider"],
            "dosage": "As prescribed"
        }
    
    def _query_openfda(self, drug_name):
        """Query OpenFDA API for drug information"""
        try:
            url = f"{self.openfda_base}/label.json?search=openfda.brand_name:{drug_name}&limit=1"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    result = data['results'][0]
                    info = {
                        'warnings': result.get('warnings', ['No warnings found']),
                        'indications': result.get('indications_and_usage', ['No indications found'])
                    }
                    return str(info)[:500]
        except:
            pass
        return "Drug information not available from FDA database"
    
    def recommend_alternatives(self, drug_name, reason):
        """Recommend alternative medications"""
        prompt = f"""Suggest 3 alternative medications for: {drug_name}
Reason for alternative: {reason}

Provide safer or more suitable alternatives with brief explanations.
Return as JSON array: [{{"drug": "name", "reason": "why better"}}]"""
        
        try:
            response = self.llm.invoke(prompt)
            content = response.content
            if '[' in content and ']' in content:
                import json
                start = content.index('[')
                end = content.rindex(']') + 1
                return json.loads(content[start:end])
        except:
            pass
        
        return [{"drug": "Consult pharmacist", "reason": "For personalized alternatives"}]
