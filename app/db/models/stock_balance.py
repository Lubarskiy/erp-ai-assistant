from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class StockBalance(Base):
    __tablename__ = "stock_balances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    snapshot_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    product_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    warehouse: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quantity: Mapped[float] = mapped_column(Float, default=0)
    reserved_quantity: Mapped[float] = mapped_column(Float, default=0)
    available_quantity: Mapped[float] = mapped_column(Float, default=0)
