import subprocess
import sys


class TestRunnerTool:
    """
    Runs automated tests inside a controlled workspace.
    """

    def __init__(self, workspace):
        self.workspace = workspace

    def run_pytest(self, test_file="tests.py", timeout=120):
        command = [
            sys.executable,
            "-m",
            "pytest",
            test_file,
        ]

        result = subprocess.run(
            command,
            cwd=self.workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return {
            "command": " ".join(command),
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }

    def compile_python(self, files):
        command = [
            sys.executable,
            "-m",
            "py_compile",
            *files,
        ]

        result = subprocess.run(
            command,
            cwd=self.workspace,
            capture_output=True,
            text=True,
            timeout=60,
        )

        return {
            "command": " ".join(command),
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }