# ==========================================================
# 10_structured_output.py
#
# CONCEPT: Structured Output
# --------------------------------------------------
# LLMs normally return free-form text. But if we want to use
# the result in code (e.g., save it to a database), we need
# "structured" data — like a Python object/JSON, not just a
# plain paragraph.
#
# Pydantic + LangChain's "with_structured_output" solves this
# problem: we define a "schema" (blueprint), and the model
# returns its answer in that exact shape.
# ==========================================================

from pydantic import BaseModel, Field
from llm_config import llm

# Step 1: Define the "shape" (schema) of the output using a Pydantic class
class MovieReview(BaseModel):
    title: str = Field(description="Name of the movie")
    rating: int = Field(description="Rating out of 10")
    summary: str = Field(description="One-line summary of the review")

# Step 2: "Bind" the LLM to this schema
structured_llm = llm.with_structured_output(MovieReview)

# Step 3: Ask a normal question, but the answer comes back as a structured object
result = structured_llm.invoke(
    "Give a short review of the movie 'Inception' with a rating."
)

print("----- Structured Output (Python Object) -----")
print(result)
print("\nAccessing fields individually:")
print("Title  :", result.title)
print("Rating :", result.rating)
print("Summary:", result.summary)

# LESSON: Structured output lets us make an LLM behave like a
# reliable "API" -> we can directly use result.title,
# result.rating, etc., further in our code.
