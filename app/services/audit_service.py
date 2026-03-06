from sqlalchemy.orm import Session
from app.db.repositories.audit_repo import AuditRepository

class AuditService:
    def __init__(self, db: Session):
        self.repo = AuditRepository(db)

    def log(self, **kwargs):
        return self.repo.create(**kwargs)
