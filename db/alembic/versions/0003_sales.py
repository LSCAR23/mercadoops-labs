"""Orders, order items, payments, refunds and shipments.

Revision ID: 0003_sales
Revises: 0002_catalog
"""
from alembic import op

revision = "0003_sales"
down_revision = "0002_catalog"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE core.orders (
            id UUID PRIMARY KEY,
            tenant_id UUID NOT NULL REFERENCES core.tenants(id),
            customer_id UUID NOT NULL,
            order_number TEXT NOT NULL,
            order_status TEXT NOT NULL,
            ordered_at TIMESTAMPTZ NOT NULL,
            currency CHAR(3) NOT NULL DEFAULT 'USD',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT uq_orders_tenant_id UNIQUE (tenant_id, id),
            CONSTRAINT uq_orders_number UNIQUE (tenant_id, order_number),
            CONSTRAINT fk_order_customer FOREIGN KEY (tenant_id, customer_id)
                REFERENCES core.customers(tenant_id, id),
            CONSTRAINT ck_order_status CHECK (
                order_status IN ('pending', 'paid', 'completed', 'cancelled')),
            CONSTRAINT ck_order_currency CHECK (currency = 'USD')
        )
    """)
    op.execute("""
        CREATE TABLE core.order_items (
            id UUID PRIMARY KEY,
            tenant_id UUID NOT NULL,
            order_id UUID NOT NULL,
            product_id UUID NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price NUMERIC(12,2) NOT NULL,
            discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT uq_items_tenant_id UNIQUE (tenant_id, id),
            CONSTRAINT fk_item_order FOREIGN KEY (tenant_id, order_id)
                REFERENCES core.orders(tenant_id, id),
            CONSTRAINT fk_item_product FOREIGN KEY (tenant_id, product_id)
                REFERENCES core.products(tenant_id, id),
            CONSTRAINT ck_item_amounts CHECK (
                quantity > 0 AND unit_price > 0 AND discount_amount >= 0
                AND discount_amount <= (quantity * unit_price))
        )
    """)
    op.execute("""
        CREATE TABLE core.payments (
            id UUID PRIMARY KEY,
            tenant_id UUID NOT NULL,
            order_id UUID NOT NULL,
            amount NUMERIC(12,2) NOT NULL,
            payment_status TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            processed_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT uq_payments_tenant_id UNIQUE (tenant_id, id),
            CONSTRAINT fk_payment_order FOREIGN KEY (tenant_id, order_id)
                REFERENCES core.orders(tenant_id, id),
            CONSTRAINT ck_payment_amount CHECK (amount > 0),
            CONSTRAINT ck_payment_status CHECK (
                payment_status IN ('pending', 'authorized', 'captured', 'failed', 'voided')),
            CONSTRAINT ck_payment_method CHECK (
                payment_method IN ('card', 'transfer', 'wallet'))
        )
    """)
    op.execute("""
        CREATE TABLE core.refunds (
            id UUID PRIMARY KEY,
            tenant_id UUID NOT NULL,
            payment_id UUID NOT NULL,
            amount NUMERIC(12,2) NOT NULL,
            refund_status TEXT NOT NULL,
            refunded_at TIMESTAMPTZ,
            CONSTRAINT fk_refund_payment FOREIGN KEY (tenant_id, payment_id)
                REFERENCES core.payments(tenant_id, id),
            CONSTRAINT ck_refund_amount CHECK (amount > 0),
            CONSTRAINT ck_refund_status CHECK (
                refund_status IN ('requested', 'approved', 'completed', 'rejected'))
        )
    """)
    op.execute("""
        CREATE TABLE core.shipments (
            id UUID PRIMARY KEY,
            tenant_id UUID NOT NULL,
            order_id UUID NOT NULL,
            shipment_status TEXT NOT NULL,
            shipping_cost NUMERIC(12,2) NOT NULL DEFAULT 0,
            shipped_at TIMESTAMPTZ,
            delivered_at TIMESTAMPTZ,
            CONSTRAINT fk_shipment_order FOREIGN KEY (tenant_id, order_id)
                REFERENCES core.orders(tenant_id, id),
            CONSTRAINT ck_shipping_cost CHECK (shipping_cost >= 0),
            CONSTRAINT ck_shipment_status CHECK (
                shipment_status IN ('created', 'in_transit', 'delivered', 'returned')),
            CONSTRAINT ck_delivery_time CHECK (
                delivered_at IS NULL OR shipped_at IS NULL OR delivered_at >= shipped_at)
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE core.shipments")
    op.execute("DROP TABLE core.refunds")
    op.execute("DROP TABLE core.payments")
    op.execute("DROP TABLE core.order_items")
    op.execute("DROP TABLE core.orders")
