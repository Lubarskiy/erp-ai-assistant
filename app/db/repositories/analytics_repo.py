from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.product import Product
from app.db.models.sales_fact import SalesFact
from app.db.models.stock_balance import StockBalance


class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def sales_summary(self, month: int, year: int) -> dict:
        start = date(year, month, 1)
        if month == 12:
            end = date(year + 1, 1, 1)
        else:
            end = date(year, month + 1, 1)

        total_sales = (
            self.db.query(func.coalesce(func.sum(SalesFact.amount), 0))
            .filter(SalesFact.sale_date >= start, SalesFact.sale_date < end)
            .scalar()
        )

        top_rows = (
            self.db.query(
                SalesFact.product_id.label("product_id"),
                Product.name.label("product_name"),
                func.coalesce(func.sum(SalesFact.amount), 0).label("amount"),
            )
            .outerjoin(Product, Product.id == SalesFact.product_id)
            .filter(SalesFact.sale_date >= start, SalesFact.sale_date < end)
            .group_by(SalesFact.product_id, Product.name)
            .order_by(func.sum(SalesFact.amount).desc())
            .limit(10)
            .all()
        )

        top_products = [
            {
                "product_id": row.product_id,
                "product_name": row.product_name,
                "amount": float(row.amount or 0),
            }
            for row in top_rows
        ]

        return {"total_sales": float(total_sales or 0), "top_products": top_products}

    def stock_balance(self):
        rows = self.db.query(
            func.count(StockBalance.id),
            func.coalesce(func.sum(StockBalance.available_quantity), 0),
        ).one()
        return {"count": rows[0], "available_quantity": float(rows[1] or 0)}
