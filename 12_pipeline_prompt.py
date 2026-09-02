# ==========================================================
# 12_pipeline_prompt.py
#
# CONCEPT: Pipeline / LCEL (LangChain Expression Language)
# --------------------------------------------------
# In LangChain, we can use the "|" (pipe operator) to join
# steps into a chain/pipeline — just like Unix pipes (the
# output of one step automatically becomes the input of the
# next).
#
# This does the same thing as "11_prompt_chaining.py", but
# instead of manual invoke() calls, LangChain handles the
# chaining of steps for us -> cleaner and more production-ready.
# ==========================================================

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.llm_config import llm

# Step 1: Build a prompt template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write a two-line poem about {topic}.",
)

# Step 2: Output parser -> extracts just the text (string) from
# the LLM's raw response object
output_parser = StrOutputParser()

# Step 3: Build the pipeline -> prompt -> llm -> parser
# CONCEPT: The "|" operator turns one step's output into the next step's input
pipeline = prompt | llm | output_parser

# Step 4: Run the pipeline in a single call
result = pipeline.invoke({"topic": "the ocean"})

print("----- Pipeline Result -----")
print(result)

# LESSON: This "chain" is the core idea of LangChain. It's
# also called a "Runnable", and it can be used with
# streaming, batching, and async as well.
