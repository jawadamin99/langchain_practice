"""
SmileCare Dental Clinic - Chatbot (Functional Style, LangChain + Gemini)
--------------------------------------------------------------------------
Scope: Limited to prompt + LLM + LangChain only - no extra tools, agents,
or structured output. The entire code is written using plain functions
(no classes).

Output: Plain text (response.content is already a string, not JSON).
Input: Runtime interactive input via terminal (chat_loop).

SETUP:
    pip install langchain langchain-google-genai python-dotenv
    export GOOGLE_API_KEY="your-gemini-api-key-here"
    (Get your key here: https://aistudio.google.com/apikey)

RUN:
    python3 dental_clinic_chatbot_gemini.py
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()


# ---------------------------------------------------------------------------
# 1) THE PROMPT (Role + Clinic Info + Instructions + Guardrails combined)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are the virtual assistant for SmileCare Dental Clinic.

Clinic Information:
- Name: SmileCare Dental Clinic
- Timings: Monday to Saturday, 9:00 AM - 8:00 PM (Closed Sunday)
- Services: Teeth Cleaning, Whitening, Root Canal, Braces, Tooth Extraction,
  Dental Checkup, Cavity Filling
- Location: Main Boulevard, New York

Your job:
1. Answer patient questions about clinic timings, services, and pricing (say
   "please confirm exact pricing with the front desk" if asked for exact cost).
2. If a patient wants to book an appointment, politely collect: name, phone
   number, preferred date/time, and reason for visit — one at a time,
   conversationally.
3. If a patient describes a dental symptom (toothache, bleeding gums, etc.),
   respond with general reassurance and advise booking an appointment. NEVER
   diagnose the exact problem or suggest medicine/dosage.
4. If the symptom sounds severe (uncontrolled bleeding, facial swelling with
   fever, knocked-out tooth, severe trauma), tell them to visit the clinic
   immediately or go to the nearest emergency room.
5. Keep responses short, warm, and conversational — this is a chat, not an essay.
   Respond in plain conversational text only — never JSON or markdown.
6. Always end symptom-related replies with: "This is not a medical diagnosis."
"""


# ---------------------------------------------------------------------------
# 2) BUILD THE CHAIN (functional style - simply returns a runnable chain)
# ---------------------------------------------------------------------------
def build_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("history"),
        ("human", "{user_input}"),
    ])

    chain = prompt | llm
    return chain


# ---------------------------------------------------------------------------
# 3) GET A SINGLE RESPONSE (functional - takes state in, returns plain text)
# ---------------------------------------------------------------------------
def get_response(chain, history, user_input):
    response = chain.invoke({"history": history, "user_input": user_input})
    # fixed: AIMessage has no .text attribute, use .content instead
    return response.text  # plain text string, not JSON


# ---------------------------------------------------------------------------
# 4) UPDATE HISTORY (pure function - returns a new list, does not mutate)
# ---------------------------------------------------------------------------
def add_to_history(history, user_input, reply):
    return history + [HumanMessage(content=user_input), AIMessage(content=reply)]


# ---------------------------------------------------------------------------
# 5) INTERACTIVE CHAT LOOP - user types their own input at runtime
# ---------------------------------------------------------------------------
def chat_loop(chain):
    print("SmileCare Dental Assistant (type 'exit' to quit)\n")
    history = []
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Assistant: Take care! See you at SmileCare soon.")
            break
        reply = get_response(chain, history, user_input)
        print(f"Assistant: {reply}\n")
        history = add_to_history(history, user_input, reply)


# ---------------------------------------------------------------------------
# 6) MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print("GOOGLE_API_KEY is not set. Run this first:")
        print('export GOOGLE_API_KEY="your-gemini-api-key-here"')
        print("Get a key here: https://aistudio.google.com/apikey")
    else:
        dental_chain = build_chain()
        chat_loop(dental_chain)
