# 1C Integration

Используются:
- OData для чтения сущностей
- HTTP services для агрегатов и контролируемых endpoint'ов

## Белый список endpoint
- /sales-summary
- /top-products
- /stock-balance
- /customer-card
- /overdue-orders

## Безопасность
- service account: svc_ai
- read-only сценарии для MVP
- все вызовы логируются
