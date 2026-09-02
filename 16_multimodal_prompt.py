# ==========================================================
# 16_multimodal_prompt.py
#
# CONCEPT: Multimodal Prompting
# --------------------------------------------------
# "Multimodal" means the model can understand not just text,
# but also images (or audio/video). We can send both text and
# an image together in a single message.
#
# NOTE: This requires a vision-capable model (e.g., gpt-4o /
# gpt-4o-mini) and a valid image URL/base64.
# ==========================================================

from langchain_core.messages import HumanMessage
from llm_config import llm

# Step 1: Build a message where "content" is a LIST -
# both a text block and an image block
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/640px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"

message = HumanMessage(
    content=[
        {"type": "text", "text": "What is shown in this image? Describe it briefly."},
        {"type": "image_url", "image_url": {"url": image_url}},
    ]
)

# Step 2: Send it to the model (must be vision-capable)
response = llm.invoke([message])

print("----- Multimodal Response -----")
print(response.content)

# LESSON: A multimodal prompt's structure differs from a
# normal text prompt -> "content" is a list that can contain
# different "type" blocks (text, image_url, etc.).
