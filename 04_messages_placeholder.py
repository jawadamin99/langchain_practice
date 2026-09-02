# ==========================================================
# 04_messages_placeholder.py
#
# CONCEPT: MessagesPlaceholder
# --------------------------------------------------
# When building a chatbot that remembers the previous
# conversation, we need to insert the entire "chat history"
# list into the template.
#
# MessagesPlaceholder is an "empty slot" where the full list
# of messages can be inserted at runtime.
# ==========================================================

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from config.llm_config import llm

# Step 1: Build a template that has a slot for history
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the conversation history to answer."),
    MessagesPlaceholder(variable_name="chat_history"),  # previous conversation goes here
    ("human", "{question}"),
])

# Step 2: Create a fake previous conversation history (in a real app
# this would come from a database)
chat_history = [
    HumanMessage(content="My name is Jawad."),
    AIMessage(content="Nice to meet you, Jawad!"),
]

# Step 3: A new question that depends on the history
new_question = "What is my name?"

messages = chat_template.format_messages(
    chat_history=chat_history,
    question=new_question,
)

print("----- Full Message List Sent to Model -----")
for m in messages:
    print(f"{m.type}: {m.content}")

response = llm.invoke(messages)
print("\n----- LLM Response -----")
print(response.text)  # The model should remember "Ali" from the history
