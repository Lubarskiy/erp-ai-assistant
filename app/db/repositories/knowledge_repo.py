from sqlalchemy.orm import Session
from app.db.models.knowledge_chunk import KnowledgeChunk

class KnowledgeRepository:
    def __init__(self, db: Session):
        self.db = db

    def search(self, limit: int = 5):
        return self.db.query(KnowledgeChunk).limit(limit).all()
