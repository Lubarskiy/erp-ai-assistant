from sqlalchemy.orm import Session
from app.db.models.feedback import Feedback

class FeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs):
        item = Feedback(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
