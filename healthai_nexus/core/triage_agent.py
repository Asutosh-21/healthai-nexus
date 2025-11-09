import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import json

load_dotenv()

class TriageAgent:
    """Routes symptoms to relevant specialist agents"""
    
    SPECIALISTS = {
        "cardiologist": ["chest pain", "heart", "palpitation", "hypertension", "blood pressure", "cardiac", "angina", "arrhythmia"],
        "neurologist": ["headache", "migraine", "seizure", "dizziness", "memory", "tremor", "stroke", "vertigo", "numbness"],
        "nutritionist": ["diet", "weight loss", "weight gain", "nutrition", "obesity", "eating disorder", "vitamin", "meal plan", "diabetes diet"],
        "pharmacologist": ["medication", "drug", "prescription", "side effect", "dosage", "pill", "medicine", "antibiotic"],
        "fitness": ["exercise", "workout", "fitness", "physical activity", "training", "gym", "muscle pain", "sports injury"],
        "sleep": ["sleep", "insomnia", "fatigue", "tired", "rest", "snoring", "sleep apnea", "drowsy"],
        "dermatologist": ["skin", "rash", "acne", "eczema", "mole", "itching", "psoriasis", "hives", "sunburn"]
    }
    
    # General symptoms that need general practitioner
    GENERAL_SYMPTOMS = {
        "fever": ["general_practitioner", "pharmacologist"],
        "cold": ["general_practitioner"],
        "cough": ["general_practitioner"],
        "sore throat": ["general_practitioner"],
        "body pain": ["general_practitioner"],
        "body ache": ["general_practitioner"],
        "flu": ["general_practitioner"],
        "infection": ["general_practitioner"],
        "pain": ["general_practitioner"],
        "nausea": ["general_practitioner"],
        "vomiting": ["general_practitioner"],
        "diarrhea": ["general_practitioner", "nutritionist"],
        "runny nose": ["general_practitioner"],
        "congestion": ["general_practitioner"],
        "chills": ["general_practitioner"],
        "weakness": ["general_practitioner"]
    }
    
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.2,
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    def route(self, symptoms):
        """Determine which specialists to consult"""
        symptoms_lower = symptoms.lower()
        selected = set()
        
        # Check general symptoms first
        for symptom, specialists in self.GENERAL_SYMPTOMS.items():
            if symptom in symptoms_lower:
                selected.update(specialists)
        
        # Check specialist-specific keywords
        for specialist, keywords in self.SPECIALISTS.items():
            if any(kw in symptoms_lower for kw in keywords):
                selected.add(specialist)
        
        # LLM-based routing if no matches or for validation
        if not selected or len(selected) > 4:
            all_specialists = list(self.SPECIALISTS.keys()) + ["general_practitioner"]
            prompt = f"""Analyze these symptoms: "{symptoms}"

Select 2-3 most relevant specialists from: {', '.join(all_specialists)}

IMPORTANT:
- Use "general_practitioner" for common symptoms like fever, cold, flu, pain, cough
- Use specialists only for specific organ/system issues

Return ONLY a JSON array like: ["general_practitioner", "pharmacologist"]
Choose specialists who can best address these specific symptoms."""
            
            try:
                response = self.llm.invoke(prompt)
                content = response.content.strip()
                if '[' in content and ']' in content:
                    start = content.index('[')
                    end = content.rindex(']') + 1
                    llm_selected = json.loads(content[start:end])
                    if llm_selected:
                        selected = set(llm_selected)
            except:
                pass
        
        # Default to general practitioner for general symptoms if nothing selected
        if not selected:
            selected = {"general_practitioner", "pharmacologist"}
        
        return list(selected)[:4]  # Limit to 4 specialists max
