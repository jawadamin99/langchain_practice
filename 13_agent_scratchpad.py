# ==========================================================
# 13_agent_scratchpad.py
#
# CONCEPT: Agent Scratchpad
# --------------------------------------------------
# When an AI "agent" takes multiple steps to solve a task
# (like: think -> use a tool -> observe -> think again), that
# entire "working memory" is called the "scratchpad" — like
# doing rough work on paper before giving the final answer.
#
# This scratchpad is injected into the prompt so the model
# knows what it has already thought and observed so far.
# ==========================================================

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from llm_config import llm

# Step 1: Build a template that has a slot for the "agent_scratchpad"
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an agent that solves problems step by step. "
               "Use the scratchpad below to see your previous thoughts."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # <-- "rough work" goes here
])

# Step 2: Simulate what the agent thought before (normally this is
# built automatically by a tool-calling loop)
scratchpad = [
    AIMessage(content="Thought: I need to break 12 * 7 into smaller steps."),
    AIMessage(content="Thought: 12 * 7 = 12 * 7 = 84."),
]

messages = agent_prompt.format_messages(
    input="What is 12 multiplied by 7?",
    agent_scratchpad=scratchpad,
)

print("----- Full Prompt with Scratchpad -----")
for m in messages:
    print(f"{m.type}: {m.content}")

response = llm.invoke(messages)
print("\n----- Final Agent Answer -----")
print(response.content)

# LESSON: The scratchpad gives the agent "context about its
# own reasoning" so it doesn't forget previous steps and
# stays consistent.
