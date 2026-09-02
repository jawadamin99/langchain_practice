# ==========================================================
# 07_partial_prompt.py
#
# CONCEPT: Partial Prompt Templates
# --------------------------------------------------
# Sometimes our template has variables that are "always
# fixed" (like the current date, app name, or user's
# language) and other variables that "change every time"
# (like the user's question).
#
# "Partializing" means: fill in the fixed variables ahead
# of time, and keep a "smaller template" for the rest.
# ==========================================================

from datetime import date
from langchain_core.prompts import PromptTemplate
from config.llm_config import llm

# Step 1: Full template - with two variables
template = PromptTemplate(
    input_variables=["today", "question"],
    template="Today's date is {today}. Answer the user's question: {question}",
)

# Step 2: Permanently fix "today" (partial)
partial_template = template.partial(today=str(date.today()))

# Now partial_template only needs "question", not "today"
print("Remaining variables needed:", partial_template.input_variables)

# Step 3: Now just provide the question to use it (no need to pass
# the date every time)
final_prompt = partial_template.format(question="What day of the week is it?")
print("\n----- Generated Prompt -----")
print(final_prompt)

response = llm.invoke(final_prompt)
print("\n----- LLM Response -----")
print(response.content)

# LESSON: Partial prompts keep the code clean -> we don't
# need to pass repeated/fixed values over and over.
