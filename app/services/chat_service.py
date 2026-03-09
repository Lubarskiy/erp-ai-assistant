from datetime import date
from sqlalchemy.orm import Session

from app.db.repositories.chat_repo import ChatRepository
from app.integrations.onec.client import OneCClient, OneCIntegrationError
from app.schemas.chat import ChatCreateSessionResponse, ChatHistoryResponse, ChatMessageRequest, ChatMessageResponse
from app.services.analytics_service import AnalyticsService
from app.services.intent_service import IntentService
from app.services.llm_service import LLMService
from app.services.rag_service import RagService


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ChatRepository(db)
        self.intent_service = IntentService()
        self.analytics_service = AnalyticsService(db)
        self.rag_service = RagService(db)
        self.llm_service = LLMService()
        self.onec_client = OneCClient()

    def create_session(self) -> ChatCreateSessionResponse:
        session = self.repo.create_session()
        return ChatCreateSessionResponse(session_id=session.id)

    def process_message(self, payload: ChatMessageRequest) -> ChatMessageResponse:
        self.repo.save_message(payload.session_id, "user", payload.text)

        intent_info = self.intent_service.detect(payload.text)
        intent = intent_info["intent"]

        data = None
        assistant_message = "AI response placeholder"

        try:
            if intent == "sales_summary":
                month, year, period_label = self._detect_sales_period(payload.text)
                data = self.analytics_service.get_sales_summary(month=month, year=year)
                assistant_message = self._format_sales_summary_text(data, period_label)
            elif intent == "knowledge_question":
                chunks = self.rag_service.search(payload.text, limit=3)
                if chunks:
                    # Готовим data в прежнем формате
                    data = {
                        "items": [
                            {"title": chunk.title, "content": chunk.content}
                            for chunk in chunks
                        ]
                    }

                    # Fallback-краткое резюме по чанкам
                    lines: list[str] = []
                    for chunk in chunks[:2]:
                        title = (chunk.title or "").strip() or "Фрагмент"
                        first_line = (chunk.content or "").strip().splitlines()[0] if (chunk.content or "").strip() else ""
                        snippet = first_line.strip()
                        if len(snippet) > 160:
                            snippet = snippet[:157].rstrip() + "..."
                        if snippet:
                            lines.append(f"{title}: {snippet}")
                        else:
                            lines.append(title)
                    bullet_lines = "\n".join(f"- {line}" for line in lines)
                    fallback_summary = f"Нашёл в базе знаний следующие материалы:\n{bullet_lines}"

                    # Собираем контекст для LLM
                    context_parts: list[str] = []
                    for chunk in chunks:
                        title = (chunk.title or "").strip() or "Фрагмент"
                        context_parts.append(f"### {title}\n{chunk.content}")
                    context = "\n\n".join(context_parts)

                    llm_answer = self.llm_service.answer_with_context(payload.text, context)
                    assistant_message = llm_answer or fallback_summary
                else:
                    assistant_message = "В базе знаний ничего не найдено по этому запросу."
                    data = {"items": []}
            elif intent == "stock_balance":
                product_code = self._extract_product_code(payload.text)
                data = self.onec_client.fetch_live(
                    "stock_balance",
                    {"product_code": product_code},
                )
                if data and data.get("status") == "live" and data.get("data"):
                    info = data["data"]
                    code = info.get("product_code") or product_code
                    qty = info.get("available_quantity")
                    assistant_message = (
                        f"По товару {code} в 1С найден остаток {qty} единиц."
                    )
                else:
                    if product_code:
                        assistant_message = (
                            f"Онлайн-запрос остатков по товару {product_code} "
                            f"выполняется в режиме заглушки, данные 1С сейчас недоступны."
                        )
                    else:
                        assistant_message = (
                            "Онлайн-запрос остатков выполняется в режиме заглушки, "
                            "код товара не указан."
                        )
            elif intent == "customer_info":
                customer_name = self._extract_customer_name(payload.text)
                data = self.onec_client.fetch_live(
                    "customer_info",
                    {"customer_name": customer_name},
                )
                if customer_name:
                    assistant_message = (
                        f"Онлайн-запрос карточки клиента «{customer_name}» выполняется "
                        f"в режиме заглушки, данные 1С сейчас недоступны."
                    )
                else:
                    assistant_message = (
                        "Онлайн-запрос карточки клиента выполняется в режиме заглушки, "
                        "имя клиента не распознано."
                    )
        except OneCIntegrationError as exc:
            assistant_message = (
                "Во время обращения к онлайн-данным 1С произошла ошибка интеграции. "
                "Сейчас используется офлайн-ответ."
            )
            data = {
                "status": "error",
                "source": "onec_integration",
                "reason": str(exc),
            }

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

    def _format_sales_summary_text(self, data: dict | None, period_label: str) -> str:
        if not data:
            return f"Продажи {period_label} отсутствуют — данных за период нет."

        def _fmt_amount(value: float | int | None) -> str:
            amount = float(value or 0)
            return f"{amount:,.2f}".replace(",", " ")

        total_sales = _fmt_amount(data.get("total_sales"))
        top_products = data.get("top_products") or []

        if not top_products:
            return f"Продажи {period_label} составили {total_sales}. Данных по отдельным товарам за период нет."

        parts: list[str] = []
        for item in top_products[:3]:
            name = item.get("product_name") or f"Товар {item.get('product_id')}"
            amount = _fmt_amount(item.get("amount"))
            parts.append(f"{name} — {amount}")

        leaders = ", ".join(parts)
        return f"Продажи {period_label} составили {total_sales}. Лидеры: {leaders}."

    def _detect_sales_period(self, text: str) -> tuple[int, int, str]:
        today = date.today()
        lowered = text.lower()

        if "за январь" in lowered:
            return 1, today.year, "за январь"
        if "за февраль" in lowered:
            return 2, today.year, "за февраль"
        if "за март" in lowered:
            return 3, today.year, "за март"
        if "за этот месяц" in lowered or "за текущий месяц" in lowered:
            return today.month, today.year, "за текущий месяц"

        return today.month, today.year, "за текущий месяц"

    def _extract_product_code(self, text: str) -> str | None:
        for raw in text.split():
            token = raw.strip(",.;:!?'\"()[]{}")
            if any(ch.isdigit() for ch in token):
                return token
        return None

    def _extract_customer_name(self, text: str) -> str | None:
        lowered = text.lower()
        marker = "клиент"
        idx = lowered.find(marker)
        if idx == -1:
            return None
        after = text[idx + len(marker) :].strip()
        return after or None
