from __future__ import annotations

from typing import Any, Dict, Optional

from app.config import settings
from app.integrations.onec.queries import ALLOWED_ENDPOINTS


class HTTPServiceClient:
    def __init__(self, timeout: float = 5.0, max_retries: int = 1):
        self.base_url = settings.onec_http_service_url
        self.timeout = timeout
        self.max_retries = max_retries

    def _validate_path(self, path: str) -> None:
        if path not in ALLOWED_ENDPOINTS:
            raise ValueError(f"Path '{path}' is not allowed for 1C HTTP service")

    def _request(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Здесь в будущем будет реальный вызов httpx с таймаутом и ретраями.
        # Сейчас безопасный stub-ответ без обращения к 1С.
        attempt = 0
        while attempt <= self.max_retries:
            attempt += 1
            return {
                "status": "stub",
                "source": "onec_http_service",
                "reason": "live 1C calls disabled",
                "base_url": self.base_url,
                "path": path,
                "params": params or {},
                "attempt": attempt,
            }
        # Теоретически сюда не дойдём, но оставляем на будущее.
        return {
            "status": "error",
            "source": "onec_http_service",
            "reason": "unexpected_retry_flow",
            "path": path,
            "params": params or {},
        }

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._validate_path(path)
        return self._request(path, params=params)
