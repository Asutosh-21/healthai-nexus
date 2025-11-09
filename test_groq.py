import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load your API key from the .env file
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY")
)

response = llm.invoke("Explain what hypertension is in simple terms.")
print(response.content)
