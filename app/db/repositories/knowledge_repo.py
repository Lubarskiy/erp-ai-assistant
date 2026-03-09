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

        tokens: list[str] = []
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

        # если нет токенов — просто последние чанки без дополнительного ранжирования
        if not tokens:
            return q.order_by(KnowledgeChunk.id.desc()).limit(limit).all()

        # забираем небольшой пул кандидатов и ранжируем в Python
        candidates = q.order_by(KnowledgeChunk.id.desc()).limit(limit * 5).all()

        def score(chunk: KnowledgeChunk) -> int:
            title = (chunk.title or "").lower()
            content = (chunk.content or "").lower()
            s = 0
            for token in tokens:
                if token in title:
                    s += 2
                if token in content:
                    s += 1
            return s

        ranked = sorted(
            candidates,
            key=lambda c: (score(c), c.id or 0),
            reverse=True,
        )
        return ranked[:limit]
