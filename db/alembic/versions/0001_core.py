"""Core tenants, customers and categories.

Revision ID: 0001_core
Revises:
"""
from alembic import op

revision = "0001_core"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS core")
    op.execute("CREATE SCHEMA IF NOT EXISTS events")
    op.execute("CREATE SCHEMA IF NOT EXISTS ops")
    op.execute("CREATE SCHEMA IF NOT EXISTS analytics")
    op.execute("""
        CREATE TABLE core.tenants (
            id UUID PRIMARY KEY,
            slug TEXT NOT NULL UNIQUE,
            display_name TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT ck_tenants_slug CHECK (slug ~ '^[a-z][a-z0-9-]{2,39}$')
        )
    """)
    op.execute("""
        CREATE TABLE core.customers (
            id UUID PRIMARY KEY,
            tenant_id UUID NOT NULL REFERENCES core.tenants(id),
            email TEXT NOT NULL,
            full_name TEXT NOT NULL,
            country_code CHAR(2) NOT NULL,
            acquisition_channel TEXT NOT NULL,
            acquired_at TIMESTAMPTZ NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT uq_customers_tenant_id UNIQUE (tenant_id, id),
            CONSTRAINT uq_customers_tenant_email UNIQUE (tenant_id, email),
            CONSTRAINT ck_customer_channel CHECK (
                acquisition_channel IN ('organic', 'paid', 'social', 'referral', 'direct'))
        )
    """)
    op.execute("""
        CREATE TABLE core.categories (
            id UUID PRIMARY KEY,
            tenant_id UUID NOT NULL REFERENCES core.tenants(id),
            name TEXT NOT NULL,
            CONSTRAINT uq_categories_tenant_id UNIQUE (tenant_id, id),
            CONSTRAINT uq_categories_tenant_name UNIQUE (tenant_id, name)
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE core.categories")
    op.execute("DROP TABLE core.customers")
    op.execute("DROP TABLE core.tenants")
    op.execute("DROP SCHEMA analytics")
    op.execute("DROP SCHEMA ops")
    op.execute("DROP SCHEMA events")
    op.execute("DROP SCHEMA core")
