import httpx
from app.config import settings

class ODataClient:
    def __init__(self):
        self.base_url = settings.onec_base_url

    def get(self, path: str):
        # placeholder for next prompt steps
        return {"base_url": self.base_url, "path": path, "status": "stub"}
