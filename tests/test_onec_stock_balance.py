from app.integrations.onec.client import OneCClient, OneCIntegrationError
from app.integrations.onec.mappers import map_stock_balance


def test_fetch_stock_balance_fallback_stub_on_error():
    client = OneCClient()

    class FailingHTTP:
        def get(self, path, params=None):
            raise OneCIntegrationError("test failure")

    client.http = FailingHTTP()
    res = client.fetch_stock_balance("A-1")

    assert res["status"] == "stub"
    assert res["intent"] == "stock_balance"
    assert res["data"]["product_code"] == "A-1"
    assert res["data"]["available_quantity"] == 0.0


def test_map_stock_balance_simple_payload():
    payload = {"product_code": "A-123", "available_quantity": 15}
    mapped = map_stock_balance(payload)

    assert mapped["product_code"] == "A-123"
    assert mapped["available_quantity"] == 15.0

