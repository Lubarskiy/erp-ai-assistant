from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    message_id: int | None = None
    user_id: int | None = None
    score: str = "like"
    comment: str | None = None
