# agents/llm.py
import requests

class LocalLLM:
    def __init__(self, model="qwen3:4b", base_url="http://localhost:11434", num_ctx=8192):
        self.model = model
        self.base_url = base_url
        self.num_ctx = num_ctx

    def generate(self, prompt):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_ctx": self.num_ctx
                }
            }
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("response", "")

        if not text.strip():
            raise ValueError(
                "LLM returned an empty response. This usually means the "
                "prompt exceeded the model's context window, or Ollama "
                "hit an internal error. Try increasing num_ctx or "
                "shortening the prompt (e.g. truncate long stdout/stderr "
                "before including it)."
            )

        return text