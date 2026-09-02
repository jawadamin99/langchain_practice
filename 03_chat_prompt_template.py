# ==========================================================
# 02_chat_prompt_template.py
#
# CONCEPT: ChatPromptTemplate
# --------------------------------------------------
# Chat models (like GPT) take a list of messages, not just
# a plain string. Each message has a "role":
#   - system : gives the model instructions / a personality
#   - human  : the user's question/message
#   - ai     : the model's previous response (in a conversation)
#
# ChatPromptTemplate lets us build this multi-role structure
# as a reusable template.
# ==========================================================

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from config.llm_config import llm

# Step 1: Build a chat template -> tuples of (role, message)
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that replies in a friendly tone."),
    ("human", "Tell me a fun fact about {subject}."),
])

# Step 2: Format the template with values -> produces a list of messages
messages = chat_template.format_messages(subject="Maths")

print("----- Generated Messages -----")
for m in messages:
    # print each message's type (SystemMessage/HumanMessage) and content
    print(f"{m.type}: {m.content}")

# Step 3: Send these messages to the LLM
response = llm.invoke(messages)

print("\n----- LLM Response -----")
print(response.text)
