"""Non-solution infrastructure checks after migrations and seed."""

import argparse
import json
from pathlib import Path

import psycopg

from seed import connection_string

EXPECTED_SCHEMAS = {"core", "events", "ops", "analytics"}
EXPECTED_TABLES = {
    "core": {"tenants", "customers", "categories", "products", "inventory",
             "stock_movements", "orders", "order_items", "payments", "refunds", "shipments"},
    "events": {"web_events"},
    "ops": {"idempotency_keys", "outbox_events", "audit_logs"},
    "analytics": {"daily_sales", "raw_orders", "data_quality_issues"},
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Check baseline schema, seed and idempotence")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--snapshot", type=Path, help="Write trusted table counts to file")
    group.add_argument("--compare", type=Path, help="Compare counts to prior snapshot")
    args = parser.parse_args()
    with psycopg.connect(connection_string()) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT version_num FROM public.alembic_version")
        revision_row = cursor.fetchone()
        revision = revision_row[0] if revision_row else "missing"
        assert revision == "0005_analytics_indexes", f"Unexpected revision: {revision}"
        cursor.execute("SELECT schema_name FROM information_schema.schemata")
        schemas = {row[0] for row in cursor.fetchall()}
        assert EXPECTED_SCHEMAS <= schemas, f"Missing schemas: {EXPECTED_SCHEMAS - schemas}"
        cursor.execute("""SELECT table_schema, table_name FROM information_schema.tables
                          WHERE table_type = 'BASE TABLE'""")
        observed = {(schema, table) for schema, table in cursor.fetchall()}
        missing = {(schema, table) for schema, tables in EXPECTED_TABLES.items() for table in tables}
        assert missing <= observed, f"Missing tables: {missing - observed}"
        cursor.execute("SELECT count(*) FROM core.tenants")
        count_row = cursor.fetchone()
        tenant_count = count_row[0] if count_row else 0
        assert tenant_count == 2, f"Expected exactly 2 tenants, got {tenant_count}"
        counts: dict[str, int] = {}
        for schema, tables in EXPECTED_TABLES.items():
            for table in sorted(tables):
                full_table = f"{schema}.{table}"
                # Hardcoded trusted table names, never user input.
                cursor.execute(f"SELECT count(*) FROM {full_table}")
                result = cursor.fetchone()
                counts[full_table] = result[0] if result else 0
        for table in ("core.orders", "core.order_items", "core.payments",
                      "events.web_events", "analytics.raw_orders"):
            assert counts[table] > 0, f"Expected seeded rows in {table}"
            print(f"{table}: {counts[table]:,}")
        if args.snapshot:
            args.snapshot.write_text(json.dumps(counts, sort_keys=True, indent=2), encoding="utf-8")
            print(f"Saved snapshot to {args.snapshot}")
        if args.compare:
            reference = json.loads(args.compare.read_text(encoding="utf-8"))
            assert counts == reference, "Seed is not idempotent: counts differ from snapshot"
            print("PASS: seeded table counts identical to saved snapshot")
        print(f"PASS: revision {revision}, {len(EXPECTED_SCHEMAS)} schemas, 2 tenants")


if __name__ == "__main__":
    main()
