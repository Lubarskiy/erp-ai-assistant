from sqlalchemy.orm import Session

from app.db.repositories.chat_repo import ChatRepository
from app.schemas.chat import ChatCreateSessionResponse, ChatHistoryResponse, ChatMessageRequest, ChatMessageResponse
from app.services.intent_service import IntentService


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ChatRepository(db)
        self.intent_service = IntentService()

    def create_session(self) -> ChatCreateSessionResponse:
        session = self.repo.create_session()
        return ChatCreateSessionResponse(session_id=session.id)

    def process_message(self, payload: ChatMessageRequest) -> ChatMessageResponse:
        self.repo.save_message(payload.session_id, "user", payload.text)

        intent_info = self.intent_service.detect(payload.text)
        intent = intent_info["intent"]

        assistant_message = "AI response placeholder"

        self.repo.save_message(payload.session_id, "assistant", assistant_message, intent)

        return ChatMessageResponse(
            session_id=payload.session_id,
            intent=intent,
            text_summary=assistant_message,
            data=None,
        )

    def get_history(self, session_id: int) -> ChatHistoryResponse:
        items = self.repo.get_history(session_id)
        return ChatHistoryResponse(session_id=session_id, items=items)
