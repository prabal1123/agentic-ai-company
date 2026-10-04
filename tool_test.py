from pathlib import Path

from appTools.filesystem import FileSystemTool
from appTools.terminal import TerminalTool


workspace = Path("ai_workspace").resolve()

filesystem = FileSystemTool(workspace)
terminal = TerminalTool(workspace)


print("=== CREATE FILE ===")

result = filesystem.create_file(
    "hello.py",
    """
def hello():
    return "Hello from AI Company"
"""
)

print(result)


print("\n=== READ FILE ===")

content = filesystem.read_file("hello.py")
print(content)


print("\n=== LIST FILES ===")

print(filesystem.list_files())


print("\n=== RUN PYTHON ===")

result = terminal.run(
    'python -c "from hello import hello; print(hello())"'
)

print(result)


print("\n=== DONE ===")