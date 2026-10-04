import json

from .base import BaseAgent


class TestingAgent(BaseAgent):
    name = "testing"

    def __init__(self, llm, filesystem):
        super().__init__(llm)
        self.filesystem = filesystem

    def run(self, files, requirements):
        files_block = "\n\n".join(
            f"### FILE: {f['path']}\n{f['content']}"
            for f in files
        )

        prompt = f"""
You are a senior test engineer writing pytest tests for the
following implementation.

REQUIREMENTS:
{requirements}

SOURCE FILES (this is the ONLY code that exists — do not invent
functions, classes, or files that are not shown below):
{files_block}

Rules:

1. Only import functions/classes that are ACTUALLY DEFINED in the
   source files shown above. Before writing any import, find the
   exact file where that name is defined and import it from there.
2. Do not assume a function exists just because the requirements
   mention a feature. If the source files don't implement it, do
   not write a test for it.
3. Every import must be of the form:
   from <module_name_without_.py> import <exact_name_as_defined>
4. Use pytest-style test functions (def test_...():), not classes.
5. Test both valid inputs (should succeed) and invalid inputs
   (should raise the appropriate exception), based on what the
   source code actually does — check the code's own validation
   logic, don't guess.
6. Do not include markdown.
7. Do not include explanations outside the JSON.

Return ONLY valid JSON with this structure:

{{
    "summary": "short description of what is being tested",
    "files": [
        {{
            "path": "tests.py",
            "content": "complete pytest file contents"
        }}
    ]
}}
"""

        response = self.llm.generate(prompt)
        return self._parse_response(response)

    def _parse_response(self, response):
        response = response.strip()

        if response.startswith("```"):
            lines = response.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response = "\n".join(lines).strip()

        try:
            data = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Testing Agent returned invalid JSON: {exc}")

        if "files" not in data:
            raise ValueError("Testing Agent response does not contain 'files'.")

        return data

    def execute(self, test_result):
        results = []
        for file_data in test_result["files"]:
            path = file_data["path"]
            content = file_data["content"]
            result = self.filesystem.create_file(path, content)
            results.append(result)
        return results