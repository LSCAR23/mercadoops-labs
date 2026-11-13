# 01 — Arquitectura de referencia

## Objetivo de aprendizaje

Construir un entorno que imite los problemas comunes de una empresa que vende productos online, opera varios comercios, recibe eventos del sitio web e importa pedidos externos. Los analistas deben obtener métricas correctas y explicar sus decisiones; los desarrolladores backend deben proteger integridad, seguridad y disponibilidad ante concurrencia y errores.

## Decisiones técnicas

| Capa | Herramienta | Por qué |
|---|---|---|
| Runtime | Python 3.12 | Tipado, tooling y compatibilidad |
| Dependencias | `uv` + `pyproject.toml` | Ambiente reproducible; generar `uv.lock` en setup |
| OLTP | PostgreSQL 16 | CTE, ventanas, JSONB, MVCC, `EXPLAIN`, transacciones |
| Migraciones | Alembic + SQL manual `op.execute` | Versionado, rollback, disciplina de esquema |
| API | FastAPI + Pydantic v2 | Contratos OpenAPI, validación |
| Acceso a datos | SQLAlchemy 2 + `psycopg` 3 | Sesiones, transacciones, SQL parametrizado |
| Analítica local | Pandas, Polars, DuckDB, PyArrow | Comparar estrategias batch y rendimiento |
| Testing | Pytest, HTTPX, Ruff, MyPy | Comprobación de calidad por niveles |
| Infra | Docker Compose PostgreSQL y Redis | Entorno repetible; Redis reservado a labs backend |
| IDE / mentor | VS Code + GitHub Copilot | Montaje y revisión; no hacer ejercicios |

## Flujo lógico

```text
                   +------------------------+
                   | VS Code + Copilot     |
                   +-----------+------------+
                               |
                  docs + código base + ejercicios
                               |
            +------------------v---------------------+
            | Python local / FastAPI / Laboratorios  |
            +----------+---------------+-------------+
                       |               |
               SQLAlchemy 2        pandas/Polars
                       |               |
                  +----v---------------v----+
                  | PostgreSQL 16           |
                  | core | events | ops     |
                  | analytics (destino)    |
                  +-------------------------+
                         Redis (retos)
```

## Separación de responsabilidades

- `core`: datos operacionales normalizados (catálogo, clientes, pedidos, pagos).
- `events`: telemetría de sesiones del sitio (web events).
- `ops`: patrones técnicos (idempotencia, outbox, bitácora); **existen tablas, no implementaciones**.
- `analytics`: almacenamiento raw de datos importados y tablas destino **vacías** para retos.
- `scripts/seed.py`: crea datos de prueba, no calcula KPI, no limpia datos y no implementa reportes.
- `workspaces`: código propio del estudiante; Copilot no debe tocar TODO(student) salvo instrucción explícita.

## Reglas de negocio de dominio

1. Hay dos tenants separados; una relación padre-hijo **debe** pertenecer al mismo tenant.
2. Un pedido tiene un cliente y uno o más ítems. En la semilla: 1–4 ítems, exactamente un pago (regla de generación, no restricción universal de BD).
3. Precios se capturan en cada `order_item` como snapshot histórico; el precio actual de `products` puede cambiar después.
4. Los reembolsos se vinculan a pagos, no directamente a ítems. La semilla crea reembolsos parciales o totales; en producción deberá validarse el total acumulado.
5. Órdenes tienen `pending`, `paid`, `completed`, `cancelled`. La máquina de estados se construye en backend; la BD solo restringe valores.
6. Inventario diferencia disponible y reservado. No se actualiza al leer; operaciones de reserva/venta deberán ser atómicas.
7. `web_events` utiliza `session_id` y eventos que pueden repetirse o faltar. La conversión no se asume como una relación 1:1 con pagos.
8. `raw_orders` contiene JSONB de fuentes externas con datos inválidos a propósito. No insertar automáticamente dichos datos en tablas core.
9. Todos los tiempos usan `TIMESTAMPTZ` y se interpretan en UTC; fechas de negocio se documentan explícitamente.
10. Todas las cifras monetarias de órdenes usan USD y `NUMERIC`/`Decimal`, no `float` en cálculos exactos.

## Niveles de dominio

- **Analista básico/intermedio:** SQL limpio, joins, agrupaciones, Pandas, calidad de datos.
- **Analista experto:** cohortes, funnels, atribución, ventanas, optimización SQL, pruebas estadísticas, pipelines incrementales.
- **Backend intermedio:** API tipada, persistencia, errores, paginación, filtros, tests.
- **Backend senior:** idempotencia, locking, aislamiento tenant, resiliencia, observabilidad, outbox, SLO, optimización, seguridad y diseño documentado.

## Elementos que no deben aparecer en el bootstrap

- Dashboard terminado.
- Tablas de resultado precalculadas con KPIs.
- Solución de reservas de inventario, pagos, cohortes, RFM, LTV o funnel.
- JWT funcional, caché funcional, workers activos o reglas de permisos implementadas.
- Tests de labs que incorporen la respuesta en forma de SQL o algoritmo de referencia.
