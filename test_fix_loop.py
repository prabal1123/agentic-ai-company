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

file_paths = ["models.py", "logic.py", "tests.py"]

MAX_ATTEMPTS = 4


def get_current_files():
    return [
        {"path": p, "content": filesystem.read_file(p)}
        for p in file_paths
    ]


def run_with_retries():
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n{'=' * 20} ATTEMPT {attempt}/{MAX_ATTEMPTS} {'=' * 20}")

        print("\n--- compile check ---")
        compile_result = test_runner.compile_python(file_paths)
        print(compile_result)

        if not compile_result["success"]:
            error_report = {"stage": "compile", **compile_result}
        else:
            print("\n--- compile passed, running pytest ---")
            pytest_result = test_runner.run_pytest()
            print(pytest_result)

            if pytest_result["success"]:
                print(f"\n✅ All checks passed on attempt {attempt}.")
                return True

            error_report = {"stage": "pytest", **pytest_result}

        print(f"\n--- fixing (stage: {error_report['stage']}) ---")
        files = get_current_files()
        fix_result = fix_agent.run(files, error_report)

        print(f"Fix summary: {fix_result['summary']}")
        print("Files changed:", [f["path"] for f in fix_result["files"]])

        fix_agent.execute(fix_result)

    print(f"\n❌ Did not pass after {MAX_ATTEMPTS} attempts. Giving up.")
    return False


if __name__ == "__main__":
    run_with_retries()
    print("\n=== DONE ===")
