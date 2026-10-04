# agents/base.py
class BaseAgent:
    name = None
    def __init__(self, llm):
        self.llm = llm
    def run(self, context):
        raise NotImplementedError