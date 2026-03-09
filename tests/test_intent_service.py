from app.services.intent_service import IntentService


def test_detect_sales():
    svc = IntentService()
    result = svc.detect("Покажи продажи за февраль")
    assert result["intent"] == "sales_summary"


def test_detect_knowledge_question_refund():
    svc = IntentService()
    result = svc.detect("как оформить возврат товара")
    assert result["intent"] == "knowledge_question"


def test_detect_top_products_simple():
    svc = IntentService()
    result = svc.detect("покажи топ товаров")
    assert result["intent"] == "top_products"


def test_detect_top_products_best_sellers():
    svc = IntentService()
    result = svc.detect("какие товары самые продаваемые")
    assert result["intent"] == "top_products"


def test_detect_knowledge_question_regulation():
    svc = IntentService()
    result = svc.detect("регламент возврата")
    assert result["intent"] == "knowledge_question"
