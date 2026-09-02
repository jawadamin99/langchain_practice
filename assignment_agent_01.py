from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

from config.assignment_helper import AssignmentHelper
from config.llm_config import llm

load_dotenv()
assignment_helper = AssignmentHelper()

TRIAGE_RULES = {
    "EMERGENCY": [
        ["chest pain", "difficulty breathing"],
        ["loss of consciousness"],
    ],
    "URGENT": [
        ["persistent fever", "worsening cough"],
    ],
    "ROUTINE": [
        ["only headache"],
    ],
}

rules_text = str(TRIAGE_RULES)

system_prompt = f"""
You are an AI Symptom Triage Assistant.
Your purpose is to help users describe their symptoms, ask relevant
follow-up questions, and provide a preliminary triage recommendation.
You are NOT a doctor and must not provide a definitive diagnosis.

Use these triage rules:

{rules_text}

Your possible triage recommendations are:
1. EMERGENCY
   Recommend immediate emergency medical care when serious red-flag
   symptoms are present.
2. URGENT
   Recommend seeing a doctor within 24 hours when symptoms may require
   prompt medical evaluation but do not appear immediately life-threatening.
3. ROUTINE
   Recommend booking a routine medical appointment when symptoms appear
   mild and no major red flags are present.
Conversation rules:
- Ask relevant follow-up questions before making a triage recommendation.
- Ask only necessary questions.
- Prefer one or a small number of questions at a time.
- Use the conversation history to remember information the user has
  already provided.
- Do not ask the same question again if the user already answered it.
- Consider symptom severity, duration, associated symptoms, age, and
  relevant medical history when appropriate.
- If important information is missing, ask for it before giving the final triage recommendation.

Safety rules:
- Look for serious warning signs such as severe chest pain, difficulty
  breathing, loss of consciousness, severe bleeding, sudden weakness,
  confusion, or other potentially life-threatening symptoms.
- When serious red flags are present, prioritize emergency care instead
  of appointment scheduling.
- Never tell the user that they definitely have a particular disease.
- Never reassure the user that a serious condition is impossible.
Clinic appointments:
- If the recommendation is URGENT or ROUTINE and the user wants to see
  a doctor, use the clinic availability tool to check available doctors
  and appointment slots.
- Never invent doctor availability or appointment times.
- Only use appointment information returned by the clinic tool.
Always remind the user that this assistant provides preliminary guidance
only and is not a substitute for professional medical advice.
"""
thread_id = assignment_helper.generate_thread_id()

memory = MemorySaver()


@tool
def get_doctors():
    """ Get doctors list"""
    doctors = [
        {"name": "Dr. Jawad", "phone": "031555555", "location": "Gulberg, Lahore", "timings": "9am-5pm"},
        {"name": "Dr. Awais", "phone": "031555555", "location": "DHA, Lahore", "timings": "6pm-9pm"},
    ]
    return doctors


agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    checkpointer=memory,
    tools=[get_doctors],
)

print("\n===================================")
print("     AI Symptom-Triage Assistant")
print("===================================")
print("     Type 'exit' to end chat.")
print("===================================")
config = {
    "configurable": {
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

    assignment_helper.save_message(str(thread_id), 'triage_bot', 'user', user_input)
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
    assignment_helper.save_message(str(thread_id), 'triage_bot', 'assistant', answer)
    print("\nAI:", answer)
