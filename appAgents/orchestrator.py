from pathlib import Path

from .llm import LocalLLM
from .product import ProductManagerAgent
from .requirments import RequirementsAgent
from .architecture import ArchitectureAgent
from .backend import BackendDeveloperAgent
from .testing import TestingAgent
from .fix import FixAgent

from appTools.filesystem import FileSystemTool
from appTools.terminal import TerminalTool
from appTools.test_runner import TestRunnerTool


class Orchestrator:
    def __init__(self, workspace, model="qwen3:1.7b", max_fix_attempts=4):
        self.workspace = Path(workspace).resolve()
        self.max_fix_attempts = max_fix_attempts

        self.llm = LocalLLM(model=model)
        self.filesystem = FileSystemTool(self.workspace)
        self.terminal = TerminalTool(self.workspace)
        self.test_runner = TestRunnerTool(self.workspace)

        self.product_agent = ProductManagerAgent(self.llm)
        self.requirements_agent = RequirementsAgent(self.llm)
        self.architecture_agent = ArchitectureAgent(self.llm)
        self.backend_agent = BackendDeveloperAgent(
            self.llm, self.filesystem, self.terminal, self.test_runner
        )
        self.testing_agent = TestingAgent(self.llm, self.filesystem)
        self.fix_agent = FixAgent(self.llm, self.filesystem)

    def run(self, idea):
        report = {}

        print("\n=== PRODUCT MANAGER AGENT ===")
        product = self.product_agent.run(idea)
        report["product"] = product

        print("\n=== REQUIREMENTS AGENT ===")
        requirements = self.requirements_agent.run(product)
        report["requirements"] = requirements

        print("\n=== ARCHITECTURE AGENT ===")
        architecture = self.architecture_agent.run(product, requirements)
        report["architecture"] = architecture

        print("\n=== BACKEND DEVELOPER AGENT ===")
        implementation = self.backend_agent.run(product, requirements, architecture)
        report["backend_summary"] = implementation["summary"]
        print("Generated files:", [f["path"] for f in implementation["files"]])

        self.backend_agent.execute(implementation)

        source_paths = [
            f["path"] for f in implementation["files"]
            if f["path"] != "tests.py"
        ]

        print("\n=== TESTING AGENT ===")
        source_files = self._get_current_files(source_paths)
        test_result = self.testing_agent.run(source_files, requirements)

        for f in test_result["files"]:
            f["path"] = "tests.py"

        self.testing_agent.execute(test_result)
        report["testing_summary"] = test_result["summary"]

        all_paths = source_paths + ["tests.py"]

        print("\n=== COMPILE + TEST LOOP (with auto-fix) ===")
        success, final_result = self._run_with_retries(all_paths)

        report["tests_passed"] = success
        report["final_result"] = final_result
        report["files"] = all_paths

        return report

    def _get_current_files(self, paths):
        return [
            {"path": p, "content": self.filesystem.read_file(p)}
            for p in paths
        ]

    def _run_with_retries(self, file_paths):
        error_report = None

        for attempt in range(1, self.max_fix_attempts + 1):
            print(f"\n--- attempt {attempt}/{self.max_fix_attempts} ---")

            compile_result = self.test_runner.compile_python(file_paths)

            if not compile_result["success"]:
                print("Compile failed.")
                error_report = {"stage": "compile", **compile_result}
            else:
                pytest_result = self.test_runner.run_pytest()

                if pytest_result["success"]:
                    print(f"✅ All tests passed on attempt {attempt}.")
                    return True, pytest_result

                print("Pytest failed.")
                error_report = {"stage": "pytest", **pytest_result}

            print(f"Fixing (stage: {error_report['stage']})...")
            files = self._get_current_files(file_paths)
            fix_result = self.fix_agent.run(files, error_report)

            if not fix_result or "files" not in fix_result:
                print(
                    f"⚠️  Fix Agent failed to produce a usable fix on "
                    f"attempt {attempt}. Retrying..."
                )
                continue

            print("Fix summary:", fix_result.get("summary", "(no summary provided)"))
            self.fix_agent.execute(fix_result)

        print(f"❌ Did not pass after {self.max_fix_attempts} attempts.")
        return False, error_report