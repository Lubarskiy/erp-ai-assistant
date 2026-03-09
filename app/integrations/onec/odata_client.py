from __future__ import annotations

from typing import Any, Dict, Optional

from app.config import settings


class ODataClient:
    def __init__(self):
        self.base_url = settings.onec_base_url

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # В будущем здесь будет реальный OData-запрос в 1С.
        # Пока возвращаем безопасный stub-ответ без сетевого вызова.
        # При необходимости можно ввести отдельный whitelist для OData-путей.
        return {
            "status": "stub",
            "source": "onec_odata",
            "reason": "live 1C calls disabled",
            "base_url": self.base_url,
            "path": path,
            "params": params or {},
        }
