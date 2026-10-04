# test_agent.py

from django.test import TestCase

from appAgents.llm import LocalLLM
from appAgents.product import ProductManagerAgent

llm = LocalLLM()
agent = ProductManagerAgent(llm)

idea = """
I want to build a payroll application
for companies with 100-500 employees.
It should manage employees, salary,
attendance, deductions and payroll.
"""

result = agent.run(idea)

print(result)
