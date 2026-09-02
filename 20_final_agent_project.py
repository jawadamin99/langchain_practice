# ==========================================================
# 20_final_agent_project.py
#
# CONCEPT: Final Project - "Study Helper Agent"
# --------------------------------------------------
# This file combines all the course concepts into one small
# real agent:
#
#   1. System Prompt        (file 03) -> the agent's persona
#   2. ChatPromptTemplate   (file 02) -> structured messages
#   3. MessagesPlaceholder  (file 04) -> conversation memory
#   4. Tool Calling         (file 14) -> a calculator tool
#   5. Chain-of-Thought     (file 17) -> "step by step" reasoning
#   6. Structured Output    (file 10) -> final summary as JSON
#   7. LCEL Pipeline        (file 12) -> chaining with "|"
#
# The agent's job: answer a student's questions, do math
# using a tool when needed, and finally return a structured
# "StudySummary" object.
# ==========================================================

from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from llm_config import llm


# ---------- 1. Define a tool (CONCEPT: Tool Calling) ----------
@tool
def calculate(expression: str) -> str:
    """Evaluate a simple math expression, e.g. '12 * 7 + 3'."""
    try:
        # NOTE: eval() is used here only for demo/learning purposes.
        # In production, always use a safe math parser.
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


tools = [calculate]
llm_with_tools = llm.bind_tools(tools)


# ---------- 2. System Prompt (CONCEPT: System Prompt + CoT) ----------
SYSTEM_PROMPT = (
    "You are 'StudyBuddy', a friendly and patient study helper for students. "
    "Always think step by step before answering (chain-of-thought). "
    "If the question involves a calculation, use the 'calculate' tool instead "
    "of doing math yourself."
)


# ---------- 3. Chat Template with a memory slot (CONCEPT: ChatPromptTemplate + MessagesPlaceholder) ----------
chat_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])


# ---------- 4. Structured Output schema (CONCEPT: Structured Output) ----------
class StudySummary(BaseModel):
    topic: str = Field(description="The main topic of the question")
    answer: str = Field(description="A concise final answer for the student")
    difficulty: str = Field(description="Estimated difficulty: easy, medium, or hard")


def run_study_agent(question: str, chat_history: list) -> StudySummary:
    """
    This function runs the entire agent flow:
    build prompt -> call the tool-aware LLM -> (if a tool call
    was made, execute it) -> generate the structured summary.
    """
    # Step A: Build the messages from the template
    messages = chat_template.format_messages(
        chat_history=chat_history,
        question=question,
    )

    # Step B: Call the tool-aware LLM
    response = llm_with_tools.invoke(messages)

    # Step C: If the model decided to use a tool, execute it
    if response.tool_calls:
        call = response.tool_calls[0]
        tool_result = calculate.invoke(call["args"])
        # Show the tool's result back to the model so it can form the final answer
        messages.append(AIMessage(content=f"Tool result: {tool_result}"))
        final_text_response = llm.invoke(messages).content
    else:
        final_text_response = response.content

    # Step D: Convert this final text into structured format
    structured_llm = llm.with_structured_output(StudySummary)
    summary = structured_llm.invoke(
        f"Question: {question}\nAnswer: {final_text_response}\n"
        f"Summarize this as topic, answer, and difficulty."
    )
    return summary


if __name__ == "__main__":
    # Simple conversation history (in a real app this would come from a database/session)
    history = []

    questions = [
        "What is the Pythagorean theorem?",
        "If a right triangle has legs 6 and 8, what is the hypotenuse? (use calculate tool: 6**2 + 8**2 then square root manually if needed)",
    ]

    for q in questions:
        print(f"\n===== Student asks: {q} =====")
        result = run_study_agent(q, history)

        print("----- Structured Summary -----")
        print(f"Topic     : {result.topic}")
        print(f"Answer    : {result.answer}")
        print(f"Difficulty: {result.difficulty}")

        # Update the conversation history so the next question keeps context
        history.append(HumanMessage(content=q))
        history.append(AIMessage(content=result.answer))

# ==========================================================
# CONGRATULATIONS! In this project, you learned:
#   - Building prompts with templates and composition
#   - Guiding the model with few-shot examples and example selectors
#   - Multi-step workflows with chaining and pipelines (LCEL)
#   - "Acting" agents with tools, ReAct, and an agent scratchpad
#   - Better reasoning with Chain-of-Thought and Tree-of-Thought
#   - Improving output quality with self-reflection
#   - Getting reliable, code-friendly results with structured output
#
# Next step: go to the "assignments/" folder and practice on
# your own, then compare your work with "solutions/".
# ==========================================================
