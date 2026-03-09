from app.integrations.onec.client import OneCClient


def test_onec_stub():
    client = OneCClient()
    result = client.fetch_stock_balance("A-1")
    assert result["intent"] == "stock_balance"
    assert result["data"]["product_code"] == "A-1"
