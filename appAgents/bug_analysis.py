from .base import BaseAgent


class BugAnalysisAgent(BaseAgent):
    name = "bug_analysis"

    def run(self, test_results, code, requirements):
        prompt = f"""
You are a senior debugging engineer.

Analyze the test results and identify the underlying software problems.

REQUIREMENTS:
{requirements}

CODE:
{code}

TEST RESULTS:
{test_results}

For every failure:

1. Identify the failing test
2. Identify the likely root cause
3. Identify the affected component
4. Determine severity
5. Explain why the failure occurred
6. Recommend a precise fix
7. Identify possible side effects
8. Recommend regression tests

Severity levels:

CRITICAL
HIGH
MEDIUM
LOW

Do not guess when evidence is insufficient.

Clearly distinguish:
- Confirmed problem
- Likely root cause
- Possible cause

Return a structured debugging report.
"""

        return self.llm.generate(prompt)