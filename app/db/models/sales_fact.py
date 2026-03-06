from datetime import date
from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class SalesFact(Base):
    __tablename__ = "sales_facts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_date: Mapped[date] = mapped_column(Date)
    manager_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    customer_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    product_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quantity: Mapped[float] = mapped_column(Float, default=0)
    amount: Mapped[float] = mapped_column(Float, default=0)
    region: Mapped[str | None] = mapped_column(String(255), nullable=True)
    warehouse: Mapped[str | None] = mapped_column(String(255), nullable=True)
