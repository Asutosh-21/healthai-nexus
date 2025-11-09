import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# ✅ Load environment variables
load_dotenv()

class BaseAgent:
    def __init__(self, role, template):
        """
        Base class for all medical AI agents.
        :param role: Agent role (e.g., 'Cardiologist', 'Nutritionist')
        :param template: PromptTemplate for agent instructions
        """
        self.role = role
        self.prompt = PromptTemplate.from_template(template)

        # --- Load Groq API key from .env ---
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "⚠️ GROQ_API_KEY not found. Please add it to your .env file:\n"
                "GROQ_API_KEY=your_api_key_here"
            )

        # ✅ Initialize the Groq LLM client
        # You can switch models here (e.g., llama-3.3-8b for faster but smaller model)
        try:
            self.llm = ChatGroq(
                temperature=0.3,
                model="llama-3.3-70b-versatile",
                api_key=api_key
            )
        except Exception as e:
            raise RuntimeError(f"❌ Failed to initialize Groq LLM: {str(e)}")

    def run(self, medical_report):
        """
        Executes the agent with a given medical report or input text.
        Returns a structured analysis or recommendations.
        """
        final_prompt = self.prompt.format(medical_report=medical_report)
        print(f"🩺 {self.role} is processing...")

        try:
            response = self.llm.invoke(final_prompt)
            return response.content
        except Exception as e:
            return f"⚠️ Error in {self.role}: {str(e)}"
