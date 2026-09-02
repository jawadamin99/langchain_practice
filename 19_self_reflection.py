# ==========================================================
# 19_self_reflection.py
#
# CONCEPT: Self-Reflection Prompting
# --------------------------------------------------
# Self-reflection means: get an initial answer from the
# model, then show that answer back to the model and ask
# "review this answer, is there any mistake or gap?" and
# have it improve the answer.
#
# This lets the model catch its own mistakes and give a
# better final answer — like a person reviewing their own
# work again.
# ==========================================================

from langchain.prompts import PromptTemplate
from llm_config import llm

question = "Write a short paragraph explaining why the sky is blue."

# ---- Step 1: Generate a first (draft) answer ----
draft_prompt = PromptTemplate(
    input_variables=["question"],
    template="{question}",
)
draft_answer = llm.invoke(draft_prompt.format(question=question)).content

print("----- Step 1: Draft Answer -----")
print(draft_answer)

# ---- Step 2: Have the model critique its own answer ----
critique_prompt = PromptTemplate(
    input_variables=["question", "draft"],
    template=(
        "Question: {question}\n"
        "Draft Answer: {draft}\n\n"
        "Critique this answer: is it accurate, clear, and complete? "
        "List any issues or missing points."
    ),
)
critique = llm.invoke(
    critique_prompt.format(question=question, draft=draft_answer)
).content

print("\n----- Step 2: Self-Critique -----")
print(critique)

# ---- Step 3: Generate an improved final answer based on the critique ----
improve_prompt = PromptTemplate(
    input_variables=["question", "draft", "critique"],
    template=(
        "Question: {question}\n"
        "Draft Answer: {draft}\n"
        "Critique: {critique}\n\n"
        "Now rewrite an improved, final answer that fixes the issues mentioned."
    ),
)
final_answer = llm.invoke(
    improve_prompt.format(question=question, draft=draft_answer, critique=critique)
).content

print("\n----- Step 3: Final Improved Answer -----")
print(final_answer)

# LESSON: The self-reflection loop (Draft -> Critique ->
# Improve) noticeably increases output quality, especially
# for writing and reasoning tasks.
