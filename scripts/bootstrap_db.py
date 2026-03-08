from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.db.base import Base
from app.db.session import engine
from app.db.models import *  # noqa

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database bootstrapped.")
