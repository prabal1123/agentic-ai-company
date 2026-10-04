from appAgents.llm import LocalLLM
from appAgents.product import ProductManagerAgent
from appAgents.requirments import RequirementsAgent
from appAgents.architecture import ArchitectureAgent

llm = LocalLLM(model="qwen3:1.7b")

idea = "A mobile app that helps small farmers track crop health using photos."

print("=== Product Manager Agent ===")
pm_agent = ProductManagerAgent(llm)
product_def = pm_agent.run(idea)
print(product_def)

print("\n=== Requirements Agent ===")
req_agent = RequirementsAgent(llm)
requirements = req_agent.run(product_def)
print(requirements)

print("\n=== Architecture Agent ===")
arch_agent = ArchitectureAgent(llm)
architecture = arch_agent.run(product_def, requirements)
print(architecture)
