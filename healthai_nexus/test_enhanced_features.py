"""Test script for enhanced features"""

from treatment_recommender import TreatmentRecommender
from drug_interaction_checker import DrugInteractionChecker
from agents.wellness_agent import WellnessAgent

def test_treatment_recommender():
    print("=" * 60)
    print("Testing Treatment Recommender")
    print("=" * 60)
    
    recommender = TreatmentRecommender()
    
    patient_profile = {
        'age': 'Adult (18-64)',
        'weight': 'Normal',
        'allergies': ['penicillin'],
        'current_medications': ['aspirin'],
        'conditions': ['hypertension']
    }
    
    diagnosis = "Upper respiratory infection with fever and cough"
    
    print(f"\nDiagnosis: {diagnosis}")
    print(f"Patient: {patient_profile['age']}, Allergies: {patient_profile['allergies']}")
    
    treatment = recommender.recommend_treatment(diagnosis, patient_profile)
    
    print("\nTreatment Plan:")
    if treatment.get('medications'):
        print("\nMedications:")
        for med in treatment['medications']:
            print(f"  - {med.get('name')}: {med.get('dosage')} {med.get('frequency')}")
            if 'safety_check' in med:
                print(f"    Safety: {med['safety_check'].get('safety')}")
    
    if treatment.get('non_pharmacological'):
        print("\nNon-Pharmacological:")
        for item in treatment['non_pharmacological']:
            print(f"  - {item}")
    
    print("\n" + "=" * 60)

def test_drug_checker():
    print("\nTesting Drug Interaction Checker")
    print("=" * 60)
    
    checker = DrugInteractionChecker()
    
    patient_profile = {
        'age': 'Adult (18-64)',
        'allergies': ['sulfa drugs'],
        'current_medications': ['warfarin'],
        'conditions': ['diabetes']
    }
    
    drug = "ibuprofen"
    
    print(f"\nChecking: {drug}")
    print(f"Current meds: {patient_profile['current_medications']}")
    
    safety = checker.check_drug_safety(drug, patient_profile)
    
    print(f"\nSafety Assessment: {safety.get('safety')}")
    if safety.get('interactions'):
        print(f"Interactions: {', '.join(safety['interactions'][:2])}")
    if safety.get('warnings'):
        print(f"Warnings: {', '.join(safety['warnings'][:2])}")
    
    print("\n" + "=" * 60)

def test_wellness_agent():
    print("\nTesting Wellness Agent")
    print("=" * 60)
    
    agent = WellnessAgent()
    
    assessment = """
    Patient has mild hypertension and is overweight.
    Sedentary lifestyle with poor diet habits.
    Stress from work. Irregular sleep schedule.
    """
    
    print(f"\nAssessment: {assessment.strip()}")
    
    wellness_plan = agent.run(assessment)
    
    print("\nWellness Plan Generated:")
    if isinstance(wellness_plan, dict):
        if 'diet' in wellness_plan:
            print("  - Diet plan included")
        if 'exercise' in wellness_plan:
            print("  - Exercise routine included")
        if 'lifestyle' in wellness_plan:
            print("  - Lifestyle modifications included")
        if 'preventive' in wellness_plan:
            print("  - Preventive measures included")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    print("\nTesting Enhanced Features\n")
    
    try:
        test_treatment_recommender()
    except Exception as e:
        print(f"Error in treatment recommender: {e}")
    
    try:
        test_drug_checker()
    except Exception as e:
        print(f"Error in drug checker: {e}")
    
    try:
        test_wellness_agent()
    except Exception as e:
        print(f"Error in wellness agent: {e}")
    
    print("\nAll tests completed!")
