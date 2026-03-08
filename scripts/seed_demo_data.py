from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path
import sys

from sqlalchemy.orm import Session

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.db.models.product import Product
from app.db.models.sales_fact import SalesFact
from app.db.session import SessionLocal


PRODUCT_NAMES = [
    "Arctic Jacket",
    "Nordic Coat",
    "Storm Down Jacket",
    "Urban Parka",
    "Alpine Vest",
]


def ensure_products(db: Session) -> list[Product]:
    existing = (
        db.query(Product)
        .filter(Product.name.in_(PRODUCT_NAMES))
        .order_by(Product.id.asc())
        .all()
    )
    if len(existing) == len(PRODUCT_NAMES):
        return existing

    created: list[Product] = []
    for idx, name in enumerate(PRODUCT_NAMES, start=1):
        code = f"SKU{idx:03d}"
        product = Product(
            code=code,
            name=name,
            category="Outerwear",
            unit="pcs",
            is_active=True,
        )
        db.add(product)
        created.append(product)

    db.commit()
    for p in created:
        db.refresh(p)

    return existing + created


def seed_sales_facts(db: Session, products: list[Product]) -> None:
    # Не дублируем данные, если продажи уже есть
    existing_count = db.query(SalesFact).count()
    if existing_count > 0:
        print(f"SalesFact already has {existing_count} rows, skipping seeding.")
        return

    if not products:
        print("No products found for seeding sales facts.")
        return

    today = date.today()
    num_rows = random.randint(50, 100)
    rows: list[SalesFact] = []

    for _ in range(num_rows):
        product = random.choice(products)
        days_ago = random.randint(0, 59)
        sale_date = today - timedelta(days=days_ago)
        amount = random.uniform(1000, 10000)
        quantity = round(amount / 1000, 2)

        rows.append(
            SalesFact(
                sale_date=sale_date,
                product_id=product.id,
                quantity=quantity,
                amount=amount,
                region=None,
                warehouse=None,
            )
        )

    db.add_all(rows)
    db.commit()
    print(f"Inserted {num_rows} demo sales_fact rows.")


def seed_demo_data(db: Session) -> None:
    products = ensure_products(db)
    seed_sales_facts(db, products)


def main() -> None:
    db = SessionLocal()
    try:
        seed_demo_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
