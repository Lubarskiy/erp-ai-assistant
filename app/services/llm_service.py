from __future__ import annotations

from app.integrations.llm.client import LLMIntegrationError, OpenAICompatibleClient
from app.services.prompt_service import SYSTEM_PROMPT


class LLMService:
    def __init__(self) -> None:
        self.client = OpenAICompatibleClient()

    def classify_intent_llm(self, text: str) -> dict:
        return {"intent": "unknown", "confidence": 0.0}

    def explain_analytics(self, question: str, data) -> str:
        return f"Summary for: {question}"

    def answer_with_context(self, question: str, context: str) -> str:
        context = (context or "").strip()
        # MVP ограничение длины контекста
        if len(context) > 4000:
            context = context[:4000]

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Вопрос:\n"
                    f"{question}\n\n"
                    "Контекст:\n"
                    f"{context}\n\n"
                    "Ответь кратко, деловым стилем, по-русски, опираясь только на контекст. "
                    "Если в контексте нет ответа, честно напиши, что по этому вопросу нет информации."
                ),
            },
        ]

        try:
            answer = self.client.chat(messages)
        except LLMIntegrationError:
            return ""

        return answer.strip() if answer else ""
