# ==========================================================
# Assignment 02: Few-Shot Prompting Practice
# --------------------------------------------------
# TASK:
# Build a few-shot prompt for "sentiment classification".
# Your examples should look something like this:
#
#   Text: "I love this product!"      -> Sentiment: Positive
#   Text: "This is terrible."         -> Sentiment: Negative
#   Text: "It's okay, nothing special" -> Sentiment: Neutral
#
# Then use this prompt to classify a new text:
#   "The delivery was super fast and the packaging was great!"
#
# HINT: See file "05_few_shot_prompt.py" in this repo.
# ==========================================================

from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from llm_config import llm

# TODO 1: Build the examples list (dicts with "text" and "sentiment")
examples = []  # <-- write your code here

# TODO 2: Build the example_prompt (PromptTemplate) that formats
# "text" and "sentiment"

# TODO 3: Build the FewShotPromptTemplate (with prefix/suffix)

# TODO 4: Generate the final prompt for the new text and send it to the LLM

print("Complete the TODOs above to finish this assignment!")
