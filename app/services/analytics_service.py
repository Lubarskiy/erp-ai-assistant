from sqlalchemy.orm import Session
from app.db.repositories.analytics_repo import AnalyticsRepository

class AnalyticsService:
    def __init__(self, db: Session):
        self.repo = AnalyticsRepository(db)

    def get_sales_summary(self):
        return self.repo.sales_summary()

    def get_stock_balance(self):
        return self.repo.stock_balance()
