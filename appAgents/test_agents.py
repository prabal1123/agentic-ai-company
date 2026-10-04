# # test_agents.py
# from appAgents.llm import LocalLLM
# from appAgents.product import ProductManagerAgent
# from appAgents.requirments import RequirementsAgent
# from appAgents.architecture import ArchitectureAgent

# llm = LocalLLM(model="qwen3:1.7b")

# idea = "A mobile app that helps small farmers track crop health using photos."

# print("=== Product Manager Agent ===")
# pm_agent = ProductManagerAgent(llm)
# product_def = pm_agent.run(idea)
# print(product_def)

# print("\n=== Requirements Agent ===")
# req_agent = RequirementsAgent(llm)
# requirements = req_agent.run(product_def)
# print(requirements)

# print("\n=== Architecture Agent ===")
# arch_agent = ArchitectureAgent(llm)
# architecture = arch_agent.run(product_def, requirements)
# print(architecture)


from appAgents.llm import LocalLLM

from appAgents.product import ProductManagerAgent
from appAgents.requirments import RequirementsAgent
from appAgents.architecture import ArchitectureAgent
from appAgents.backend import BackendDeveloperAgent
from appAgents.code_review import CodeReviewAgent
from appAgents.testing import TestingAgent
from appAgents.bug_analysis import BugAnalysisAgent
from appAgents.fix import FixAgent


llm = LocalLLM(model="qwen3:1.7b")


idea = """
A mobile app that helps small farmers track crop health using photos.
"""


print("\n=== PRODUCT MANAGER ===")
pm_agent = ProductManagerAgent(llm)
product = pm_agent.run(idea)
print(product)


print("\n=== REQUIREMENTS ===")
requirements_agent = RequirementsAgent(llm)
requirements = requirements_agent.run(product)
print(requirements)


print("\n=== ARCHITECTURE ===")
architecture_agent = ArchitectureAgent(llm)
architecture = architecture_agent.run(product, requirements)
print(architecture)


print("\n=== BACKEND DEVELOPER ===")
backend_agent = BackendDeveloperAgent(llm)
backend = backend_agent.run(
    product,
    requirements,
    architecture
)
print(backend)


print("\n=== CODE REVIEW ===")
review_agent = CodeReviewAgent(llm)
review = review_agent.run(
    backend,
    requirements,
    architecture
)
print(review)


print("\n=== TESTING ===")
testing_agent = TestingAgent(llm)
tests = testing_agent.run(
    product,
    requirements,
    architecture,
    backend
)
print(tests)


print("\n=== BUG ANALYSIS ===")

# For now, we use the generated test strategy as input.
# Later this will be replaced by real test execution results.

bug_agent = BugAnalysisAgent(llm)
bug_analysis = bug_agent.run(
    tests,
    backend,
    requirements
)

print(bug_analysis)


print("\n=== FIX ===")

fix_agent = FixAgent(llm)
fix = fix_agent.run(
    backend,
    bug_analysis,
    architecture
)

print(fix)