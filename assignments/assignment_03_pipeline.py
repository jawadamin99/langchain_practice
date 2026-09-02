# ==========================================================
# Assignment 03: LCEL Pipeline Practice
# --------------------------------------------------
# TASK:
# Build a pipeline that:
#   1. Takes a PromptTemplate with a "{product}" variable that asks:
#      "Suggest a catchy slogan for {product}."
#   2. Calls the LLM
#   3. Uses StrOutputParser to extract just the text
#
# Then chain these three together using the "|" operator and
# test it with product="eco-friendly water bottle".
#
# HINT: See file "12_pipeline_prompt.py" in this repo.
# ==========================================================

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_config import llm

# TODO 1: Build the prompt template

# TODO 2: Build the output_parser (StrOutputParser)

# TODO 3: pipeline = prompt | llm | output_parser

# TODO 4: Call pipeline.invoke({"product": "eco-friendly water bottle"})

print("Complete the TODOs above to finish this assignment!")
