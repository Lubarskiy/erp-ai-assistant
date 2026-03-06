from sqlalchemy.orm import Session
from app.db.models.audit_log import AuditLog

class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs):
        item = AuditLog(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
