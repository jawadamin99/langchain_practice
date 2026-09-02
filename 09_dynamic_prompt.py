# ==========================================================
# 09_dynamic_prompt.py
#
# CONCEPT: Dynamic Prompts
# --------------------------------------------------
# A dynamic prompt is one whose SHAPE changes on its own at
# runtime based on conditions/logic — meaning Python code
# builds the prompt instead of using a static template.
#
# Example: Generating a different kind of prompt depending
# on the user's experience level (beginner or expert).
# ==========================================================

from config.llm_config import llm

def build_dynamic_prompt(topic: str, level: str) -> str:
    """
    CONCEPT: This function "composes" the prompt itself
    based on a condition -> this is exactly what dynamic
    prompting means.
    """
    if level == "beginner":
        instruction = "Explain in very simple words, avoid jargon, use an analogy."
    elif level == "expert":
        instruction = "Explain with technical depth, assume strong background knowledge."
    else:
        instruction = "Explain in a balanced, moderately detailed way."

    prompt = f"Topic: {topic}\nInstruction: {instruction}\nExplanation:"
    return prompt

# Step 1: Generate different prompts for different users based on level
for level in ["beginner", "expert"]:
    prompt = build_dynamic_prompt("Neural Networks", level)
    print(f"----- Prompt for level='{level}' -----")
    print(prompt)

    response = llm.invoke(prompt)
    print("\n----- LLM Response -----")
    print(response.text)
    print("\n" + "=" * 50 + "\n")

# LESSON: In dynamic prompting we can use Python's if/else,
# loops, or user data (profile, history) to "personalize"
# the prompt.
