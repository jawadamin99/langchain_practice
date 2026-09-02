# ==========================================================
# 17_chain_of_thought.py
#
# CONCEPT: Chain-of-Thought (CoT) Prompting
# --------------------------------------------------
# When we ask the model to "just give the final answer", it
# sometimes rushes and gives a wrong answer (especially on
# math/logic questions). Chain-of-Thought prompting tells the
# model to "think step by step" -> this significantly
# improves accuracy.
# ==========================================================

from langchain.prompts import PromptTemplate
from llm_config import llm

question = (
    "A shop had 120 apples. They sold 45 in the morning and "
    "38 in the afternoon. How many apples are left?"
)

# ---- Without Chain-of-Thought (direct answer) ----
direct_prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer this question directly with just the number: {question}",
)

direct_response = llm.invoke(direct_prompt.format(question=question))
print("----- Without Chain-of-Thought -----")
print(direct_response.content)

# ---- With Chain-of-Thought ----
cot_prompt = PromptTemplate(
    input_variables=["question"],
    # "Let's think step by step" -> the magic phrase that
    # triggers the model to reason
    template="{question}\nLet's think step by step.",
)

cot_response = llm.invoke(cot_prompt.format(question=question))
print("\n----- With Chain-of-Thought -----")
print(cot_response.content)

# LESSON: Phrases like "Let's think step by step" push the
# model to write out intermediate reasoning steps, which
# increases accuracy on complex problems.
