# ==========================================================
# 14_tool_calling.py
#
# CONCEPT: Tool Calling (Function Calling)
# --------------------------------------------------
# An LLM isn't a calculator by itself, nor does it know
# live weather data. By defining "tools" (functions), we
# give the LLM the power to decide for itself "which function
# should I run for this question", and then use its result to
# build the correct answer.
# ==========================================================

from langchain_core.tools import tool
from config.llm_config import llm

# Step 1: Turn a simple Python function into a "tool"
# The @tool decorator tells LangChain that this function is
# "callable" by the LLM
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together and return the result."""
    return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers together and return the result."""
    return a * b

tools = [add_numbers, multiply_numbers]

# Step 2: "Bind" the tools to the LLM (tell the LLM these tools are available)
llm_with_tools = llm.bind_tools(tools)

# Step 3: Ask a question -> the model decides for itself which tool is needed
question = "What is 15 plus 27?"
response = llm_with_tools.invoke(question)

print("----- Model's Tool Call Decision -----")
print(response.tool_calls)  # shows which function and with what values

# Step 4: If the model decided to call a tool, run it manually
# (in a real agent loop, this happens automatically)
if response.tool_calls:
    call = response.tool_calls[0]
    tool_name = call["name"]
    tool_args = call["args"]

    # Find and run the correct tool
    selected_tool = {t.name: t for t in tools}[tool_name]
    result = selected_tool.invoke(tool_args)

    print(f"\n----- Executing Tool: {tool_name}({tool_args}) -----")
    print("Result:", result)

# LESSON: Tool calling gives an LLM the ability to "take
# actions" — like running a calculator, a search engine, or a
# database query — instead of just generating text.
