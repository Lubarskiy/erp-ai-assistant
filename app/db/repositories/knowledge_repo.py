from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.models.knowledge_chunk import KnowledgeChunk


class KnowledgeRepository:
    def __init__(self, db: Session):
        self.db = db

    def search(self, query: str, limit: int = 5):
        q = self.db.query(KnowledgeChunk)
        text = (query or "").strip()
        if text:
            pattern = f"%{text}%"
            q = q.filter(
                or_(
                    KnowledgeChunk.content.ilike(pattern),
                    KnowledgeChunk.title.ilike(pattern),
                )
            )
        return q.order_by(KnowledgeChunk.id.desc()).limit(limit).all()
