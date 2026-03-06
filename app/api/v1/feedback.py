from fastapi import APIRouter
from app.schemas.feedback import FeedbackCreate

router = APIRouter()

@router.post("")
def create_feedback(payload: FeedbackCreate):
    return {"status": "accepted", "payload": payload.model_dump()}
