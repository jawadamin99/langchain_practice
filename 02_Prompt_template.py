import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Create Gemini LLM
# ==========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Step 1: Create a template -> {topic} is a placeholder/variable
mytopic = input("Enter the Topic")
template_text = "Explain the concept of {topic} in simple words for a beginner."


prompt = PromptTemplate(
    input_variables=[mytopic],   # tells the template which variables it has
    template=template_text,
)

# Step 2: "Format" the template with values -> produces the real prompt

final_prompt = prompt.format(topic=mytopic)
print("----- Generated Prompt -----")
print(final_prompt)

# Step 3: Send this generated prompt to the LLM
response = llm.invoke(final_prompt)

print("\n----- LLM Response -----")
print(response.text)

# TIP: The same template can be reused with multiple topics:
# prompt.format(topic="Machine Learning")
# prompt.format(topic="Blockchain")
