import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class RAGRetriever:
    """Retrieves evidence-based medical information"""
    
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.1,
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
        # In production, this would connect to a vector database
        self.knowledge_base = {
            "hypertension": "Evidence: ACC/AHA guidelines recommend lifestyle modifications and medication for BP >130/80",
            "diabetes": "Evidence: ADA standards recommend HbA1c <7% for most adults",
            "chest_pain": "Evidence: HEART score helps stratify acute chest pain risk"
        }
    
    def retrieve(self, query):
        """Retrieve relevant medical evidence"""
        # Simple keyword matching (in production, use vector similarity)
        query_lower = query.lower()
        evidence = []
        
        for condition, info in self.knowledge_base.items():
            if condition in query_lower:
                evidence.append(info)
        
        # LLM-enhanced retrieval
        if evidence:
            return " | ".join(evidence)
        
        prompt = f"""Provide evidence-based medical information for: {query}
        
Include clinical guidelines or research findings. Be concise."""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except:
            return "No specific evidence found."
