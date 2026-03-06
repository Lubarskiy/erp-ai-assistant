from sqlalchemy.orm import Session

from app.db.repositories.chat_repo import ChatRepository
from app.schemas.chat import ChatCreateSessionResponse, ChatHistoryResponse, ChatMessageResponse
from app.services.analytics_service import AnalyticsService
from app.services.intent_service import IntentService

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ChatRepository(db)
        self.intent_service = IntentService()
        self.analytics_service = AnalyticsService(db)

    def create_session(self):
        session = self.repo.create_session()
        return ChatCreateSessionResponse(session_id=session.id)

    def process_message(self, payload):
        self.repo.save_message(payload.session_id, "user", payload.text)
        intent_info = self.intent_service.detect(payload.text)
        intent = intent_info["intent"]

        if intent == "sales_summary":
            data = self.analytics_service.get_sales_summary()
            text_summary = "Сводка по продажам подготовлена."
        elif intent == "stock_balance":
            data = self.analytics_service.get_stock_balance()
            text_summary = "Сводка по остаткам подготовлена."
        else:
            data = None
            text_summary = "Пока это заглушка. Следующим шагом добавим полноценную оркестрацию."

        self.repo.save_message(payload.session_id, "assistant", text_summary, intent)
        return ChatMessageResponse(
            session_id=payload.session_id,
            intent=intent,
            text_summary=text_summary,
            data=data,
        )

    def get_history(self, session_id: int):
        items = self.repo.get_history(session_id)
        return ChatHistoryResponse(session_id=session_id, items=items)
