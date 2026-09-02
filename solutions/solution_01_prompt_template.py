# ==========================================================
# Solution 01: PromptTemplate Practice
# ==========================================================

from langchain_core.prompts import PromptTemplate
from config.llm_config import llm

prompt = PromptTemplate(
    input_variables=["language", "sentence"],
    template="Translate the following sentence into {language}: {sentence}",
)

final_prompt = prompt.format(language="French", sentence="Hello, how are you?")
print("----- Generated Prompt -----")
print(final_prompt)

response = llm.invoke(final_prompt)
print("\n----- LLM Response -----")
print(response.text)
