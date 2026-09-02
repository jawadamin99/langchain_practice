# ==========================================================
# 03_system_prompt.py
#
# CONCEPT: System Prompt
# --------------------------------------------------
# The system prompt is a "hidden instruction" that the user
# doesn't see, but it sets the model's behavior/personality/
# rules. You can also think of it as a "role definition".
#
# Example: If we want the model to always respond like a
# "pirate", we specify that in the system prompt.
# ==========================================================

from langchain.prompts import ChatPromptTemplate
from llm_config import llm

# Different system prompts -> same question, different behavior
system_prompt_formal = "You are a professional assistant. Answer formally and concisely."
system_prompt_casual = "You are a witty pirate. Answer every question like a pirate would."

question = "What is Python programming language?"

for system_prompt in [system_prompt_formal, system_prompt_casual]:
    chat_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])

    messages = chat_template.format_messages(question=question)
    response = llm.invoke(messages)

    print(f"----- System Prompt: {system_prompt[:30]}... -----")
    print(response.content)
    print()

# LESSON: Changing the system prompt doesn't just change the
# "content" — it also changes the tone/style/persona. This is
# one of the most powerful tools in prompt engineering.
