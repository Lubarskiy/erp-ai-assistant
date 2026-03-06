from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.models.sales_fact import SalesFact
from app.db.models.stock_balance import StockBalance

class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def sales_summary(self):
        rows = self.db.query(func.count(SalesFact.id), func.coalesce(func.sum(SalesFact.amount), 0)).one()
        return {"count": rows[0], "amount": float(rows[1] or 0)}

    def stock_balance(self):
        rows = self.db.query(func.count(StockBalance.id), func.coalesce(func.sum(StockBalance.available_quantity), 0)).one()
        return {"count": rows[0], "available_quantity": float(rows[1] or 0)}
