from langchain_core.prompts import PromptTemplate

from config.llm_config import llm



# ================================================================================
# 1. Healthcare – Medical Appointment Assistant
# ================================================================================

age = input("Enter Your Age: ")
symptom_1 = input("Whats your first symptom: ")
symptom_2 = input("Whats your second symptom: ")

symptoms = [symptom_1, symptom_2]

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

response = chain.invoke({"age": age, "symptoms": symptoms})
print(response.text)

# ================================================================================
# 2. Healthcare – Hospital Triage Agent
# ================================================================================

# prompt = PromptTemplate.from_template("""You are an Emergency Room Triage AI.
#
# Evaluate:
# - Heart rate
# - Blood pressure
# - Temperature
# - Oxygen level
# - Medical history
#
# Classify:
# - Critical
# - High Priority
# - Medium
# - Low
#
# Patient Data:
# Heart Rate: {heart_rate}
# Blood Pressure: {blood_pressure}
# Temperature: {temperature}
# Oxygen Level: {oxygen_level}
# Medical History: {medical_history}
#
# Return:
# Triage Level:
# Reasoning:
# Recommended Action:
# """)
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "heart_rate": "125 bpm",
#     "blood_pressure": "90/60 mmHg",
#     "temperature": "102 F",
#     "oxygen_level": "89%",
#     "medical_history": "Diabetes"
# })
# print(response.text)

# ================================================================================
# 3. Healthcare – Prescription Reminder Agent
# ================================================================================

# prompt = PromptTemplate.from_template("""You are an AI Medication Manager.
#
# Prescriptions:
# {prescriptions}
#
# Tasks:
# - Read prescriptions.
# - Generate medication schedule.
# - Detect medicine conflicts.
# - Send reminders.
# - Warn about missed doses.
# - Suggest contacting doctor if symptoms continue.
# """)
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "prescriptions": ['Panadol Xtra 1+1', 'Panadol CF 1+1', 'Brufen 1+1+1']
# })
#
# print(response.text)


# ================================================================================
# 4. Education – Personal AI Tutor
# ================================================================================

# prompt = PromptTemplate.from_template("""You are an AI Tutor.
#
# Student Information:
# Grade: {grade}
# Subject: {subject}
#
# Weak Topics:
# {weak_topics}
#
# Tasks:
# - Assess knowledge.
# - Create personalized study plan.
# - Generate practice questions.
# - Evaluate answers.
# - Recommend next lessons.
# """
# )
#
# chain = prompt | llm
# response = chain.invoke({
#     "grade":10,
#     "subject":"Mathematics",
#     "weak_topics":["Pythagoras Theorem","Trigonometry"],
# })
#
# print(response.text)


# ================================================================================
# 5. Education – Assignment Reviewer
# ================================================================================

# prompt = PromptTemplate.from_template(
#     """You are an AI Teacher.
# Here's the student Assignment
# {student_assignment}
#
# Your Task is to:
# Review student assignment.
#
# Evaluate:
# - Grammar
# - Logic
# - Originality
# - Formatting
# - References
#
# Provide:
# - Marks out of 100
# - Suggestions for improvement
# - Improved version if the assignment"""
# )
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "student_assignment": """
#     Pakstan is a grat contry, It is divided into 10 states
#     """
# })
# print(response.text)

# ================================================================================
# 6. Education – Learning Path Generator
# ================================================================================
# prompt = PromptTemplate.from_template(
#     """
#     Create a {days}-day learning roadmap.
#
# Goal:
# {goal}
# Student Level:
# {student_level}
#
# Include:
# - Python
# - Machine Learning
# - Deep Learning
# - LangChain
# - RAG
# - AI Agents
# - Projects
# - Interview Preparation
#
#
# Adjust roadmap for beginners.
#     """
# )
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "days": 90,
#     "goal": "Become an AI Engineer",
#     "student_level": "Beginner"
# })
#
# print(response.text)

# ================================================================================
# 7. Real Estate – Property Recommendation Agent
# ================================================================================

# prompt = PromptTemplate.from_template(
#     """You are an AI Real Estate Consultant.
# Customer Preferences:
# Budget: {budget}
# Location: {location}
# Bedrooms: {bedrooms}
# Garage: {garage_needed}
# Schools Nearby: {schools_nearby}
#
# Tasks:
# - Search properties.
# - Rank top 10.
# - Explain why each property matches."""
# )
#
# chain = prompt | llm
# response = chain.invoke({
#     "budget": "$250,000",
#     "location": "Dallas",
#     "bedrooms": 2,
#     "garage_needed": "Yes",
#     "schools_nearby": "Required"
# })
# print(response.text)


# ================================================================================
# 8. Real Estate – Property Investment Advisor
# ================================================================================
# prompt = PromptTemplate.from_template(
#     """You are an AI Property Investment Advisor.
#
# Analyze this property investment.
#
# Inputs:
# - Purchase Price: {purchase_price}
# - Rental Income: {rental_income}
# - Maintenance Cost: {maintenance_cost}
# - Location: {location}
# - Crime Rate: {crime_rate}
# - Future Development: {future_development}
#
# Calculate:
# - Annual Net Rental Income = (Rental Income * 12) - Maintenance Cost
# - ROI = (Annual Net Rental Income / Purchase Price) * 100
# - Rental Yield = ((Rental Income * 12) / Purchase Price) * 100
# - Risk Score from 1 to 10 using crime rate, location quality, and future development
#
# Recommend one:
# - Buy
# - Hold
# - Avoid
#
# Return:
# - ROI percentage
# - Rental Yield percentage
# - Risk Score
# - Recommendation
# - Short reasoning
# """
# )
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "purchase_price": 250000,
#     "rental_income": 2200,
#     "maintenance_cost": 4500,
#     "location": "Austin, Texas",
#     "crime_rate": "Medium",
#     "future_development": "New metro line and business park planned nearby"
# })
#
# print(response.text)

# ================================================================================
# 9. Real Estate – Lead Qualification Agent
# ================================================================================
# prompt = PromptTemplate.from_template(
#     """You are an AI Sales Agent.
#
# Collect:
# - Budget: {budget}
# - Timeline: {timeline}
# - Property Type: {property_type}
# - Location: {location}
# - Loan Status: {loan_status}
#
# Classify Lead:
# - Hot
# - Warm
# - Cold
#
# Schedule meeting if qualified.
#
# Return:
# - Lead classification
# - Qualification reason
# - Meeting recommendation
# - Suggested next step
# """
# )
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "budget": "$300,000",
#     "timeline": "Ready to buy within 30 days",
#     "property_type": "Single-family home",
#     "location": "Dallas",
#     "loan_status": "Pre-approved"
# })
#
# print(response.text)

# ================================================================================
# 10. E-commerce – Shopping Assistant
# ================================================================================
# prompt = PromptTemplate.from_template(
#     """You are an AI Shopping Assistant.
#
# Customer Wants:
# {customer_wants}
#
# Budget:
# {budget}
#
# Requirements:
# {requirements}
#
# Compare products.
#
# Recommend the best option.
#
# Explain pros and cons.
#
# Return:
# - Compared products
# - Best recommendation
# - Pros and cons
# - Reasoning
# """
# )
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "customer_wants": "Gaming Laptop",
#     "budget": "$1200",
#     "requirements": ["RTX Graphics", "16GB RAM", "Battery > 6 Hours"]
# })
#
# print(response.text)

# ================================================================================
# 11. E-commerce – Customer Support Agent
# ================================================================================
# prompt = PromptTemplate.from_template(
#     """You are an AI Support Representative.
#
# Customer says:
# {customer_message}
#
# Tasks:
# - Check order status.
# - Verify shipping.
# - Estimate delivery.
# - Offer refund if delayed.
# - Escalate if necessary.
#
# Respond professionally.
#
# Return:
# - Customer response
# - Order status action
# - Shipping verification action
# - Refund or escalation decision
# """
# )
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "customer_message": "My order hasn't arrived."
# })
#
# print(response.text)

# ================================================================================
# 12. E-commerce – Inventory Management Agent
# ================================================================================
# prompt = PromptTemplate.from_template(
#     """You are an AI Inventory Manager.
#
# Analyze:
# - Sales History: {sales_history}
# - Current Inventory: {current_inventory}
# - Supplier Lead Time: {supplier_lead_time}
# - Seasonality: {seasonality}
#
# Predict:
# - Stock shortage
# - Overstock
#
# Recommend purchase quantities.
#
# Return:
# - Shortage prediction
# - Overstock prediction
# - Purchase quantities
# - Reasoning
# """
# )
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "sales_history": "Average 120 units/month, last month 160 units",
#     "current_inventory": "80 units",
#     "supplier_lead_time": "21 days",
#     "seasonality": "Holiday demand expected to increase by 30%"
# })
#
# print(response.text)

# ================================================================================
# 13. Finance – Financial Advisor
# ================================================================================
# prompt = PromptTemplate.from_template(
#     """You are an AI Financial Planner.
#
# Client:
# Age: {age}
# Salary: {salary}
# Savings: {savings}
# Risk Appetite: {risk_appetite}
#
# Create:
# - Monthly Budget
# - Emergency Fund
# - Investment Plan
# - Retirement Strategy
#
# Return:
# - Monthly budget
# - Emergency fund target
# - Investment plan
# - Retirement strategy
# """
# )
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "age": 30,
#     "salary": "$5,000/month",
#     "savings": "$20,000",
#     "risk_appetite": "Medium"
# })
#
# print(response.text)

# ================================================================================
# 14. Finance – Fraud Detection Agent
# ================================================================================
# prompt = PromptTemplate.from_template(
#     """You are an AI Fraud Analyst.
#
# Analyze transaction.
#
# Inputs:
# - Amount: {amount}
# - Location: {location}
# - Device: {device}
# - Previous Transactions: {previous_transactions}
# - IP Address: {ip_address}
#
# Determine:
# - Fraud Probability
# - Risk Score
#
# Explain suspicious activities.
#
# Recommend action.
#
# Return:
# - Fraud probability
# - Risk score
# - Suspicious activity explanation
# - Recommended action
# """
# )
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "amount": "$2,800",
#     "location": "Miami, Florida",
#     "device": "New Android device",
#     "previous_transactions": "Usually under $200 from Dallas, Texas",
#     "ip_address": "203.0.113.45"
# })
#
# print(response.text)

# ================================================================================
# 15. Food Restaurant – Ordering Assistant
# ================================================================================
# test = input("testring:")
# print(test)
# prompt = PromptTemplate.from_template(
#     """You are an AI Restaurant Assistant.
#
# Customer says:
# {customer_message}
#
# Tasks:
# - Recommend menu.
# - Suggest combo deals.
# - Check allergies.
# - Calculate total bill.
# - Recommend drinks.
# - Estimate preparation time.
# - Place order.
#
# Return:
# - Recommended menu
# - Combo deals
# - Allergy questions
# - Total bill estimate
# - Drink recommendations
# - Preparation time
# - Order confirmation
# """
# )
#
# chain = prompt | llm
#
# response = chain.invoke({
#     "customer_message": "I want dinner for 4 people."
# })
#
# print(response.text)
