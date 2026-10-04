# agents/product.py

from .base import BaseAgent

class ProductManagerAgent(BaseAgent):
    name = "product_manager"
    def run(self, idea):
        prompt = f"""
        You are the Product Manager Agent of an AI-native software company.
        Your responsibility is to convert a raw business idea into a structured product definition.

        Business idea:
        {idea}

        Analyze:
        1. Problem
        2. Target customers
        3. User personas
        4. Main user journeys
        5. Functional requirements
        6. Non-functional requirements
        7. MVP features
        8. Future features
        9. Risks
        10. Assumptions
        11. Acceptance criteria

        Return a clear structured response.
        """
        return self.llm.generate(prompt)