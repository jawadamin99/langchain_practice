# ==========================================================
# 08_prompt_composition.py
#
# CONCEPT: Prompt Composition
# --------------------------------------------------
# Breaking big prompts into small reusable "pieces" (blocks),
# then combining (joining) them into one final big prompt.
#
# Benefit: We can test/reuse each piece separately, like
# joining LEGO blocks together.
# ==========================================================

from langchain_core.prompts import PromptTemplate
from config.llm_config import llm

# Step 1: Create small text pieces (blocks)
persona_block = "You are an expert {role}."
task_block = "Your task is to {task}."
format_block = "Respond in {format} format."

# Step 2: Join them (compose) into one big template
full_template_text = "\n".join([persona_block, task_block, format_block])

composed_prompt = PromptTemplate(
    input_variables=["role", "task", "format"],
    template=full_template_text,
)

# Step 3: Use the combined template by providing values
final_prompt = composed_prompt.format(
    role="nutritionist",
    task="suggest a healthy breakfast",
    format="a bullet point list",
)

print("----- Composed Prompt -----")
print(final_prompt)

response = llm.invoke(final_prompt)
print("\n----- LLM Response -----")
print(response.content)

# LESSON: Composition makes it easier to manage large,
# complex prompts -> each block has its own responsibility.
