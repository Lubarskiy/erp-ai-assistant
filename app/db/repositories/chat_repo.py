from sqlalchemy.orm import Session
from app.db.models.chat_message import ChatMessage
from app.db.models.chat_session import ChatSession

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self) -> ChatSession:
        session = ChatSession()
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def save_message(self, session_id: int, role: str, content: str, intent: str | None = None) -> ChatMessage:
        msg = ChatMessage(session_id=session_id, role=role, content=content, intent=intent)
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def get_history(self, session_id: int):
        return self.db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.id.asc()).all()
