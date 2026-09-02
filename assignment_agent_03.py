from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.document_loaders import PyPDFLoader
from config.assignment_helper import AssignmentHelper
# from config.llm_config import llm_gemini as llm
from config.llm_config import llm
assignment_helper = AssignmentHelper()

load_dotenv()

reader = PyPDFLoader("agentic_data/history_book.pdf")
pages = reader.load()

syllabus_text = ""

# for page in pages:
#     syllabus_text += page.page_content + "\n"

syllabus_text += pages[0].page_content
syllabus_text += pages[1].page_content
syllabus_text += pages[7].page_content

system_prompt = f"""
You are a Personalized Tutor Bot.

You must teach the student using ONLY the syllabus below.

SYLLABUS:
{syllabus_text}

Rules:

- Ask questions only from the syllabus.
- Ask one question at a time.
- Do not use outside knowledge.
- Remember the conversation.
- Check whether the student's answer is correct or incorrect.
- If the student gives two wrong answers on the same topic,
  explain that topic again before continuing.
- After explaining a weak topic, ask an easier question.
- If the student is answering correctly, gradually ask harder questions.

IMPORTANT PERFORMANCE RULE:

Whenever the student answers a question:

- Start your response with RESULT: CORRECT if the answer is correct.
- Start your response with RESULT: INCORRECT if the answer is incorrect.
- Start your response with RESULT: NONE if the student is not answering
  a question, for example if they are asking you to change difficulty.

After the RESULT line, continue your normal tutor response.
"""

memory = MemorySaver()

thread_id = assignment_helper.generate_thread_id()
config = {
    "configurable": {
        "thread_id": thread_id
    }
}

agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    checkpointer=memory
)

performance = {
    "correct": 0,
    "incorrect": 0
}


print("==============================")
print(" PERSONALIZED TUTOR BOT")
print("==============================")
print("Type 'exit' to finish")
print()


while True:
    user_input = input("Student: ")
    if user_input.lower() == "exit":
        break
    if user_input.lower() is None:
        continue
    assignment_helper.save_message(str(thread_id), 'tutor_bot', 'user', user_input)
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

    ai_message = response["messages"][-1].text
    assignment_helper.save_message(str(thread_id), 'tutor_bot', 'assistant', ai_message)

    if "RESULT: CORRECT" in ai_message:
        performance["correct"] += 1
    elif "RESULT: INCORRECT" in ai_message:
        performance["incorrect"] += 1
    print()

    display_message = ai_message.replace("RESULT: CORRECT", "")
    display_message = display_message.replace("RESULT: INCORRECT", "")
    display_message = display_message.replace("RESULT: NONE", "")
    display_message = display_message.strip()

    print("\nTutor:", display_message)


print("==============================")
print("SESSION SUMMARY")
print("==============================")

print("Correct answers:", performance["correct"])
print("Incorrect answers:", performance["incorrect"])