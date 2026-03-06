from app.config import settings

class HTTPServiceClient:
    def __init__(self):
        self.base_url = settings.onec_http_service_url

    def get(self, path: str):
        return {"base_url": self.base_url, "path": path, "status": "stub"}
