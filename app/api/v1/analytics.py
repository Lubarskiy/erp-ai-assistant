from fastapi import APIRouter
router = APIRouter()

@router.get("/sales-summary")
def sales_summary():
    return {"items": []}

@router.get("/top-products")
def top_products():
    return {"items": []}

@router.get("/overdue-orders")
def overdue_orders():
    return {"items": []}

@router.get("/stock-balance")
def stock_balance():
    return {"items": []}
