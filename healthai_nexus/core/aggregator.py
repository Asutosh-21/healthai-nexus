import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from core.rag_retriever import RAGRetriever
import json

load_dotenv()

class Aggregator:
    """Synthesizes multiple agent outputs with RAG evidence"""
    
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.3,
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.rag = RAGRetriever()
    
    def synthesize(self, agent_results, symptoms):
        """Combine agent outputs with evidence"""
        # Collect all findings
        all_findings = []
        for agent_name, result in agent_results.items():
            all_findings.append(f"{agent_name.upper()}: {result}")
        
        combined = "\n\n".join(all_findings)
        
        # Retrieve evidence
        evidence = self.rag.retrieve(symptoms)
        
        # Generate final synthesis
        prompt = f"""Synthesize these specialist reports into a comprehensive medical assessment:

{combined}

Evidence-based information:
{evidence}

Create a final report with:
1. Key findings summary
2. Most likely diagnoses (with confidence)
3. Risk assessment
4. Recommended actions
5. When to seek immediate care

Be clear, professional, and patient-friendly."""
        
        try:
            response = self.llm.invoke(prompt)
            return {
                "synthesis": response.content,
                "evidence": evidence,
                "specialist_reports": agent_results
            }
        except Exception as e:
            return {
                "synthesis": f"Error generating synthesis: {str(e)}",
                "evidence": evidence,
                "specialist_reports": agent_results
            }
    
    def calculate_risk_score(self, agent_results):
        """Calculate overall risk score"""
        risk_keywords = ["urgent", "emergency", "severe", "critical", "immediate"]
        risk_count = 0
        total_words = 0
        
        for result in agent_results.values():
            if isinstance(result, str):
                words = result.lower().split()
                total_words += len(words)
                risk_count += sum(1 for word in words if any(kw in word for kw in risk_keywords))
        
        if total_words == 0:
            return 0.0
        
        risk_score = min((risk_count / total_words) * 100, 10.0)
        return round(risk_score, 2)
