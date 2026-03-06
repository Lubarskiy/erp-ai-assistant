from dataclasses import dataclass

@dataclass
class StockBalanceDTO:
    product_code: str
    available_quantity: float = 0.0
