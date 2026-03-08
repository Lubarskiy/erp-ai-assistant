from datetime import datetime, timedelta, timezone
from typing import Optional
import hashlib

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.db.session import get_db
from app.db.repositories.user_repo import UserRepository


bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    data = (settings.secret_key + password).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def verify_password(plain_password: str, password_hash: str) -> bool:
    return hash_password(plain_password) == password_hash


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing token")
    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    repo = UserRepository(db)
    user = repo.get_by_username(payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
