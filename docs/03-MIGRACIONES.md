# 03 — Migraciones SQL: código incluido y política de cambios

## Ubicación del código **real y completo**

Las migraciones están **implementadas** (incluyen `upgrade()` y `downgrade()`, DDL PostgreSQL, constraints, índices y FKs):

1. `db/alembic/versions/0001_core.py` — schemas, tenants, customers y categories.
2. `db/alembic/versions/0002_catalog.py` — products, inventory y stock_movements.
3. `db/alembic/versions/0003_sales.py` — orders, order_items, payments, refunds y shipments.
4. `db/alembic/versions/0004_events_ops.py` — web_events, idempotency_keys, outbox_events y audit_logs.
5. `db/alembic/versions/0005_analytics_indexes.py` — daily_sales, raw_orders, data_quality_issues, índices mínimos.

**No hay respuestas de laboratorios en las migraciones.** Se definen únicamente las tablas y restricciones para que exista un problema real que resolver.

## Ejecución

```powershell
uv run alembic history
uv run alembic upgrade head
uv run alembic current
```

## Probar reversibilidad con precaución

Haz rollback **antes del seed y solo en una BD temporal**. Si ya ejecutaste el seed, restaurar una revisión anterior puede perder tablas y datos. No uses esto en tu base principal sin backup:

```powershell
# SOLO EN UNA BASE DESCARTABLE SIN DATOS DE VALOR
uv run alembic downgrade 0004_events_ops
uv run alembic upgrade head
```

La prueba automatizada de rollback completo debe usar una BD efímera dedicada, nunca una base usada para ejercicios. El rollback de `0001_core` elimina schemas vacíos luego de retirar todas las revisiones posteriores.

## Política de migraciones futuras (laboratorios)

1. Crea revisión nueva con `uv run alembic revision -m "descripcion"`.
2. Escribe **siempre** `upgrade()` y `downgrade()` coherentes.
3. En cambios destructivos de producción, aplica expand/contract: nueva columna -> backfill -> cambio consumidor -> retirar antigua después.
4. Ejecuta con datos de ejemplo y prueba la reversión en entorno descartable.
5. **No edites 0001–0005** después de aplicarlas; los cambios forman parte de nuevas revisiones.
6. No metas `CREATE INDEX CONCURRENTLY` dentro de una transacción normal de Alembic: requiere bloque autocommit apropiado y documentación explícita.
7. Evita objetos generados automáticamente que incorporen respuestas a SQL/Python labs.

## Validación estructural

Comprobar: FKs que preservan tenant, checks de dinero/estados, índices mínimos de ruta operacional, tablas para staging y audit. Los índices **no** incluyen todos los posibles tuning para que el estudiante diseñe y justifique mejoras.

## Condiciones de error que debe contemplar el backend futuro

- Item de un tenant apuntando a producto de otro -> FK rechaza.
- `quantity=0`, `unit_price<=0`, `discount_amount<0` -> CHECK rechaza.
- `available_qty<0` -> CHECK rechaza.
- SKU o email duplicado dentro del mismo tenant -> UNIQUE rechaza.
- `refund` mayor que pagos acumulados **no está restringido a nivel fila**: debe trabajarse en una transacción del servicio de negocio.
- `orders` y `payments` pueden tener cardinalidades diferentes en sistemas reales; no asumir la estructura del seed para todos los casos.

## Aclaración sobre datos y borrado

`docker compose down` mantiene el volumen; `down -v` lo borra. No uses `DROP SCHEMA ... CASCADE` como atajo. La creación de datos y las transformaciones deben ser reejecutables y observables.
