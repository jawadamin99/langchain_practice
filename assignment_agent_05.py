import json
import random

from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from config.assignment_helper import AssignmentHelper
from config.llm_config import llm

assignment_helper = AssignmentHelper()
load_dotenv()


system_prompt = """
You are an AI Waiter.

Rules:
- Use only the given restaurant menu.
- Do not invent items or prices.
- Be short, polite, and simple.
- Help with adding items, removing items, substitutions, allergies, and checkout.
"""


memory = MemorySaver()

agent = create_agent(
    model=llm,
    tools=[],
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

    last_message = response["messages"][-1]
    if hasattr(last_message, "text") and last_message.text:
        return last_message.text
    return str(last_message.content)


def load_menu():
   menu = {
  "items": [
    {
      "name": "zinger burger",
      "price": 500,
      "spice_levels": ["mild", "medium", "hot"],
      "substitutions": ["no mayo", "extra cheese"],
      "allergy_notes": "contains gluten and dairy",
      "in_stock": 1
    },
    {
      "name": "chicken biryani",
      "price": 350,
      "spice_levels": ["mild", "medium", "hot"],
      "substitutions": ["less spice"],
      "allergy_notes": "contains dairy",
      "in_stock": 1
    },
    {
      "name": "fries",
      "price": 200,
      "spice_levels": ["regular"],
      "substitutions": ["no masala"],
      "allergy_notes": "may contain traces of gluten",
      "in_stock": 1
    },
    {
      "name": "soft drink",
      "price": 150,
      "spice_levels": ["none"],
      "substitutions": ["no ice"],
      "allergy_notes": "no major allergy warning",
      "in_stock": 1
    },
    {
      "name": "chicken burger combo",
      "price": 800,
      "spice_levels": ["mild", "medium", "hot"],
      "substitutions": ["no mayo", "no ice"],
      "allergy_notes": "contains gluten and dairy",
      "in_stock": 1,
      "combo_items": ["zinger burger", "fries", "soft drink"],
      "combo_discount": 50
    }
  ]
}
   return menu


def find_item(menu_items, item_name):
    for item in menu_items:
        if item["name"] == item_name:
            return item
    return None


def calculate_total(cart, menu_items):
    total = 0

    for item in cart:
        total += item["price"]

    names = []
    for item in cart:
        names.append(item["name"])

    combo = find_item(menu_items, "chicken burger combo")
    if combo:
        combo_items = combo["combo_items"]
        if all(combo_item in names for combo_item in combo_items):
            total = total - combo["combo_discount"]

    return total


def show_menu(menu_items):
    print("\n========== MENU ==========")
    for item in menu_items:
        print(item["name"].title(), "- Rs.", item["price"])
        print("Spice Levels:", ", ".join(item["spice_levels"]))
        print("Substitutions:", ", ".join(item["substitutions"]))
        print("Allergy Notes:", item["allergy_notes"])
        if "combo_discount" in item:
            print("Combo Discount: Rs.", item["combo_discount"])
        print()


def show_cart(cart, menu_items):
    print("\n========== YOUR ORDER ==========")

    if len(cart) == 0:
        print("Your cart is empty.")
        return

    for item in cart:
        print("-", item["name"].title(), "| Rs.", item["price"], "| Spice:", item["spice"], "| Note:", item["note"])

    print("Total Price: Rs.", calculate_total(cart, menu_items))


def parse_customer_message(thread_id, user_message, menu_items):
    menu_text = ""
    for item in menu_items:
        menu_text += f"- {item['name']} | price: {item['price']} | spice: {', '.join(item['spice_levels'])} | substitutions: {', '.join(item['substitutions'])} | allergy: {item['allergy_notes']}\n"

    prompt = f"""
Read the customer message and convert it into one simple JSON action.

Menu:
{menu_text}

Customer message:
{user_message}

Return JSON only:
{{
  "action": "show_menu OR add OR remove OR show_cart OR checkout OR unknown",
  "item_name": "",
  "spice": "",
  "note": ""
}}

Rules:
- If the customer wants to order something, use "add".
- If the customer wants to delete something, use "remove".
- If the customer asks for menu, use "show_menu".
- If the customer asks about cart, use "show_cart".
- If the customer wants to finish order, use "checkout".
- Keep missing values empty.
"""

    raw = ask_llm(thread_id, prompt)
    raw = raw.strip().replace("```json", "").replace("```", "")

    try:
        data = json.loads(raw)
        return data
    except Exception:
        return {
            "action": "unknown",
            "item_name": "",
            "spice": "",
            "note": ""
        }


menu = load_menu()
menu_items = menu["items"]
cart = []
thread_id = assignment_helper.generate_thread_id()

print("===================================")
print(" AI WAITER - RESTAURANT ORDER BOT")
print("===================================")
print("Type normal sentences like:")
print("- show me the menu")
print("- add zinger burger")
print("- add fries")
print("- remove fries")
print("- show my cart")
print("- checkout")
print("- exit")
print("===================================")

while True:
    user_input = input("\nCustomer: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye.")
        break

    assignment_helper.save_message(thread_id, "restaurant_bot", "user", user_input)

    action_data = parse_customer_message(thread_id, user_input, menu_items)
    action = action_data["action"].lower()
    item_name = action_data["item_name"].lower().strip()
    spice = action_data["spice"].lower().strip()
    note = action_data["note"].lower().strip()

    if action == "show_menu":
        show_menu(menu_items)
        continue

    if action == "show_cart":
        show_cart(cart, menu_items)
        continue

    if action == "add":
        item = find_item(menu_items, item_name)

        if item is None:
            print("Sorry, that item is not on the menu.")
            continue

        if item["in_stock"] is False:
            print("Sorry, that item is out of stock.")
            continue

        if spice == "":
            spice = item["spice_levels"][0]

        if spice not in item["spice_levels"]:
            spice = item["spice_levels"][0]

        if note == "":
            note = "none"

        if "gluten" in note and "gluten" in item["allergy_notes"].lower():
            print("Sorry, this item is not safe for a gluten allergy.")
            print("Allowed substitutions:", ", ".join(item["substitutions"]))
            continue

        if "dairy" in note and "dairy" in item["allergy_notes"].lower():
            print("Sorry, this item is not safe for a dairy allergy.")
            print("Allowed substitutions:", ", ".join(item["substitutions"]))
            continue

        cart.append(
            {
                "name": item["name"],
                "price": item["price"],
                "spice": spice,
                "note": note
            }
        )

        reply = ask_llm(
            thread_id,
            f"""
            The customer added this item:
            Item: {item['name']}
            Spice: {spice}
            Note: {note}

            Reply in one short polite sentence.
            """
        )
        print(reply)
        continue

    if action == "remove":
        found = False
        for i, cart_item in enumerate(cart):
            if cart_item["name"] == item_name:
                del cart[i]
                found = True
                break

        if found:
            reply = ask_llm(
                thread_id,
                f"The customer removed {item_name}. Reply in one short polite sentence."
            )
            print(reply)
        else:
            print("That item is not in your cart.")
        continue

    if action == "checkout":
        if len(cart) == 0:
            print("Your cart is empty.")
            continue

        total = calculate_total(cart, menu_items)
        show_cart(cart, menu_items)

        final_reply = ask_llm(
            thread_id,
            f"""
            Confirm the final order in simple words.
            Order: {cart}
            Total price: Rs. {total}
            Mention that the order is confirmed.
            """
        )
        print("\nOrder Confirmation:")
        print(final_reply)
        assignment_helper.save_message(thread_id, "restaurant_bot", "assistant", final_reply)
        break

    print("Unknown command. Try: show menu, add burger, remove fries, show cart, checkout")
