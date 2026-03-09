from app.integrations.onec.dto import StockBalanceDTO


def map_stock_balance(payload: dict) -> dict:
    product_code = str(payload.get("product_code") or "")
    available_quantity_raw = payload.get("available_quantity")
    try:
        available_quantity = float(available_quantity_raw or 0)
    except (TypeError, ValueError):
        available_quantity = 0.0

    dto = StockBalanceDTO(product_code=product_code, available_quantity=available_quantity)
    return {
        "product_code": dto.product_code,
        "available_quantity": dto.available_quantity,
    }
