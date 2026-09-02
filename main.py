from langchain_core.prompts import PromptTemplate

from config.llm_config import llm

# ========= EXAMPLE 4 - Multiple Variables ========== #
# chain = prompt | llm
# response = chain.invoke({"topic": "python"})
# print(response.text)


# prompt = PromptTemplate.from_template("""
# Explain {topic}.
#
# Difficulty Level:
# {level}
#
# Language:
# {language}
# """)
#
# chain = prompt | llm
# response = chain.invoke({"language": "Urdu", "topic": "python", "level": "expert"})
# print(response.text)


# =====================================================
# Example 4 - Interview Questions Generator
# =====================================================

# prompt = PromptTemplate.from_template("""
# Generate {count} interview questions.
#
# Technology:
# {technology}
#
# Difficulty:
# {difficulty}
# """)
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "count": 3,
#     "technology": "React",
#     "difficulty": "Intermediate"
# });
# print(response.text)


# =====================================================
# Example 7 - SQL Query Generator
# =====================================================
#
# prompt = PromptTemplate.from_template("""
# Generate an SQL query.
#
# Table Name:
# {table}
#
# Task:
# {task}
#
# Return only SQL code.
# """)
#
# chain = prompt | llm
# response = chain.invoke({
#     "table": "employees",
#     "task": "Find the top 5 highest-paid employees"
# });
# print(response.text)
#


# =====================================================
# Example 8 - Python Code Generator
# =====================================================

# prompt = PromptTemplate.from_template("""
# Generate {language} code.
#
# Problem:
# {problem}
#
# Return only code.
# """)
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "language": "Python",
#     "problem": "Binary Search"
# })
#
# print(response.text)


# ==========================================================
# Example 1
# Basic PromptTemplate
# ==========================================================

# prompt = PromptTemplate.from_template(
#     "Explain {topic} in simple English."
# )
#
# print(prompt)
#
# chain = prompt | llm
# print(llm)
# print(chain)

#
# response = chain.invoke({
#     "topic": "Python"
# })
#
# print("=" * 60)
# print("Example 1")
# print("=" * 60)
# print(response.text)


# ================================================================================
# 1. Healthcare – Medical Appointment Assistant
# ================================================================================

prompt = PromptTemplate.from_template(
    """
    You are an AI Healthcare Assistant.

Responsibilities:
- Understand patient symptoms.
- Ask follow-up questions.
- Search available doctors.
- Book appointments.
- Explain preparation before the appointment.
- Send confirmation.

Patient:
Age: {age}
Symptoms:
{symptoms}

Output:
- Possible department
- Urgency level
- Appointment recommendation
- Preparation checklist
    """
)

print(prompt)

chain = prompt | llm

response = chain.invoke({"age": 42, "symptoms": ['headache for 3 days', 'fever', 'body pain']})
print(response.text)

