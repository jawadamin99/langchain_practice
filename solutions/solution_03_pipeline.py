# ==========================================================
# Solution 03: LCEL Pipeline Practice
# ==========================================================

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_config import llm

prompt = PromptTemplate(
    input_variables=["product"],
    template="Suggest a catchy slogan for {product}.",
)

output_parser = StrOutputParser()

pipeline = prompt | llm | output_parser

result = pipeline.invoke({"product": "eco-friendly water bottle"})

print("----- Pipeline Result -----")
print(result)
