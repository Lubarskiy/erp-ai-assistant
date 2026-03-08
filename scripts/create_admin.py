from pathlib import Path
import sys

from sqlalchemy.orm import Session

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.core.security import hash_password
from app.db.models.user import User
from app.db.session import SessionLocal


def create_admin(db: Session) -> None:
    username = "admin"
    password = "admin"

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        print("Admin user already exists")
        return

    user = User(
        username=username,
        password_hash=hash_password(password),
        role="admin",
        is_active=True,
    )
    db.add(user)
    db.commit()
    print("Admin user created with username=admin, password=admin")


def main() -> None:
    db = SessionLocal()
    try:
        create_admin(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
