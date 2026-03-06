from app.services.intent_service import IntentService

def test_detect_sales():
    svc = IntentService()
    result = svc.detect("Покажи продажи за февраль")
    assert result["intent"] == "sales_summary"
