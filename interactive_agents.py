from appAgents.llm import LocalLLM
from appAgents.product import ProductManagerAgent
from appAgents.requirments import RequirementsAgent
from appAgents.architecture import ArchitectureAgent

def main():
    llm = LocalLLM(model="qwen3:1.7b")

    print("Enter your business idea (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    idea = "\n".join(lines)

    if not idea.strip():
        print("No idea entered, exiting.")
        return

    print("\n=== Product Manager Agent ===")
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

if __name__ == "__main__":
    main()
