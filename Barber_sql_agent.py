from dotenv import load_dotenv

load_dotenv()
import sqlite3

from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from config.llm_config import llm

# =====================================================
# 1. SQL DATABASE
#    Long-Term Memory
# =====================================================

db = sqlite3.connect("barber.db", check_same_thread=False)

# Pre Defined Schema (table name, column name, and Data types)
db.execute("""
           CREATE TABLE IF NOT EXISTS customers
           (
               id
               INTEGER
               PRIMARY
               KEY
               AUTOINCREMENT,
               name
               TEXT
               UNIQUE,
               favorite_service
               TEXT
           )
           """)

db.commit()

db.execute("""
           CREATE TABLE IF NOT EXISTS conversations
           (
               id
               INTEGER
               PRIMARY
               KEY
               AUTOINCREMENT,
               thread_id
               TEXT,
               role
               TEXT,
               content
               TEXT
           )
           """)

db.commit()


# Save customer in SQL
def save_message(thread_id:str, role:str, content:str):
    db.execute(
        "INSERT INTO conversations (thread_id, role, content) VALUES (?, ?, ?)",
        (thread_id, role, content)
    )
    db.commit()

@tool
def save_customer(name:str, service:str):
    """Save or update a customer's favorite service."""
    db.execute(
        """
        INSERT OR REPLACE INTO customers
        (name, favorite_service)
        VALUES (?, ?)
        """,
        (name, service)
    )
    db.commit()
    return f"Saved {name}'s favorite service as {service}."

# Get customer from SQL
@tool
def get_customer(name:str):
    """Look up a customer's saved favorite service."""
    result = db.execute(
        """
        SELECT name, favorite_service
        FROM customers
        WHERE name = ?
        """,
        (name,)
    ).fetchone()

    if not result:
        return f"No saved record found for {name}."

    return f"{result[0]}'s favorite service is {result[1]}."


# =====================================================
# 2. TOOL
# =====================================================

@tool
def get_service_price(service: str):
    """
    Get the price of a barber shop service.
    """

    prices = {
        "haircut": "$35",
        "fade": "$40",
        "beard": "$20",
        "haircut and beard": "$55",
        "haircut , beard and fade": "$75"
    }

    price = prices.get(service.lower())

    if price:
        return f"{service.title()} costs {price}."

    return "Sorry, price for this service is not available."


# =====================================================
# 3. PROMPT ENGINEERING
# =====================================================

SYSTEM_PROMPT = """
You are a friendly AI receptionist for a USA barber shop.

Your responsibilities:

1. Answer customer questions.
2. Give service prices using the available tool.
3. Be short and professional.
4. Never invent prices.
5. Remember information during the current conversation.
6. If a customer tells you their name and favorite service, save it using the save tool.
7. If a customer asks what you remember about them, use the lookup tool.
"""

# =====================================================
# 4. GEMINI
# =====================================================
# imported llm from config.llm_config

# =====================================================
# 5. SHORT-TERM MEMORY
# =====================================================

memory = MemorySaver()

agent = create_agent(
    model=llm,
    tools=[get_service_price, save_customer, get_customer],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory
)

# =====================================================
# 6. CHAT CONFIGURATION
# =====================================================
thread_id = "customer_001"
config = {
    "configurable": {
        "thread_id": thread_id
    }
}

# =====================================================
# 7. CHAT LOOP
# =====================================================

print("\n===================================")
print("     AI BARBER RECEPTIONIST")
print("===================================")
#save_customer("Awais Sheikh", "Hair cut")
while True:

    user_input = input("\nCustomer: ")

    if user_input.lower() == "exit":
        break

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config=config
    )

    answer = response["messages"][-1].text

    save_message(thread_id, "user", user_input)
    save_message(thread_id, "assistant", answer)

    print("\nAI:", answer)
