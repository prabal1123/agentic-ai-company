import shlex
import subprocess
import sys


class TerminalTool:
    """
    Executes a restricted set of commands inside a controlled workspace.
    """

    ALLOWED_COMMANDS = {
        "python",
        "pytest",
        "git",
    }

    def __init__(self, workspace):
        self.workspace = workspace

    def run(self, command, timeout=60):
        if not isinstance(command, str):
            raise TypeError("Command must be a string.")

        parts = shlex.split(command)

        if not parts:
            raise ValueError("Command cannot be empty.")

        executable = parts[0]

        # Only allow approved executables.
        if executable not in self.ALLOWED_COMMANDS:
            raise PermissionError(
                f"Command '{executable}' is not allowed."
            )

        # Prevent arbitrary Python code execution.
        if executable == "python":
            if "-c" in parts or "-m" in parts and "pip" in parts:
                raise PermissionError(
                    "This Python command is not allowed."
                )

        result = subprocess.run(
            parts,
            cwd=self.workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return {
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }

    def run_tests(self):
        result = subprocess.run(
            [sys.executable, "manage.py", "test"],
            cwd=self.workspace,
            capture_output=True,
            text=True,
            timeout=120,
        )

        return {
            "command": f"{sys.executable} manage.py test",
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }