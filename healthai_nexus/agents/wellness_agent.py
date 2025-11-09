from .base_agent import BaseAgent
import json

class WellnessAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Wellness Coach",
            template="""
            You are a Wellness Coach AI specializing in preventive health.
            
            Based on the patient's health assessment, create a personalized wellness plan.
            
            Patient Assessment: {medical_report}
            
            Provide a comprehensive wellness plan with:
            
            1. DIET PLAN:
               - Recommended foods
               - Foods to avoid
               - Meal timing suggestions
               - Hydration goals
            
            2. EXERCISE ROUTINE:
               - Type of exercises
               - Duration and frequency
               - Intensity level
               - Precautions
            
            3. LIFESTYLE MODIFICATIONS:
               - Sleep schedule (hours, timing)
               - Stress management techniques
               - Daily habits to adopt
               - Habits to eliminate
            
            4. PREVENTIVE MEASURES:
               - Health screenings needed
               - Supplements (if any)
               - Follow-up timeline
            
            Return as structured JSON:
            {{
                "diet": {{"foods_to_eat": [], "foods_to_avoid": [], "hydration": ""}},
                "exercise": {{"type": "", "duration": "", "frequency": "", "precautions": []}},
                "lifestyle": {{"sleep": "", "stress_management": [], "habits": []}},
                "preventive": {{"screenings": [], "supplements": [], "follow_up": ""}}
            }}
            
            Be specific, practical, and motivating.
            """
        )
    
    def run(self, medical_report):
        """Returns structured wellness plan"""
        response = super().run(medical_report)
        
        # Try to extract JSON
        try:
            if '{' in response and '}' in response:
                start = response.index('{')
                end = response.rindex('}') + 1
                json_data = json.loads(response[start:end])
                return json_data
        except:
            pass
        
        # Return text if JSON parsing fails
        return {"raw_plan": response}
