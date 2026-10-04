import json

from .base import BaseAgent


class FixAgent(BaseAgent):
    name = "fix"

    def __init__(self, llm, filesystem):
        super().__init__(llm)
        self.filesystem = filesystem

    def run(self, files, error_report):
        """
        files: list of {"path": ..., "content": ...} - the CURRENT
               contents of every file involved (read fresh from disk,
               not just the ones that failed, so the model has full
               context of imports/usages).
        error_report: the dict returned by test_runner (stage,
               stdout, stderr, return_code, etc.)

        Returns a dict shaped like {"summary": ..., "files": [...]}
        on success, or None if the LLM response was empty or could
        not be parsed as valid JSON. Callers MUST check for None.
        """

        files_block = "\n\n".join(
            f"### FILE: {f['path']}\n{f['content']}"
            for f in files
        )

        error_text = error_report.get("stderr") or error_report.get("stdout") or ""
        error_text = self._truncate(error_text, max_chars=1500)

        prompt = f"""
You are a senior software engineer fixing a broken implementation.

The following files were generated and failed at the "{error_report.get('stage')}"
stage.

ERROR OUTPUT:
{error_text}

CURRENT FILES:
{files_block}

Fix ONLY what is necessary to resolve the error above. Do not rewrite
unrelated code. Preserve existing behavior and style wherever possible.

Return ONLY valid JSON with this structure:

{{
    "summary": "short explanation of what was wrong and what changed",
    "files": [
        {{
            "path": "relative/path/to/file.py",
            "content": "complete corrected file contents"
        }}
    ]
}}

Rules:

1. Only include files that actually needed changes.
2. Provide COMPLETE file contents for each included file, not a diff.
3. Paths must match the original paths exactly.
4. Do not include markdown.
5. Do not include explanations outside the JSON.
"""

        response = self.llm.generate(prompt)

        return self._parse_response(response)

    def execute(self, fix_result):
        """
        Writes the corrected file contents from a fix_result dict
        (as returned by run()) back to disk. Every file in a fix
        is an EDIT to an existing file, not a new file, so this
        always uses edit_file() rather than create_file().

        Safe to call with a dict that has an empty "files" list
        (e.g. if the model decided no files needed changes) - it
        will simply do nothing in that case.
        """
        for f in fix_result.get("files", []):
            self.filesystem.edit_file(f["path"], f["content"])

    @staticmethod
    def _truncate(text, max_chars):
        if len(text) <= max_chars:
            return text
        # Keep the END of the traceback (usually has the actual error),
        # not the beginning (usually setup noise).
        return "...[truncated]...\n" + text[-max_chars:]

    def _parse_response(self, response):
        """
        Parses the LLM's raw text response into a fix dict.

        Never raises on bad input. On any failure (empty response,
        malformed JSON, missing fields) it prints a diagnostic message
        and returns None, so the orchestrator's retry loop can treat
        it as "this attempt produced no usable fix" and try again
        instead of crashing.
        """
        if not response or not response.strip():
            print("Fix Agent returned an empty response.")
            return None

        cleaned = response.strip()

        # Strip a markdown code fence if the model wrapped its JSON in one,
        # e.g. ```json ... ``` or ``` ... ```
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            lines = lines[1:]  # drop the opening ``` or ```json line
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]  # drop the trailing ``` line
            cleaned = "\n".join(lines)

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(
                f"Fix Agent returned invalid JSON: {e}\n"
                f"Raw response (first 500 chars): {cleaned[:500]!r}"
            )
            return None

        if not isinstance(parsed, dict) or "files" not in parsed:
            print(
                "Fix Agent JSON was valid but missing the expected "
                f"'files' key. Parsed content: {parsed!r}"
            )
            return None

        return parsed