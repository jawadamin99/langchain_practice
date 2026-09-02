import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from langgraph.checkpoint.memory import MemorySaver
from config.llm_config import llm
load_dotenv()

# Google Search
search = GoogleSerperAPIWrapper(
    serper_api_key=os.getenv("SERPER_API_KEY")
)


system_prompt = """
You are a Google Search Agent.
You can search Google to answer user's questions.
"""


# Memory
memory = MemorySaver()


# Agent
agent = create_agent(
    model=llm,
    tools=[search.run],
    system_prompt=system_prompt,
    checkpointer=memory
)


# =========================
# THREAD 1
# =========================

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "My name is Jawad. I am looking for the best cash for cars services in Calgary, Alberta, Canada."
            }
        ]
    },
    {
        "configurable": {
            "thread_id": "jwd123"
        }
    }
)
print("\nAI:", response["messages"][-1].text)


# Same Thread ID
# response = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "What is my name?"
#             }
#         ]
#     },
#     {
#         "configurable": {
#             "thread_id": "awa123"
#         }
#     }
# )

# print("\nAI:", response["messages"][-1].text)


# =========================
# THREAD 2
# =========================


response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What was my name and what I was looking for?"
            }
        ]
    },
    {
        "configurable": {
            "thread_id": "jwd123"
        }
    }
)

print("\nAI:", response["messages"][-1].text)