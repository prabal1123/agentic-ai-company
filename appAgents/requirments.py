# agents/requirements.py
from .base import BaseAgent
class RequirementsAgent(BaseAgent):
    name = "requirements"
    def run(self, product_definition):
        prompt = f"""
You are a senior software requirements engineer.

Convert the following product definition into detailed software requirements.

PRODUCT DEFINITION:

{product_definition}

Create:
1. Epics
2. User stories
3. Functional requirements
4. Business rules
5. Edge cases
6. Acceptance criteria
7. API requirements
8. Data requirements
9. Validation rules

Return a structured response.
"""
        return self.llm.generate(prompt)