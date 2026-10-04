from pathlib import Path

from appAgents.llm import LocalLLM
from appAgents.testing import TestingAgent
from appTools.filesystem import FileSystemTool
from appTools.test_runner import TestRunnerTool


workspace = Path("ai_workspace").resolve()

filesystem = FileSystemTool(workspace)
test_runner = TestRunnerTool(workspace)

llm = LocalLLM(model="qwen3:1.7b")

testing_agent = TestingAgent(llm=llm, filesystem=filesystem)

requirements = """
Farmers should be able to:

1. Create an account
2. Add farms
3. Upload crop photos
4. Record crop health observations
5. View crop health history
"""

source_paths = ["models.py", "logic.py"]

print("\n=== READING SOURCE FILES ===")
files = []
for path in source_paths:
    content = filesystem.read_file(path)
    files.append({"path": path, "content": content})
    print(f"- read {path} ({len(content)} chars)")

print("\n=== TESTING AGENT ===")
test_result = testing_agent.run(files, requirements)

print("\n=== SUMMARY ===")
print(test_result["summary"])

for f in test_result["files"]:
    f["path"] = "tests_generated.py"

print("\n=== WRITING tests_generated.py ===")
results = testing_agent.execute(test_result)
for r in results:
    print(r)

print("\n=== GENERATED CONTENT ===")
print(filesystem.read_file("tests_generated.py"))

print("\n=== COMPILE CHECK ===")
compile_result = test_runner.compile_python(["tests_generated.py"])
print(compile_result)

if compile_result["success"]:
    print("\n=== RUNNING PYTEST ON GENERATED TESTS ===")
    pytest_result = test_runner.run_pytest(test_file="tests_generated.py")
    print(pytest_result)

    if pytest_result["success"]:
        print("\n✅ Generated tests compile AND pass.")
    else:
        print("\n⚠️ Generated tests compile but fail — likely wrong "
              "assumptions about validation behavior.")
else:
    print("\n❌ Generated tests do not even compile — likely a "
          "cross-file import mistake.")

print("\n=== DONE ===")
