from app.core.enums import IntentEnum


class IntentService:
    KEYWORDS = {
        # сначала вопросы/регламенты
        IntentEnum.knowledge_question: [
            "как оформить",
            "как сделать",
            "как вернуть",
            "регламент",
            "инструкция",
            "возврат",
            "faq",
        ],
        IntentEnum.sales_summary: ["продаж", "выручк", "sales"],
        # более точные маркеры для топов
        IntentEnum.top_products: [
            "топ",
            "лидер",
            "лучшие товар",
            "самые продаваем",
            "best seller",
        ],
        IntentEnum.overdue_orders: ["просроч", "overdue", "заказ"],
        IntentEnum.stock_balance: ["остат", "balance", "склад"],
        IntentEnum.customer_info: ["контрагент", "customer", "клиент"],
    }

    def detect(self, text: str) -> dict:
        lowered = text.lower()
        for intent, words in self.KEYWORDS.items():
            if any(word in lowered for word in words):
                return {"intent": intent.value, "confidence": 0.8}
        return {"intent": IntentEnum.unknown.value, "confidence": 0.1}
