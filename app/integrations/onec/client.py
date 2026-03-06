from app.integrations.onec.odata_client import ODataClient
from app.integrations.onec.http_service_client import HTTPServiceClient

class OneCClient:
    def __init__(self):
        self.odata = ODataClient()
        self.http = HTTPServiceClient()

    def fetch_live(self, intent: str, params: dict):
        if intent == "stock_balance":
            return self.fetch_stock_balance(params.get("product_code", ""))
        if intent == "customer_info":
            return self.fetch_customer_card(params.get("customer_name", ""))
        return {"status": "unsupported", "intent": intent}

    def fetch_stock_balance(self, product_code: str):
        return {"product_code": product_code, "available_quantity": 0}

    def fetch_customer_card(self, customer_name: str):
        return {"customer_name": customer_name, "status": "stub"}

    def fetch_sales_summary(self):
        return {"status": "stub"}
