# ==========================================================
# Solution 02: Few-Shot Prompting Practice
# ==========================================================

from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from llm_config import llm

examples = [
    {"text": "I love this product!", "sentiment": "Positive"},
    {"text": "This is terrible.", "sentiment": "Negative"},
    {"text": "It's okay, nothing special.", "sentiment": "Neutral"},
]

example_prompt = PromptTemplate(
    input_variables=["text", "sentiment"],
    template="Text: {text}\nSentiment: {sentiment}",
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Classify the sentiment of each text as Positive, Negative, or Neutral.",
    suffix="Text: {input_text}\nSentiment:",
    input_variables=["input_text"],
)

final_prompt = few_shot_prompt.format(
    input_text="The delivery was super fast and the packaging was great!"
)
print("----- Generated Prompt -----")
print(final_prompt)

response = llm.invoke(final_prompt)
print("\n----- LLM Response -----")
print(response.content)  # Expected: Positive
