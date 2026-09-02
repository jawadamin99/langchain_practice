from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
import sqlite3

from config.assignment_helper import AssignmentHelper
from config.llm_config import llm
import random
import pandas as pd

assignment_helper = AssignmentHelper()
load_dotenv()

@tool
def search_properties(budget:int,location:str,property_type:str,bedrooms:int):
    """ Search properties based on a budget, location, and property type."""
    df = pd.read_csv("agentic_data/properties_data.csv")
    matches = df.copy()

    if budget is not None:
        matches = matches[matches["price"] <= budget]

    if location:
        matches = matches[matches["location"].str.contains(location, case=False, na=False)]

    if property_type:
        matches = matches[matches["property_type"].str.lower() == property_type.lower()]

    if bedrooms is not None:
        matches = matches[matches["bedrooms"] >= bedrooms]
    return matches.to_dict(orient="records")

system_prompt = f"""
You are an AI Property Recommendation Assistant.

Your job is to help users find suitable properties based on their preferences.

You should collect and remember the following preferences during the conversation:

- Budget
- Preferred location
- Property type
- Number of bedrooms

Conversation rules:

- Ask only for information that is still missing.
- Do not ask again for preferences the user has already provided.
- If the user changes a preference later, treat the newest value as the current preference.
- Refine recommendations whenever the user updates their requirements.
- Ask one or a small number of questions at a time.
- If the user gives multiple preferences in one message, extract and remember all of them.

Recommendation rules:

- Only recommend properties returned from the provided property dataset or property-search tool.
- Never invent property names, prices, locations, features, or availability.
- If no properties match the user's current preferences, clearly say that no exact matches were found.
- If appropriate, ask whether the user wants to relax one of their filters.
- Present matching properties clearly with:
  property name,
  price,
  location,
  property type,
  bedrooms,
  and key features.

Preference updates:

- The latest stated preference overrides an older one.
- For example, if the user first says the budget is 2 crore and later changes it to 2.5 crore, use 2.5 crore from that point onward.
- Do not reset other preferences when only one preference changes.

Stay focused on property recommendation and property-search assistance.
"""

thread_id = assignment_helper.generate_thread_id()

memory = MemorySaver()

agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    checkpointer=memory,
    tools=[search_properties]
)


print("\n===================================")
print("     AI Property Recommendation Assistant")
print("===================================")
print("     Type 'exit' to end chat.")
print("===================================")
config = {
    "configurable":{
        "thread_id": thread_id
    }
}
while True:
    user_input = input("\nUser: ")
    if user_input.lower() == "exit":
        print("\n It was nice talking to you... Take Care!!!")
        break
    if not user_input:
        continue

    assignment_helper.save_message(str(thread_id),'property_bot','user',user_input)
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config = config
    )

    answer = response["messages"][-1].text
    assignment_helper.save_message(str(thread_id),'property_bot','assistant',answer)
    print("\nAI:", answer)
