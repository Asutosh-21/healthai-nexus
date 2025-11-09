"""Test script for the HealthAI Nexus system"""

from preprocessor import InputPreprocessor
from triage_agent import TriageAgent
from orchestrator import Orchestrator
from aggregator import Aggregator
from database import Database
from sample_dataset import SAMPLE_CASES

def test_system():
    print("🏥 Testing HealthAI Nexus System\n")
    
    # Initialize components
    preprocessor = InputPreprocessor()
    triage = TriageAgent()
    orchestrator = Orchestrator()
    aggregator = Aggregator()
    db = Database()
    
    # Test with sample case
    test_case = SAMPLE_CASES[0]
    symptoms = test_case['symptoms']
    
    print(f"📝 Input Symptoms: {symptoms}\n")
    
    # Step 1: Preprocess
    print("Step 1: Preprocessing...")
    processed = preprocessor.process(symptoms)
    print(f"✅ Processed: {processed}\n")
    
    # Step 2: Triage
    print("Step 2: Triage routing...")
    specialists = triage.route(processed)
    print(f"✅ Selected specialists: {specialists}\n")
    
    # Step 3: Execute agents
    print("Step 3: Executing agents concurrently...")
    results = orchestrator.execute(specialists, processed)
    print(f"✅ Got {len(results)} specialist reports\n")
    
    for specialist, report in results.items():
        print(f"  - {specialist}: {report[:100]}...")
    
    # Step 4: Aggregate
    print("\nStep 4: Aggregating with RAG...")
    synthesis = aggregator.synthesize(results, processed)
    risk_score = aggregator.calculate_risk_score(results)
    print(f"✅ Risk Score: {risk_score}/10")
    print(f"✅ Synthesis: {synthesis['synthesis'][:200]}...\n")
    
    # Step 5: Save to database
    print("Step 5: Saving to database...")
    report_data = {
        'symptoms': symptoms,
        'risk_score': risk_score,
        'synthesis': synthesis['synthesis'],
        'evidence': synthesis['evidence'],
        'specialist_reports': results
    }
    report_id = db.save_report(report_data)
    print(f"✅ Saved with ID: {report_id}\n")
    
    print("🎉 System test completed successfully!")

if __name__ == "__main__":
    test_system()
