from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.knowledge import KnowledgeItem, KnowledgeSearchRequest, KnowledgeSearchResponse
from app.services.rag_service import RagService


router = APIRouter()


@router.post("/search", response_model=KnowledgeSearchResponse)
def search(payload: KnowledgeSearchRequest, db: Session = Depends(get_db)):
    service = RagService(db)
    chunks = service.search(payload.question, limit=5)
    items = [
        KnowledgeItem(title=chunk.title, content=chunk.content)
        for chunk in chunks
    ]
    return KnowledgeSearchResponse(items=items)


@router.post("/reindex")
def reindex():
    return {"status": "queued"}
