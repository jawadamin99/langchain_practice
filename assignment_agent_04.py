import random
import re

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from config.assignment_helper import AssignmentHelper
from config.llm_config import llm

assignment_helper = AssignmentHelper()

load_dotenv()


system_prompt = """
You are a Campaign Strategy Assistant.

Your job is to help create a basic digital marketing campaign.

Rules:
- Keep the response simple.
- Use the client details given in the prompt.
- Use the ad metrics tool before making the final plan.
- Give one ad copy for each suggested platform.
"""


@tool
def get_ad_metrics(platform: str):
    """Return simple mock ad metrics for a platform."""
    platform = platform.lower().strip()

    if platform == "facebook":
        return {
            "reach": "15,000 people",
            "cpc": "$0.80",
            "audience_size": "large local audience"
        }

    if platform == "instagram":
        return {
            "reach": "12,000 people",
            "cpc": "$0.95",
            "audience_size": "young visual audience"
        }

    if platform == "google search":
        return {
            "reach": "8,000 people",
            "cpc": "$1.20",
            "audience_size": "high intent search audience"
        }

    return {
        "reach": "unknown",
        "cpc": "unknown",
        "audience_size": "unknown"
    }


memory = MemorySaver()

agent = create_agent(
    model=llm,
    tools=[get_ad_metrics],
    system_prompt=system_prompt,
    checkpointer=memory
)


def ask_llm(thread_id, prompt):
    response = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        config={"configurable": {"thread_id": thread_id}}
    )
    assignment_helper.save_message(thread_id,"campaign_bot","user",prompt)

    return response["messages"][-1].text


def get_budget_number(budget_text):
    numbers = re.findall(r"\d+", budget_text.replace(",", ""))
    if numbers:
        return int(numbers[0])
    return 1000


def choose_platforms(goal_text):
    goal_text = goal_text.lower()

    if "awareness" in goal_text:
        return ["Facebook", "Instagram"]

    if "sales" in goal_text or "lead" in goal_text:
        return ["Google Search", "Facebook"]

    return ["Facebook", "Instagram", "Google Search"]


def split_budget(total_budget, platforms):
    result = {}

    if len(platforms) == 2:
        result[platforms[0]] = int(total_budget * 0.60)
        result[platforms[1]] = total_budget - result[platforms[0]]
    elif len(platforms) == 3:
        result[platforms[0]] = int(total_budget * 0.40)
        result[platforms[1]] = int(total_budget * 0.35)
        result[platforms[2]] = total_budget - result[platforms[0]] - result[platforms[1]]
    else:
        result[platforms[0]] = total_budget

    return result


def make_ad_copy(thread_id, platform, business_type, audience, goal):
    prompt = f"""
Write one short ad copy.

Platform: {platform}
Business type: {business_type}
Target audience: {audience}
Goal: {goal}
"""

    return ask_llm(thread_id, prompt)

thread_id = assignment_helper.generate_thread_id()

print("===================================")
print(" CAMPAIGN STRATEGY ASSISTANT")
print("===================================")
print("Answer the questions.")
print("===================================")

business_type = input("\nWhat is the business type? ")
target_audience = input("Who is the target audience? ")
budget = input("What is the marketing budget? ")
marketing_goals = input("What are the marketing goals? ")

total_budget = get_budget_number(budget)
platforms = choose_platforms(marketing_goals)
budget_split = split_budget(total_budget, platforms)

print("\nGenerating campaign plan...\n")

print("===================================")
print(" FINAL CAMPAIGN SUMMARY")
print("===================================")
print("Business Type   :", business_type)
print("Target Audience :", target_audience)
print("Budget          :", budget)
print("Marketing Goals :", marketing_goals)

print("\nRecommended Platforms:")
for platform in platforms:
    print("-", platform)

print("\nBudget Split:")
for platform in platforms:
    print("-", platform, ":", "$" + str(budget_split[platform]))

print("\nEstimated Metrics:")
for platform in platforms:
    metrics = get_ad_metrics.invoke(platform)
    print("-", platform)
    print("  Reach:", metrics["reach"])
    print("  CPC:", metrics["cpc"])
    print("  Audience Size:", metrics["audience_size"])

print("\nSample Ad Copy:")
for platform in platforms:
    ad_copy = make_ad_copy(
        thread_id,
        platform,
        business_type,
        target_audience,
        marketing_goals
    )
    print("-", platform + ":", ad_copy)

    assignment_helper.save_message(
        thread_id,
        "campaign_bot",
        "assistant",
        ad_copy)

print("\nStrategy Explanation:")
print("This campaign uses the selected platforms based on the client's goals.")
print("The budget is divided across the platforms to improve reach and results.")
