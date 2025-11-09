from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.cardiologist_agent import CardiologistAgent
from agents.neurologist_agent import NeurologistAgent
from agents.nutritionist_agent import NutritionistAgent
from agents.pharmacologist_agent import PharmacologistAgent
from agents.fitness_agent import FitnessAgent
from agents.sleep_agent import SleepAgent
from agents.dermatologist_agent import DermatologistAgent
from agents.general_practitioner_agent import GeneralPractitionerAgent

class Orchestrator:
    """Manages concurrent execution of multiple specialist agents"""
    
    AGENT_MAP = {
        "cardiologist": CardiologistAgent,
        "neurologist": NeurologistAgent,
        "nutritionist": NutritionistAgent,
        "pharmacologist": PharmacologistAgent,
        "fitness": FitnessAgent,
        "sleep": SleepAgent,
        "dermatologist": DermatologistAgent,
        "general_practitioner": GeneralPractitionerAgent
    }
    
    def __init__(self):
        pass
    
    def execute(self, specialist_names, symptoms):
        """Execute multiple agents concurrently"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_agent = {}
            
            for name in specialist_names:
                if name in self.AGENT_MAP:
                    agent_class = self.AGENT_MAP[name]
                    agent = agent_class()
                    future = executor.submit(agent.run, symptoms)
                    future_to_agent[future] = name
            
            for future in as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                try:
                    result = future.result()
                    results[agent_name] = result
                except Exception as e:
                    results[agent_name] = f"Error: {str(e)}"
        
        return results
