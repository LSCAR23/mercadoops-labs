# 19 — Checklist de construcción exacta (para Cursor con poca autonomía técnica)

Este checklist convierte el contrato general en un guion que debe ejecutarse **en orden**. Marca una casilla solo con evidencia. Si un paso falla, detén la fase, corrige únicamente el error y reintenta el paso fallido.

## A. Archivos que deben existir ANTES de tocar código

- [ ] `README.md`
- [ ] `pyproject.toml` y `.env.example`
- [ ] `docker-compose.yml`, `alembic.ini`
- [ ] `db/alembic/env.py`, `db/alembic/script.py.mako`, 5 revisiones `versions/000*.py`
- [ ] `src/mercadoops/__init__.py`, `config.py`, `db.py`, `main.py`
- [ ] `scripts/seed.py`, `scripts/verify_bootstrap.py`
- [ ] `tests/test_bootstrap.py`
- [ ] `.cursor/rules/00-project.mdc`
- [ ] `docs/00` a `docs/19` y `workspaces/README.md`

## B. Validaciones de sintaxis / archivos

- [ ] `python -m compileall -q src scripts db/alembic`
- [ ] `docker compose config` sin errores
- [ ] `uv sync --python 3.12` finaliza correctamente
- [ ] `uv run ruff check src scripts tests` sin errores
- [ ] `uv run pytest -q` en verde
- [ ] `uv.lock` generado y listo para versionar

## C. Validaciones de base de datos

- [ ] Postgres healthy según `docker compose ps`
- [ ] `uv run alembic upgrade head` finaliza sin errores
- [ ] `uv run alembic current` = `0005_analytics_indexes`
- [ ] 4 schemas correctos
- [ ] 18 tablas correctas (11 core + 1 events + 3 ops + 3 analytics)
- [ ] `tiny` insertó 2 tenants, órdenes, pagos, eventos y raw
- [ ] `uv run python scripts/verify_bootstrap.py` en verde
- [ ] `verify_bootstrap.py --snapshot counts.bootstrap.json`, repetir seed, luego `--compare counts.bootstrap.json` pasa sin diferencias
- [ ] `analytics.daily_sales` y `analytics.data_quality_issues` siguen vacías

## D. Validaciones de API

- [ ] `uv run uvicorn mercadoops.main:app --reload --port 8000` arranca
- [ ] `GET /health/live` devuelve 200 con status `alive`
- [ ] `GET /health/ready` devuelve 200 si DB accesible
- [ ] `/docs` expone exclusivamente health antes de labs
- [ ] 503 de readiness ante DB inaccesible (probar de forma controlada)

## E. Restricciones de código para NO resolver labs

- [ ] No hay vista de ventas/cohortes/RFM o ETL prehecho.
- [ ] `analytics.daily_sales` no se rellena en el seed.
- [ ] No hay routers/products/orders/payments reales antes de los labs BE.
- [ ] No hay autenticación, workers ni cache funcional en bootstrap.
- [ ] `workspaces/` conserva únicamente docs/instrucciones y TODO(student).
- [ ] Test de bootstrap solo inspecciona infraestructura, sin respuestas de negocio.

## F. Cierre y reporte obligatorio

Genera reporte con comandos, stdout resumido, errores encontrados, cambios, revisiones aplicadas, conteos, links/paths de archivos y limitaciones actuales. No declares pasos ejecutados si no los ejecutaste. **No entregues proyectos finales listos:** deben ser trabajo del estudiante.

## G. Política de mejoras y correcciones

- Corrige errores de compatibilidad con versiones instaladas, no migres tecnologías sin motivo.
- Si el seed tiene un bug, crea test mínimo de infraestructura y ajústalo sin modificar resultados del lab.
- Si modificas una migración ya aplicada, eso viola el contrato: crea revisión nueva en su lugar.
- Si no hay Docker ni acceso a red, realiza únicamente sintaxis/inspección y reporta lo no comprobado.
