from pydantic import BaseModel

class KnowledgeSearchRequest(BaseModel):
    question: str

class KnowledgeItem(BaseModel):
    title: str | None = None
    content: str
