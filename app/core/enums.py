from enum import Enum

class IntentEnum(str, Enum):
    sales_summary = "sales_summary"
    top_products = "top_products"
    overdue_orders = "overdue_orders"
    stock_balance = "stock_balance"
    customer_info = "customer_info"
    knowledge_question = "knowledge_question"
    unknown = "unknown"
