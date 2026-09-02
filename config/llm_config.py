import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq



load_dotenv()

# ==========================================================
# Create Gemini LLM
# ==========================================================

llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


# ==========================================================
# Create GROQ LLM
# ==========================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)