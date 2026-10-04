from pathlib import Path


class FileSystemTool:
    """
    Provides safe file operations inside a designated workspace.
    """

    def __init__(self, workspace):
        self.workspace = Path(workspace).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)

    def _safe_path(self, path):
        """
        Prevent access outside the workspace.
        """
        target = (self.workspace / path).resolve()

        if not target.is_relative_to(self.workspace):
            raise ValueError("Access outside workspace is not allowed.")

        return target

    def create_file(self, path, content=""):
        target = self._safe_path(path)

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "action": "created",
            "path": str(target.relative_to(self.workspace)),
        }

    def read_file(self, path):
        target = self._safe_path(path)

        if not target.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not target.is_file():
            raise ValueError(f"Not a file: {path}")

        return target.read_text(encoding="utf-8")

    def edit_file(self, path, content):
        target = self._safe_path(path)

        if not target.exists():
            raise FileNotFoundError(f"File not found: {path}")

        target.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "action": "updated",
            "path": str(target.relative_to(self.workspace)),
        }

    def delete_file(self, path):
        target = self._safe_path(path)

        if not target.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not target.is_file():
            raise ValueError("Only files can be deleted.")

        target.unlink()

        return {
            "success": True,
            "action": "deleted",
            "path": str(target.relative_to(self.workspace)),
        }

    def list_files(self, path="."):
        target = self._safe_path(path)

        if not target.exists():
            raise FileNotFoundError(f"Directory not found: {path}")

        return [
            str(item.relative_to(self.workspace))
            for item in target.rglob("*")
            if item.is_file()
        ]