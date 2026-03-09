from sqlalchemy.orm import Session

from app.db.repositories.knowledge_repo import KnowledgeRepository


class RagService:
    def __init__(self, db: Session):
        self.repo = KnowledgeRepository(db)

    def search(self, question: str, limit: int = 5):
        return self.repo.search(query=question, limit=limit)
