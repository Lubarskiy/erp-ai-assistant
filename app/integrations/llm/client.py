from __future__ import annotations

from typing import Any, Dict, List

import httpx

from app.config import settings


class LLMIntegrationError(Exception):
    """Base error for LLM integration issues."""


class OpenAICompatibleClient:
    def __init__(self) -> None:
        self.base_url = settings.llm_base_url.rstrip("/")
        self.api_key = settings.llm_api_key
        self.model = settings.llm_chat_model

    def chat(self, messages: List[Dict[str, Any]]) -> str:
        if not self.api_key or self.api_key == "your_key":
            raise LLMIntegrationError("LLM API key is not configured")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }

        try:
            resp = httpx.post(url, json=payload, headers=headers, timeout=15.0)
            resp.raise_for_status()
            data = resp.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise LLMIntegrationError(f"LLM HTTP error: {exc}") from exc

        try:
            choices = data.get("choices") or []
            if not choices:
                raise KeyError("choices is empty")
            message = choices[0].get("message") or {}
            content = message.get("content") or ""
            if not isinstance(content, str):
                raise TypeError("content is not a string")
            return content.strip()
        except Exception as exc:
            raise LLMIntegrationError(f"Unexpected LLM response format: {exc}") from exc

    def embeddings(self, text: str):
        # Not used in current flow; keep as stub.
        return [0.0, 0.1, 0.2]
