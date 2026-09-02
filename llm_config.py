# ==========================================================
# llm_config.py
#
# CONCEPT:
# This file creates a shared/reusable LLM object that every
# example file (01_*.py through 20_*.py) imports and uses.
# This means we don't have to repeat API key and model setup
# in every single file -> DRY principle (Don't Repeat Yourself).
# ==========================================================

import os
from dotenv import load_dotenv          # To read the .env file
from langchain_openai import ChatOpenAI  # OpenAI chat model wrapper

# Step 1: Load environment variables from the .env file
# (this puts OPENAI_API_KEY into os.environ)
load_dotenv()

# Step 2: A helper function that returns an LLM object
def get_llm(model_name: str = "gpt-4o-mini", temperature: float = 0.7):
    """
    CONCEPT: temperature
    - 0.0  -> deterministic, always gives predictable/same answers
    - 1.0+ -> creative, more random, different answers each time

    model_name: which OpenAI model to use
    """
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

# Also create a default llm instance for direct import
llm = get_llm()

if __name__ == "__main__":
    # This block only runs when the file is executed directly
    # (not when imported) -> a standard Python pattern
    response = llm.invoke("Say hello in one short sentence.")
    print(response.content)
