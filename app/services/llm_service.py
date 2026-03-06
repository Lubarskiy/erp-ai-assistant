class LLMService:
    def classify_intent_llm(self, text: str) -> dict:
        return {"intent": "unknown", "confidence": 0.0}

    def explain_analytics(self, question: str, data) -> str:
        return f"Summary for: {question}"

    def answer_with_context(self, question: str, context) -> str:
        return "RAG response stub"
