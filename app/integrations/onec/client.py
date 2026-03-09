from app.integrations.onec.odata_client import ODataClient
from app.integrations.onec.http_service_client import HTTPServiceClient


class OneCIntegrationError(Exception):
    """Base error for 1C integration issues."""


class UnsupportedIntentError(OneCIntegrationError):
    """Raised when OneCClient.fetch_live is called with unsupported intent."""

    def __init__(self, intent: str) -> None:
        super().__init__(f"Unsupported 1C live intent: {intent}")
        self.intent = intent


class OneCClient:
    def __init__(self):
        self.odata = ODataClient()
        self.http = HTTPServiceClient()

    def fetch_live(self, intent: str, params: dict):
        params = params or {}

        if intent == "stock_balance":
            return self.fetch_stock_balance(product_code=params.get("product_code"))
        if intent == "customer_info":
            return self.fetch_customer_card(
                customer_name=params.get("customer_name"),
                customer_id=params.get("customer_id"),
            )
        if intent == "sales_summary":
            return self.fetch_sales_summary(
                month=params.get("month"),
                year=params.get("year"),
            )

        raise UnsupportedIntentError(intent)

    def fetch_stock_balance(self, product_code: str | None):
        return {
            "status": "stub",
            "intent": "stock_balance",
            "data": {
                "product_code": product_code,
                "available_quantity": 0.0,
                "source": "onec_live_disabled",
            },
        }

    def fetch_customer_card(
        self,
        customer_name: str | None = None,
        customer_id: str | None = None,
    ):
        return {
            "status": "stub",
            "intent": "customer_info",
            "data": {
                "customer_name": customer_name,
                "customer_id": customer_id,
                "details": None,
                "source": "onec_live_disabled",
            },
        }

    def fetch_sales_summary(self, month: int | None, year: int | None):
        return {
            "status": "stub",
            "intent": "sales_summary",
            "data": {
                "month": month,
                "year": year,
                "total_sales": None,
                "source": "onec_live_disabled",
            },
        }
