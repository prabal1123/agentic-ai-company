# # # appAgents/architecture.py
# # class ArchitectureAgent(BaseAgent):
# #     name = "architecture"
# #     def run(self, product, requirements):
# #         prompt = f"""
# #         You are a senior software architect.

# #         Design a production-ready software architecture for the following product.

# #         PRODUCT:
# #         {product}

# #         REQUIREMENTS:
# #         {requirements}

# #         Define:
# #         1. Technology stack
# #         2. Application architecture
# #         3. Database architecture
# #         4. Data models
# #         5. APIs
# #         6. Authentication
# #         7. Authorization
# #         8. Background jobs
# #         9. Caching
# #         10. Logging
# #         11. Monitoring
# #         12. Security
# #         13. Scalability
# #         14. Deployment architecture

# #         Explain important architectural decisions.
# #         """

# #         return self.llm.generate(prompt)



# # appAgents/architecture.py
# from .base import BaseAgent

# class ArchitectureAgent(BaseAgent):
#     name = "architecture"
#     def run(self, product, requirements):
#         prompt = f"""
#         You are a senior software architect.

#         Design a production-ready software architecture for the following product.

#         PRODUCT:
#         {product}

#         REQUIREMENTS:
#         {requirements}

#         Define:
#         1. Technology stack
#         2. Application architecture
#         3. Database architecture
#         4. Data models
#         5. APIs
#         6. Authentication
#         7. Authorization
#         8. Background jobs
#         9. Caching
#         10. Logging
#         11. Monitoring
#         12. Security
#         13. Scalability
#         14. Deployment architecture

#         Explain important architectural decisions.
#         """
#         return self.llm.generate(prompt)



# appAgents/architecture.py
from .base import BaseAgent

class ArchitectureAgent(BaseAgent):
    name = "architecture"
    def run(self, product, requirements):
        prompt = f"""
        You are a senior software architect.

        Design a production-ready software architecture for the following product.

        PRODUCT:
        {product}

        REQUIREMENTS:
        {requirements}

        IMPORTANT EXECUTION CONSTRAINT:
        The generated code will run as standalone Python scripts/modules
        in an isolated workspace. There is NO web framework runtime
        available (no Django app registry, no configured settings, no
        ORM connection, no ASGI/WSGI server). Code cannot rely on
        `django.setup()`, `INSTALLED_APPS`, `django.db.models.Model`,
        Django REST Framework, Flask, or any framework that requires
        app initialization before classes can be defined or imported.
        You may still discuss such frameworks narratively as a
        real-world recommendation for a FUTURE production deployment,
        but the "Data models" and "APIs" sections must ALSO specify a
        plain-Python implementation approach (e.g. plain classes or
        dataclasses for models, plain functions or classes for API
        handlers) that a backend engineer can implement and unit test
        with pytest, with zero framework dependencies.

        Define:
        1. Technology stack
        2. Application architecture
        3. Database architecture
        4. Data models
        5. APIs
        6. Authentication
        7. Authorization
        8. Background jobs
        9. Caching
        10. Logging
        11. Monitoring
        12. Security
        13. Scalability
        14. Deployment architecture

        Explain important architectural decisions.
        """
        return self.llm.generate(prompt)