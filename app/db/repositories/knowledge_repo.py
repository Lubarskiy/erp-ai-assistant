import re

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
            raw_tokens = re.split(r"\s+", text)
            tokens = [t for t in raw_tokens if len(t) >= 3]

            if tokens:
                conditions = []
                for token in tokens:
                    pattern = f"%{token}%"
                    conditions.append(KnowledgeChunk.content.ilike(pattern))
                    conditions.append(KnowledgeChunk.title.ilike(pattern))

                q = q.filter(or_(*conditions))

        return q.order_by(KnowledgeChunk.id.desc()).limit(limit).all()
