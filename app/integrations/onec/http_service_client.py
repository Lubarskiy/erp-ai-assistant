from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from app.config import settings
from app.integrations.onec.queries import ALLOWED_ENDPOINTS


class HTTPServiceClient:
    def __init__(self, timeout: float = 5.0, max_retries: int = 1):
        self.base_url = settings.onec_http_service_url
        self.timeout = timeout
        self.max_retries = max_retries

    def _validate_path(self, path: str) -> None:
        from app.integrations.onec.client import OneCIntegrationError

        if path not in ALLOWED_ENDPOINTS:
            raise OneCIntegrationError(f"Path '{path}' is not allowed for 1C HTTP service")

    def _request(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        from app.integrations.onec.client import OneCIntegrationError

        url = f"{self.base_url}{path}"
        attempt = 0
        last_error: Exception | None = None

        while attempt <= self.max_retries:
            attempt += 1
            try:
                resp = httpx.get(
                    url,
                    params=params,
                    timeout=self.timeout,
                    auth=(settings.onec_username, settings.onec_password),
                )
                if resp.status_code != 200:
                    raise OneCIntegrationError(
                        f"1C HTTP service responded with status {resp.status_code}"
                    )
                try:
                    data = resp.json()
                except ValueError as exc:  # JSON decode error
                    raise OneCIntegrationError(
                        "Failed to decode 1C HTTP service response as JSON"
                    ) from exc
                if not isinstance(data, dict):
                    raise OneCIntegrationError("Unexpected 1C HTTP service payload type")
                return data
            except (httpx.HTTPError, OneCIntegrationError) as exc:
                last_error = exc
                break

        message = str(last_error) if last_error else "Unknown HTTP error"
        raise OneCIntegrationError(f"1C HTTP service request failed: {message}")

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._validate_path(path)
        return self._request(path, params=params)
