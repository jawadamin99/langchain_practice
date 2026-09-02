# ==========================================================
# 18_tree_of_thought.py
#
# CONCEPT: Tree-of-Thought (ToT) Prompting
# --------------------------------------------------
# In Chain-of-Thought (file 17), the model reasons along a
# SINGLE path (linear). In Tree-of-Thought, we have the model
# generate MULTIPLE different solutions/paths (like branches
# of a tree), then COMPARE them to choose the best one.
#
# This technique works well for complex/creative problems
# where more than one approach is possible.
# ==========================================================

from langchain.prompts import PromptTemplate
from llm_config import llm

problem = "How can a small bakery increase its sales without spending much money on advertising?"

# ---- Step 1: Generate multiple different "branches" (solutions) ----
branch_prompt = PromptTemplate(
    input_variables=["problem"],
    template=(
        "Problem: {problem}\n"
        "Generate 3 different possible solutions (label them A, B, C). "
        "Keep each solution to 1-2 sentences."
    ),
)

branches_response = llm.invoke(branch_prompt.format(problem=problem)).content
print("----- Step 1: Multiple Branches (Tree) -----")
print(branches_response)

# ---- Step 2: Have the model itself evaluate/compare these branches ----
evaluate_prompt = PromptTemplate(
    input_variables=["problem", "branches"],
    template=(
        "Problem: {problem}\n\n"
        "Here are 3 candidate solutions:\n{branches}\n\n"
        "Evaluate each solution's pros and cons briefly, "
        "then pick the BEST one and explain why."
    ),
)

final_response = llm.invoke(
    evaluate_prompt.format(problem=problem, branches=branches_response)
).content

print("\n----- Step 2: Evaluation & Best Choice -----")
print(final_response)

# LESSON: Tree-of-Thought = "generate many options" + "compare
# and pick the best" -> this makes the model's decision-making
# more thoughtful and robust, especially for open-ended problems.
