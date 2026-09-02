# ==========================================================
# 11_prompt_chaining.py
#
# CONCEPT: Prompt Chaining
# --------------------------------------------------
# Sometimes a single prompt can't finish the whole task.
# "Chaining" means: the OUTPUT of one prompt becomes the
# INPUT of the next prompt -> breaking a complex task into
# small steps (like an assembly line).
#
# Example: First generate an idea, then expand it into a
# full story.
# ==========================================================

from langchain_core.prompts import PromptTemplate
from llm_config import llm

# ---- Step 1: First prompt -> generate an idea ----
idea_prompt = PromptTemplate(
    input_variables=["genre"],
    template="Give me one creative story idea in the {genre} genre. Just one sentence.",
)

idea_chain_input = idea_prompt.format(genre="science fiction")
idea_output = llm.invoke(idea_chain_input).content
print("----- Step 1 Output (Idea) -----")
print(idea_output)

# ---- Step 2: Second prompt -> use the first output as input to write a story ----
story_prompt = PromptTemplate(
    input_variables=["idea"],
    template="Write a short 3-sentence story based on this idea: {idea}",
)

story_chain_input = story_prompt.format(idea=idea_output)  # <-- chaining happens here
story_output = llm.invoke(story_chain_input).content

print("\n----- Step 2 Output (Story, based on Step 1) -----")
print(story_output)

# LESSON: Chaining lets us break complex tasks into multiple
# simple steps, where each step depends on the result of the
# previous one.
