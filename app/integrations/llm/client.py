class OpenAICompatibleClient:
    def chat(self, messages):
        return {"content": "stub"}

    def embeddings(self, text: str):
        return [0.0, 0.1, 0.2]
