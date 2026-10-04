from .base import BaseAgent


class CodeReviewAgent(BaseAgent):
    name = "code_review"

    def run(self, code, requirements, architecture):
        prompt = f"""
You are a senior software engineer performing a rigorous code review.

Review the following implementation against the requirements and
architecture.

REQUIREMENTS:
{requirements}

ARCHITECTURE:
{architecture}

CODE:
{code}

Analyze the code for:

1. Correctness
2. Requirements compliance
3. Architecture compliance
4. Bugs
5. Security vulnerabilities
6. Authentication problems
7. Authorization problems
8. Input validation
9. Error handling
10. Database problems
11. Performance problems
12. Scalability problems
13. Maintainability
14. Code quality
15. Testability

For every problem found, provide:

- Severity
- Location
- Problem
- Why it matters
- Recommended fix

Severity levels:

CRITICAL
HIGH
MEDIUM
LOW

At the end provide:

1. Critical issues
2. High-priority issues
3. Medium/low issues
4. Recommended changes
5. Whether the implementation is ready for testing

Do not rewrite the entire project unless necessary.
Focus on actionable engineering feedback.
"""

        return self.llm.generate(prompt)