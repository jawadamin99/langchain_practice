# ==========================================================
# 01_prompt_template.py
#
# CONCEPT: PromptTemplate
# --------------------------------------------------
# A PromptTemplate is a "reusable text mold" where we leave
# {variables} as placeholders. At runtime, we substitute
# these variables with actual values.
#
# Benefit: Instead of writing a new prompt every time, we
# create one template and just swap out the data.
# ==========================================================

from langchain.prompts import PromptTemplate
from llm_config import llm

# Step 1: Create a template -> {topic} is a placeholder/variable
template_text = "Explain the concept of {topic} in simple words for a beginner."

prompt = PromptTemplate(
    input_variables=["topic"],   # tells the template which variables it has
    template=template_text,
)

# Step 2: "Format" the template with values -> produces the real prompt
final_prompt = prompt.format(topic="Recursion")
print("----- Generated Prompt -----")
print(final_prompt)

# Step 3: Send this generated prompt to the LLM
response = llm.invoke(final_prompt)

print("\n----- LLM Response -----")
print(response.content)

# TIP: The same template can be reused with multiple topics:
# prompt.format(topic="Machine Learning")
# prompt.format(topic="Blockchain")
