import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class StructuredAgent:
    """Agent that returns structured JSON outputs"""
    
    def __init__(self, role, system_prompt):
        self.role = role
        self.system_prompt = system_prompt
        self.llm = ChatGroq(
            temperature=0.3,
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    def run(self, symptoms):
        """Returns structured JSON response"""
        prompt = f"""{self.system_prompt}

Patient Symptoms: {symptoms}

Return a JSON object with this structure:
{{
    "findings": ["finding1", "finding2"],
    "differential_diagnosis": ["condition1", "condition2"],
    "confidence": 0.8,
    "recommended_tests": ["test1", "test2"],
    "recommendations": ["recommendation1", "recommendation2"]
}}"""
        
        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()
            
            # Extract JSON
            if '{' in content and '}' in content:
                start = content.index('{')
                end = content.rindex('}') + 1
                json_str = content[start:end]
                return json.loads(json_str)
            else:
                return self._default_response()
        except Exception as e:
            return self._default_response()
    
    def _default_response(self):
        return {
            "findings": ["Unable to parse response"],
            "differential_diagnosis": [],
            "confidence": 0.0,
            "recommended_tests": [],
            "recommendations": []
        }
