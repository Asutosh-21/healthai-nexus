"""Test triage routing for different symptoms"""

from triage_agent import TriageAgent

def test_triage():
    triage = TriageAgent()
    
    test_cases = [
        "high fever with cold symptoms, pain and other problems",
        "chest pain and shortness of breath",
        "severe headache and dizziness",
        "skin rash and itching",
        "trouble sleeping and fatigue",
        "weight loss and diet concerns",
        "cough, sore throat, and body aches"
    ]
    
    print("Testing Triage Agent Routing\n")
    print("=" * 60)
    
    for symptoms in test_cases:
        print(f"\nSymptoms: {symptoms}")
        specialists = triage.route(symptoms)
        print(f"Routed to: {', '.join([s.replace('_', ' ').title() for s in specialists])}")
        print("-" * 60)

if __name__ == "__main__":
    test_triage()
