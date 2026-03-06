from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import ChatCreateSessionResponse, ChatHistoryResponse, ChatMessageRequest, ChatMessageResponse
from app.services.chat_service import ChatService

router = APIRouter()

@router.post("/new-session", response_model=ChatCreateSessionResponse)
def new_session(db: Session = Depends(get_db)):
    service = ChatService(db)
    return service.create_session()

@router.post("/message", response_model=ChatMessageResponse)
def send_message(payload: ChatMessageRequest, db: Session = Depends(get_db)):
    service = ChatService(db)
    return service.process_message(payload)

@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
def history(session_id: int, db: Session = Depends(get_db)):
    service = ChatService(db)
    return service.get_history(session_id)
