"""Deterministic, repeatable synthetic dataset. This is infrastructure, NOT lab solutions.

Usage: uv run python scripts/seed.py --scale tiny --seed 20261101
Intentional data quality defects exist ONLY in analytics.raw_orders.
"""
from __future__ import annotations

import argparse
import os
import random
import uuid
from datetime import datetime, timedelta, timezone
from bisect import bisect_right
from decimal import Decimal
from typing import Any, Iterable, Iterator

import psycopg
from psycopg.types.json import Jsonb


ANCHOR = datetime(2026, 11, 1, 12, 0, 0, tzinfo=timezone.utc)
NAMESPACE = uuid.UUID("51f2c8ad-1b74-4f0c-b2e2-7ffea65be311")
TENANTS = (("caribe-demo", "Caribe Demo"), ("pacifico-demo", "Pacífico Demo"))
CATEGORIES = ("Electrónica", "Hogar", "Moda", "Deportes", "Oficina", "Jardín")
CHANNELS = ("organic", "paid", "social", "referral", "direct")
COUNTRIES = ("CR", "MX", "CO", "US", "PA")
SOURCES = ("google", "meta", "organic", "email", "direct")
NAMES = ("Ana", "Luis", "María", "Carlos", "Lucía", "José", "Paula", "Andrés", "Sofía", "Diego")
SURNAMES = ("Rojas", "Mora", "Vargas", "López", "Castro", "Soto", "Jiménez", "Salas")
SCALES = {
    "tiny": {"customers": 120, "products": 48, "orders": 600, "events": 2500, "raw": 35},
    "small": {"customers": 500, "products": 120, "orders": 2500, "events": 15000, "raw": 150},
    "medium": {"customers": 2000, "products": 250, "orders": 10000, "events": 100000, "raw": 500},
    "large": {"customers": 7000, "products": 500, "orders": 50000, "events": 500000, "raw": 2000},
}


def uid(*parts: object) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, ":".join(str(part) for part in parts))


def money(value: str | int | float | Decimal) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"))


def batches(source: Iterable[tuple[Any, ...]], chunk_size: int = 1000) -> Iterator[list[tuple[Any, ...]]]:
    chunk: list[tuple[Any, ...]] = []
    for row in source:
        chunk.append(row)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def insert_many(conn: psycopg.Connection[Any], sql: str, rows: Iterable[tuple[Any, ...]], label: str) -> None:
    count = 0
    with conn.cursor() as cur:
        for chunk in batches(rows):
            cur.executemany(sql, chunk)
            count += len(chunk)
    conn.commit()
    print(f"  {label}: procesadas {count:,} filas (conflictos ignorados)")


def connection_string() -> str:
    # psycopg accepts postgresql://, while the application uses SQLAlchemy's driver notation.
    url = os.getenv("DATABASE_URL")
    if not url:
        from mercadoops.config import get_settings
        url = get_settings().database_url
    if not url:
        raise RuntimeError("DATABASE_URL is missing. Copy .env.example to .env.")
    return str(url).replace("postgresql+psycopg://", "postgresql://", 1)


def seed_tenant(conn: psycopg.Connection[Any], slug: str, name: str, scale: dict[str, int], seed: int) -> None:
    tenant_id = uid("tenant", slug)
    rng = random.Random(f"{seed}-{slug}")
    print(f"TENANT: {slug} ({tenant_id})")
    insert_many(
        conn,
        "INSERT INTO core.tenants (id, slug, display_name) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
        [(tenant_id, slug, name)], "tenants",
    )

    categories = [(uid(slug, "category", x), tenant_id, x) for x in CATEGORIES]
    insert_many(conn,
        "INSERT INTO core.categories (id,tenant_id,name) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
        categories, "categories")

    customer_acquired: list[datetime] = []
    def customer_rows() -> Iterator[tuple[Any, ...]]:
        for i in range(scale["customers"]):
            acquired_at = ANCHOR - timedelta(days=rng.randint(0, 900), hours=rng.randint(0, 23))
            customer_acquired.append(acquired_at)
            yield (uid(slug, "customer", i), tenant_id,
                   f"cliente{i:06d}@{slug}.example", f"{rng.choice(NAMES)} {rng.choice(SURNAMES)}",
                   rng.choice(COUNTRIES), rng.choice(CHANNELS), acquired_at)
    insert_many(conn,
        """INSERT INTO core.customers
           (id,tenant_id,email,full_name,country_code,acquisition_channel,acquired_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
        customer_rows(), "customers")

    product_prices: list[Decimal] = []
    def product_rows() -> Iterator[tuple[Any, ...]]:
        for i in range(scale["products"]):
            price = money(rng.randint(10, 550))
            product_prices.append(price)
            yield (uid(slug, "product", i), tenant_id, categories[i % len(categories)][0],
                   f"{slug[:3].upper()}-{i:05d}", f"Artículo demostración {i:05d}",
                   price, money(price * Decimal("0.65")), i % 13 != 0)
    insert_many(conn,
        """INSERT INTO core.products
           (id,tenant_id,category_id,sku,name,unit_price,unit_cost,is_active)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
        product_rows(), "products")

    def inventory_rows() -> Iterator[tuple[Any, ...]]:
        for i in range(scale["products"]):
            yield (tenant_id, uid(slug, "product", i), 600 + (i * 19) % 1500, 0, 0)
    insert_many(conn,
        """INSERT INTO core.inventory
           (tenant_id,product_id,available_qty,reserved_qty,version)
           VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
        inventory_rows(), "inventory")

    # Pre-generate stable order shapes once; no answers to analytics exercises are materialized.
    # Ordered customers allow order timestamps to remain after their acquisition dates.
    eligible_sorted = sorted((when, index) for index, when in enumerate(customer_acquired))
    eligible_times = [when for when, _ in eligible_sorted]
    order_rows: list[tuple[Any, ...]] = []
    item_rows: list[tuple[Any, ...]] = []
    payment_rows: list[tuple[Any, ...]] = []
    refund_rows: list[tuple[Any, ...]] = []
    shipment_rows: list[tuple[Any, ...]] = []
    for i in range(scale["orders"]):
        order_id = uid(slug, "order", i)
        ordered_at = ANCHOR - timedelta(days=rng.randint(0, 729), minutes=rng.randint(0, 1439))
        eligible_count = bisect_right(eligible_times, ordered_at)
        if eligible_count == 0:
            # A rare edge case if no generated customer predates the order.
            ordered_at = eligible_times[0] + timedelta(minutes=1)
            eligible_count = 1
        customer_id = uid(slug, "customer", eligible_sorted[rng.randrange(eligible_count)][1])
        roll = rng.random()
        status = "cancelled" if roll < .06 else "pending" if roll < .18 else "paid" if roll < .33 else "completed"
        order_rows.append((order_id, tenant_id, customer_id, f"{slug[:3].upper()}-{i:08d}", status, ordered_at))
        total = Decimal("0.00")
        for j in range(rng.randint(1, 4)):
            product_index = rng.randrange(scale["products"])
            qty = rng.randint(1, 3)
            unit_price = product_prices[product_index]
            discount = money(unit_price * qty * (Decimal("0.10") if rng.random() < .13 else Decimal("0")))
            item_rows.append((uid(slug, "order-item", i, j), tenant_id, order_id,
                              uid(slug, "product", product_index), qty, unit_price, discount))
            total += money(unit_price * qty - discount)
        payment_id = uid(slug, "payment", i)
        payment_status = "captured" if status in ("paid", "completed") else ("failed" if status == "cancelled" else "pending")
        processed_at = ordered_at + timedelta(minutes=rng.randint(1, 20)) if payment_status == "captured" else None
        payment_rows.append((payment_id, tenant_id, order_id, total, payment_status,
                             rng.choice(("card", "transfer", "wallet")), processed_at))
        if payment_status == "captured" and rng.random() < .045:
            refund_rows.append((uid(slug, "refund", i), tenant_id, payment_id,
                                money(total * Decimal(str(rng.choice((.25, .5, 1.0))))),
                                "completed", ordered_at + timedelta(days=rng.randint(2, 15))))
        if status == "completed":
            shipped_at = ordered_at + timedelta(days=rng.randint(1, 3))
            shipment_rows.append((uid(slug, "shipment", i), tenant_id, order_id, "delivered",
                                  money(rng.choice((0, 5, 10, 15))), shipped_at,
                                  shipped_at + timedelta(days=rng.randint(1, 6))))
        elif status == "paid":
            shipment_rows.append((uid(slug, "shipment", i), tenant_id, order_id, "created",
                                  money(0), None, None))

    insert_many(conn,
        """INSERT INTO core.orders (id,tenant_id,customer_id,order_number,order_status,ordered_at)
           VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", order_rows, "orders")
    insert_many(conn,
        """INSERT INTO core.order_items
           (id,tenant_id,order_id,product_id,quantity,unit_price,discount_amount)
           VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", item_rows, "order_items")
    insert_many(conn,
        """INSERT INTO core.payments
           (id,tenant_id,order_id,amount,payment_status,payment_method,processed_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", payment_rows, "payments")
    insert_many(conn,
        """INSERT INTO core.refunds (id,tenant_id,payment_id,amount,refund_status,refunded_at)
           VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", refund_rows, "refunds")
    insert_many(conn,
        """INSERT INTO core.shipments
           (id,tenant_id,order_id,shipment_status,shipping_cost,shipped_at,delivered_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", shipment_rows, "shipments")

    def event_rows() -> Iterator[tuple[Any, ...]]:
        # Synthetic sessions with plausible event progression; each row has a stable UUID.
        path = ("page_view", "product_view", "add_to_cart", "checkout_started", "purchase")
        for i in range(scale["events"]):
            session_number = i // 5
            stage = i % 5
            # Not every session reaches purchase, intentionally creating dropoff.
            event_type = path[stage] if rng.random() < (1.0 - stage * .13) else "page_view"
            event_at = ANCHOR - timedelta(days=1 + session_number % 729) + timedelta(minutes=stage)
            eligible_count = bisect_right(eligible_times, event_at)
            if eligible_count == 0:
                event_at = eligible_times[0] + timedelta(minutes=stage + 1)
                eligible_count = 1
            customer_index = eligible_sorted[session_number % eligible_count][1]
            yield (uid(slug, "event", i), tenant_id,
                   uid(slug, "customer", customer_index),
                   uid(slug, "product", (session_number * 7) % scale["products"]),
                   uid(slug, "session", session_number), event_type,
                   event_at,
                   rng.choice(("mobile", "desktop", "tablet")), rng.choice(SOURCES),
                   Jsonb({"campaign": f"campaign-{session_number % 17}", "screen": stage}))
    insert_many(conn,
        """INSERT INTO events.web_events
           (id,tenant_id,customer_id,product_id,session_id,event_type,occurred_at,
            device_type,source,properties)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
        event_rows(), "web_events")

    def raw_rows() -> Iterator[tuple[Any, ...]]:
        for i in range(scale["raw"]):
            defect = i % 11
            payload: dict[str, object] = {
                "order_id": f"EXT-{i // 2 if defect == 0 else i}",
                "amount": str(money(rng.randint(10, 400))), "currency": "USD",
                "customer_email": f"import{i}@example.test", "placed_at": "2026-08-20T10:10:00Z",
            }
            if defect == 1:
                payload["amount"] = "not-a-number"
            elif defect == 2:
                payload.pop("customer_email")
            elif defect == 3:
                payload["currency"] = "???"
            elif defect == 4:
                payload["placed_at"] = "yesterday-ish"
            elif defect == 5:
                payload["amount"] = "-20.00"
            elif defect == 6:
                payload["customer_email"] = "bad-address"
            yield (uid(slug, "raw", i), tenant_id, "partner-api", payload["order_id"], Jsonb(payload))
    insert_many(conn,
        """INSERT INTO analytics.raw_orders
           (ingest_id,tenant_id,source_system,source_order_id,payload)
           VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", raw_rows(), "raw_orders")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed synthetic multi-tenant dataset")
    parser.add_argument("--scale", choices=sorted(SCALES), default="tiny")
    parser.add_argument("--seed", type=int, default=20261101)
    args = parser.parse_args()
    print(f"Scale={args.scale}; Seed={args.seed}; Anchor={ANCHOR.isoformat()}")
    print("NOTA: ejecuta primero las migraciones (alembic upgrade head).")
    with psycopg.connect(connection_string()) as conn:
        for slug, name in TENANTS:
            seed_tenant(conn, slug, name, SCALES[args.scale], args.seed)
    print("Seed complete. Repetir con la MISMA escala/seed no duplica filas.")
    print("Cambiar seed NO sustituye valores existentes. Subir scale puede añadir filas.")


if __name__ == "__main__":
    main()
