from pathlib import Path

from appAgents.llm import LocalLLM
from appAgents.backend import BackendDeveloperAgent
from appTools.filesystem import FileSystemTool
from appTools.terminal import TerminalTool


# -----------------------------------------
# Workspace
# -----------------------------------------

workspace = Path("ai_workspace").resolve()


# -----------------------------------------
# Tools
# -----------------------------------------

filesystem = FileSystemTool(workspace)
terminal = TerminalTool(workspace)


# -----------------------------------------
# LLM
# -----------------------------------------

llm = LocalLLM(model="qwen3:1.7b")


# -----------------------------------------
# Backend Agent
# -----------------------------------------

backend_agent = BackendDeveloperAgent(
    llm=llm,
    filesystem=filesystem,
    terminal=terminal,
)


# -----------------------------------------
# Example inputs
# -----------------------------------------

product = """
A mobile application that helps small farmers
track crop health using photos.
"""

requirements = """
Farmers should be able to:

1. Create an account
2. Add farms
3. Upload crop photos
4. Record crop health observations
5. View crop health history
"""

architecture = """
Use Django and SQLite for the initial MVP.

Create a clean Django backend with:

- models
- APIs
- validation
- tests

Keep the architecture simple and maintainable.
"""


# -----------------------------------------
# Generate implementation
# -----------------------------------------

print("\n=== BACKEND AGENT ===")

implementation = backend_agent.run(
    product,
    requirements,
    architecture,
)

print("\n=== IMPLEMENTATION SUMMARY ===")
print(implementation["summary"])


# -----------------------------------------
# Show generated files
# -----------------------------------------

print("\n=== GENERATED FILES ===")

for file_data in implementation["files"]:
    print(f"- {file_data['path']}")


# -----------------------------------------
# Execute implementation
# -----------------------------------------

print("\n=== CREATING FILES ===")

results = backend_agent.execute(
    implementation
)

for result in results:
    print(result)


# -----------------------------------------
# List workspace
# -----------------------------------------

print("\n=== WORKSPACE ===")

print(filesystem.list_files())

print("\n=== RUNNING PYTHON COMPILE CHECK ===")

result = terminal.run(
    "python -m py_compile models.py views.py tests.py"
)

print(result)

if result["success"]:
    print("\n✅ Generated code passed compilation.")
else:
    print("\n❌ Generated code has errors.")


print("\n=== DONE ===")