# ==========================================================
# Assignment 01: PromptTemplate Practice
# --------------------------------------------------
# TASK:
# Create a PromptTemplate that takes two variables:
#   - "language"  (e.g. "French", "Urdu", "Spanish")
#   - "sentence"  (the sentence to translate)
#
# Write a template that tells the model:
#   "Translate the following sentence into {language}: {sentence}"
#
# Then use this template to translate "Hello, how are you?"
# into "French".
#
# HINT: See file "01_prompt_template.py" in this repo.
# ==========================================================

from langchain.prompts import PromptTemplate
from llm_config import llm

# TODO 1: Build a PromptTemplate (input_variables + template)
prompt = None  # <-- write your code here

# TODO 2: Call prompt.format(...) to build the final_prompt

# TODO 3: Call llm.invoke(final_prompt) and print the response

print("Complete the TODOs above to finish this assignment!")
