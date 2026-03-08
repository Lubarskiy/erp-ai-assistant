from datetime import date
from sqlalchemy.orm import Session

from app.db.repositories.chat_repo import ChatRepository
from app.schemas.chat import ChatCreateSessionResponse, ChatHistoryResponse, ChatMessageRequest, ChatMessageResponse
from app.services.analytics_service import AnalyticsService
from app.services.intent_service import IntentService


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ChatRepository(db)
        self.intent_service = IntentService()
        self.analytics_service = AnalyticsService(db)

    def create_session(self) -> ChatCreateSessionResponse:
        session = self.repo.create_session()
        return ChatCreateSessionResponse(session_id=session.id)

    def process_message(self, payload: ChatMessageRequest) -> ChatMessageResponse:
        self.repo.save_message(payload.session_id, "user", payload.text)

        intent_info = self.intent_service.detect(payload.text)
        intent = intent_info["intent"]

        data = None
        assistant_message = "AI response placeholder"

        if intent == "sales_summary":
            today = date.today()
            data = self.analytics_service.get_sales_summary(month=today.month, year=today.year)
            assistant_message = self._format_sales_summary_text(data)

        self.repo.save_message(payload.session_id, "assistant", assistant_message, intent)

        return ChatMessageResponse(
            session_id=payload.session_id,
            intent=intent,
            text_summary=assistant_message,
            data=data,
        )

    def get_history(self, session_id: int) -> ChatHistoryResponse:
        items = self.repo.get_history(session_id)
        return ChatHistoryResponse(session_id=session_id, items=items)

    def _format_sales_summary_text(self, data: dict | None) -> str:
        if not data:
            return "Продажи за текущий месяц отсутствуют — данных за период нет."

        def _fmt_amount(value: float | int | None) -> str:
            amount = float(value or 0)
            return f"{amount:,.2f}".replace(",", " ")

        total_sales = _fmt_amount(data.get("total_sales"))
        top_products = data.get("top_products") or []

        if not top_products:
            return f"Продажи за текущий месяц составили {total_sales}. Данных по отдельным товарам за период нет."

        parts: list[str] = []
        for item in top_products[:3]:
            name = item.get("product_name") or f"Товар {item.get('product_id')}"
            amount = _fmt_amount(item.get("amount"))
            parts.append(f"{name} — {amount}")

        leaders = ", ".join(parts)
        return f"Продажи за текущий месяц составили {total_sales}. Лидеры: {leaders}."
