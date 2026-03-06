from app.core.enums import IntentEnum

class IntentService:
    KEYWORDS = {
        IntentEnum.sales_summary: ["продаж", "выручк", "sales"],
        IntentEnum.top_products: ["топ", "best", "товар"],
        IntentEnum.overdue_orders: ["просроч", "overdue", "заказ"],
        IntentEnum.stock_balance: ["остат", "balance", "склад"],
        IntentEnum.customer_info: ["контрагент", "customer", "клиент"],
        IntentEnum.knowledge_question: ["как", "регламент", "инструкция", "faq"],
    }

    def detect(self, text: str) -> dict:
        lowered = text.lower()
        for intent, words in self.KEYWORDS.items():
            if any(word in lowered for word in words):
                return {"intent": intent.value, "confidence": 0.8}
        return {"intent": IntentEnum.unknown.value, "confidence": 0.1}
