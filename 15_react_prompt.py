# ==========================================================
# 15_react_prompt.py
#
# CONCEPT: ReAct Prompting (Reason + Act)
# --------------------------------------------------
# ReAct is a prompting technique where the model is explicitly
# told to follow a "Thought" (reasoning), "Action" (which tool
# it will use), "Observation" (what result it got) pattern,
# and then give a "Final Answer".
#
# This pattern is the foundation of agents — the model makes
# its reasoning process "visible", which makes debugging easier.
# ==========================================================

from langchain.prompts import PromptTemplate
from llm_config import llm

# Step 1: Build a ReAct-style template -> teach the model the format
react_template = """Answer the following question as best you can.
Use this exact format:

Question: the input question
Thought: think about what to do
Action: describe the action you would take (e.g., "search", "calculate")
Observation: the result of that action (imagine a plausible result)
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the question

Question: {question}
"""

react_prompt = PromptTemplate(
    input_variables=["question"],
    template=react_template,
)

final_prompt = react_prompt.format(
    question="If a train travels 60 km in 1 hour, how far will it travel in 3.5 hours?"
)

print("----- ReAct Prompt -----")
print(final_prompt)

response = llm.invoke(final_prompt)
print("\n----- Model's ReAct-style Response -----")
print(response.content)

# LESSON: The "Thought -> Action -> Observation" loop makes
# the model's reasoning transparent. In real agents, "Action"
# is replaced with an actual tool call (see file 14).
