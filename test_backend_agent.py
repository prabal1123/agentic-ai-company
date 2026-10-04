from pathlib import Path

from appAgents.llm import LocalLLM
from appAgents.backend import BackendDeveloperAgent
from appTools.filesystem import FileSystemTool
from appTools.terminal import TerminalTool
from appTools.test_runner import TestRunnerTool


workspace = Path("ai_workspace").resolve()

filesystem = FileSystemTool(workspace)
terminal = TerminalTool(workspace)
test_runner = TestRunnerTool(workspace)

llm = LocalLLM(model="qwen3:1.7b")

backend_agent = BackendDeveloperAgent(
    llm=llm,
    filesystem=filesystem,
    terminal=terminal,
    test_runner=test_runner,
)

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
Use plain Python for the initial MVP (no Django project scaffold needed
in this workspace).

Create clean, self-contained modules with:

- models (plain Python classes)
- basic business logic functions
- input validation
- pytest-style tests

Keep the architecture simple and maintainable.
"""

print("\n=== BACKEND AGENT ===")

implementation = backend_agent.run(product, requirements, architecture)

print("\n=== IMPLEMENTATION SUMMARY ===")
print(implementation["summary"])

print("\n=== GENERATED FILES ===")
for file_data in implementation["files"]:
    print(f"- {file_data['path']}")

print("\n=== CREATING FILES ===")
results = backend_agent.execute(implementation)
for result in results:
    print(result)

print("\n=== WORKSPACE ===")
print(filesystem.list_files())

print("\n=== RUNNING COMPILE + TEST CHECK ===")
result = backend_agent.test(implementation)
print(result)

if result["success"]:
    print(f"\n✅ Passed ({result['stage']} stage).")
else:
    print(f"\n❌ Failed at {result['stage']} stage.")

print("\n=== DONE ===")
