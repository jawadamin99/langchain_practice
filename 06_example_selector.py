# ==========================================================
# 06_example_selector.py
#
# CONCEPT: Example Selector
# --------------------------------------------------
# If we have a lot of examples (like 100+), we can't put ALL
# of them in the prompt (token limit + cost + noise). An
# Example Selector picks only the "most relevant" examples
# based on similarity to the new input.
#
# Here we use LengthBasedExampleSelector (simple, doesn't
# need embeddings) which selects more or fewer examples
# depending on the prompt's length.
# ==========================================================

from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector
from llm_config import llm

# Step 1: A larger set of examples (dataset)
examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "tall", "antonym": "short"},
    {"word": "fast", "antonym": "slow"},
    {"word": "big", "antonym": "small"},
    {"word": "hot", "antonym": "cold"},
    {"word": "light", "antonym": "dark"},
]

example_template = PromptTemplate(
    input_variables=["word", "antonym"],
    template="Word: {word}\nAntonym: {antonym}",
)

# Step 2: Build the selector -> it decides how many examples will fit
example_selector = LengthBasedExampleSelector(
    examples=examples,
    example_prompt=example_template,
    max_length=25,   # approximate total length (in words) allowed
)

# Step 3: Use "example_selector=" instead of "examples=" in FewShotPromptTemplate
dynamic_prompt = FewShotPromptTemplate(
    example_selector=example_selector,   # <-- dynamic selector instead of a fixed list
    example_prompt=example_template,
    prefix="Give the antonym (opposite) of each word.",
    suffix="Word: {input_word}\nAntonym:",
    input_variables=["input_word"],
)

final_prompt = dynamic_prompt.format(input_word="strong")
print("----- Prompt with Examples Chosen by the Selector -----")
print(final_prompt)

response = llm.invoke(final_prompt)
print("\n----- LLM Response -----")
print(response.content)

# LESSON: When the input is short, the selector can fit more
# examples. When the input is long, fewer examples are
# selected so the total length doesn't exceed the limit.
