from pydantic import BaseModel

class AnalyticsSummary(BaseModel):
    count: int
    amount: float | None = None
    available_quantity: float | None = None


class SalesSummaryTopProduct(BaseModel):
    product_id: int | None
    amount: float


class SalesSummaryResponse(BaseModel):
    total_sales: float
    top_products: list[SalesSummaryTopProduct]
