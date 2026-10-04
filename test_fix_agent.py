from pathlib import Path

from appAgents.llm import LocalLLM
from appAgents.backend import BackendDeveloperAgent
from appAgents.fix import FixAgent
from appTools.filesystem import FileSystemTool
from appTools.terminal import TerminalTool
from appTools.test_runner import TestRunnerTool


workspace = Path("ai_workspace").resolve()

filesystem = FileSystemTool(workspace)
terminal = TerminalTool(workspace)
test_runner = TestRunnerTool(workspace)

llm = LocalLLM(model="qwen3:1.7b")

backend_agent = BackendDeveloperAgent(
    llm=llm, filesystem=filesystem, terminal=terminal, test_runner=test_runner,
)
fix_agent = FixAgent(llm=llm, filesystem=filesystem)

print("\n=== READING EXISTING WORKSPACE FILES ===")
file_paths = ["models.py", "logic.py", "tests.py"]
files = []
for path in file_paths:
    content = filesystem.read_file(path)
    files.append({"path": path, "content": content})
    print(f"- read {path} ({len(content)} chars)")

print("\n=== RUNNING COMPILE CHECK (expect failure) ===")
compile_result = test_runner.compile_python(file_paths)
print(compile_result)

if compile_result["success"]:
    print("\nNothing to fix — compile already passes.")
else:
    error_report = {"stage": "compile", **compile_result}

    print("\n=== FIX AGENT ===")
    fix_result = fix_agent.run(files, error_report)

    print("\n=== FIX SUMMARY ===")
    print(fix_result["summary"])

    print("\n=== FILES CHANGED ===")
    for f in fix_result["files"]:
        print(f"- {f['path']}")

    print("\n=== APPLYING FIX ===")
    results = fix_agent.execute(fix_result)
    for r in results:
        print(r)

    print("\n=== RE-RUNNING COMPILE CHECK ===")
    recheck = test_runner.compile_python(file_paths)
    print(recheck)

    if recheck["success"]:
        print("\n✅ Fix worked — compile now passes.")
        print("\n=== RUNNING PYTEST ===")
        pytest_result = test_runner.run_pytest()
        print(pytest_result)
        if pytest_result["success"]:
            print("\n✅ Tests pass too.")
        else:
            print("\n⚠️ Compile passes but pytest still fails.")
    else:
        print("\n❌ Fix did not resolve the compile error.")

print("\n=== DONE ===")
