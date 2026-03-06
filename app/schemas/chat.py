from pydantic import BaseModel

class ChatCreateSessionResponse(BaseModel):
    session_id: int

class ChatMessageRequest(BaseModel):
    session_id: int
    text: str

class ChatMessageResponse(BaseModel):
    session_id: int
    intent: str
    text_summary: str
    data: list | dict | None = None

class ChatHistoryItem(BaseModel):
    role: str
    content: str
    intent: str | None = None

    class Config:
        from_attributes = True

class ChatHistoryResponse(BaseModel):
    session_id: int
    items: list[ChatHistoryItem]
