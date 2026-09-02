# ==========================================================
# 05_few_shot_prompt.py
#
# CONCEPT: Few-Shot Prompting
# --------------------------------------------------
# Few-shot prompting means: we show the model a few examples
# (input -> output pairs) to teach it the task, then ask our
# real question.
#
# This helps the model learn the pattern and give more
# accurate/consistent answers (better than zero-shot).
# ==========================================================

from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from llm_config import llm

# Step 1: Define a few examples (input -> output)
examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "tall", "antonym": "short"},
    {"word": "fast", "antonym": "slow"},
]

# Step 2: Template for how each example should be formatted
example_template = PromptTemplate(
    input_variables=["word", "antonym"],
    template="Word: {word}\nAntonym: {antonym}",
)

# Step 3: Build the FewShotPromptTemplate that joins examples + new question
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="Give the antonym (opposite) of each word.",  # instructions on top
    suffix="Word: {input_word}\nAntonym:",                # the real question at the bottom
    input_variables=["input_word"],
)

final_prompt = few_shot_prompt.format(input_word="strong")
print("----- Generated Few-Shot Prompt -----")
print(final_prompt)

response = llm.invoke(final_prompt)
print("\n----- LLM Response -----")
print(response.content)  # Expected: "weak" (learned from the pattern)
