from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.db.repositories.user_repo import UserRepository

class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def login(self, username: str, password: str) -> str | None:
        user = self.repo.get_by_username(username)
        if not user:
            return None
        return create_access_token(username)
