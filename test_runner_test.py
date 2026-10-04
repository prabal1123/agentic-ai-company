from pathlib import Path

from appTools.test_runner import TestRunnerTool


workspace = Path("ai_workspace").resolve()

runner = TestRunnerTool(workspace)

print("=== PYTHON COMPILE TEST ===")

result = runner.compile_python(
    [
        "models.py",
        "views.py",
        "tests.py",
    ]
)

print(result)

print("\n=== PYTEST ===")

result = runner.run_pytest()

print(result)