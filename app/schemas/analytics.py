from pydantic import BaseModel

class AnalyticsSummary(BaseModel):
    count: int
    amount: float | None = None
    available_quantity: float | None = None
