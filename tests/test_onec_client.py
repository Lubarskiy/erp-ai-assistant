from app.integrations.onec.client import OneCClient

def test_onec_stub():
    client = OneCClient()
    assert client.fetch_stock_balance("A-1")["product_code"] == "A-1"
