# MercadoOps Labs — Python, SQL, Analytics y Backend Senior

Un **proyecto de entrenamiento práctico, sin soluciones**, para progresar desde fundamentos hasta análisis de datos de nivel experto y diseño de sistemas backend de nivel senior. GitHub Copilot en VS Code te acompaña como mentor: **puede ayudarte a construir y verificar la plataforma, pero no debe resolver tus retos**.

**Tema:** Marketplace multiempresa con órdenes, inventario, clientes, pagos, reembolsos, envíos, sesiones/eventos web, staging de importaciones y auditoría. **Datos:** sintéticos, reproducibles, ~2 años (fecha ancla 2026-11-01 UTC), dos empresas.

## Qué incluye este ZIP

- `docs/*.md`: contrato del agente, arquitectura, setup, SQL, Python, backend, pruebas, rúbricas y proyectos finales.
- `.github/copilot-instructions.md`: reglas persistentes de GitHub Copilot para este repositorio.
- `.vscode/extensions.json`: extensiones recomendadas para trabajar en VS Code.
- `.cursor/rules/00-project.mdc`: regla heredada, conservada para compatibilidad con Cursor; VS Code usa `.github/copilot-instructions.md`.
- `db/alembic/versions/*.py`: **cinco migraciones Alembic completas**, reversibles, con SQL real PostgreSQL.
- `src/mercadoops`: API FastAPI mínima con `/health/live` y `/health/ready`.
- `scripts/seed.py`: generador reproducible de datos sintéticos; defectos controlados en `analytics.raw_orders`.
- `workspaces/`: directorios vacíos para que escribas **tus** soluciones.
- `tests/`: test básico de infraestructura (no incluye solución de ningún laboratorio).

## Inicio rápido (PowerShell en Windows 11)

Requisitos: VS Code, GitHub Copilot Chat, Python 3.12 o 3.13, [uv](https://docs.astral.sh/uv/), Docker Desktop (Linux containers) y Git. Ejecuta los comandos en el terminal PowerShell de VS Code, desde la raíz del proyecto.

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv python install 3.12
uv sync --python 3.12
# A partir de aquí Postgres queda disponible en localhost:5433
docker compose up -d
# Espera a que docker compose ps indique servicio postgres healthy
uv run alembic upgrade head
uv run python scripts/seed.py --scale tiny --seed 20261101
uv run uvicorn mercadoops.main:app --reload --port 8000
```

Abre `http://localhost:8000/docs` y `http://localhost:8000/health/ready`. En otra terminal:

```powershell
uv run pytest -q
uv run ruff check src scripts tests
uv run alembic current
uv run python scripts/verify_bootstrap.py --snapshot counts.bootstrap.json
uv run python scripts/seed.py --scale tiny --seed 20261101
uv run python scripts/verify_bootstrap.py --compare counts.bootstrap.json
```

> Si `.env` ya existe, consérvalo: el comando no lo sobrescribe. Si `uv sync` falla por conexión, proxy o versiones, pídele a Copilot que diagnostique el error con evidencia; no debe afirmar que algo funciona sin ejecutarlo. El archivo `.env` y los datos locales no deben commitearse.

## Índice de lectura obligatorio

| Orden | Documento | Propósito |
|---|---|---|
| 1 | [00-CONTRATO-AGENTE](docs/00-CONTRATO-AGENTE.md) | Contrato del agente |
| 2 | [01-ARQUITECTURA](docs/01-ARQUITECTURA.md) | Diseño, dominio y decisiones técnicas |
| 3 | [02-INSTALACION](docs/02-INSTALACION.md) | Setup y diagnóstico paso a paso |
| 4 | [03-MIGRACIONES](docs/03-MIGRACIONES.md) | Evolución del esquema y rollback |
| 5 | [04-MODELO-DE-DATOS](docs/04-MODELO-DE-DATOS.md) | Diccionario y reglas de negocio |
| 6 | [05-DATOS-Y-CALIDAD](docs/05-DATOS-Y-CALIDAD.md) | Semillas, escalas, defectos controlados |
| 7 | [06-METODOLOGIA](docs/06-METODOLOGIA.md) | Cómo resolver, entregar y evaluar |
| 8 | [07-LABS-SQL-BASE](docs/07-LABS-SQL-BASE.md) | SQL esencial e intermedio |
| 9 | [08-LABS-SQL-EXPERTO](docs/08-LABS-SQL-EXPERTO.md) | SQL analítico y performance |
| 10 | [09-LABS-PYTHON-BASE](docs/09-LABS-PYTHON-BASE.md) | Python orientado a datos |
| 11 | [10-LABS-PYTHON-EXPERTO](docs/10-LABS-PYTHON-EXPERTO.md) | ETL, estadística, calidad, rendimiento |
| 12 | [11-LABS-BACKEND-BASE](docs/11-LABS-BACKEND-BASE.md) | API, persistencia y contratos |
| 13 | [12-LABS-BACKEND-SENIOR](docs/12-LABS-BACKEND-SENIOR.md) | Concurrencia, seguridad, consistencia |
| 14 | [13-QA-OPS](docs/13-QA-OPS.md) | Testing, CI, Docker, observabilidad |
| 15 | [14-PROYECTOS-FINALES](docs/14-PROYECTOS-FINALES.md) | Capstones de portafolio |
| 16 | [15-RUTA-Y-RUBRICAS](docs/15-RUTA-Y-RUBRICAS.md) | 20 semanas y niveles de dominio |
| 17 | [16-PROMPTS-COPILOT](docs/16-PROMPTS-COPILOT.md) | Prompts para Copilot Chat por fase |
| 18 | [17-CONTRATOS-API](docs/17-CONTRATOS-API.md) | Contratos a implementar, no respuestas |
| 19 | [18-SEGURIDAD-Y-CALIDAD](docs/18-SEGURIDAD-Y-CALIDAD.md) | Seguridad y reglas profesionales |
| 20 | [19-CHECKLIST-IMPLEMENTACION](docs/19-CHECKLIST-IMPLEMENTACION.md) | Checklist ejecutable y auditoría del entorno |
| 21 | [20-CODIGO-MIGRACIONES](docs/20-CODIGO-MIGRACIONES.md) | Migraciones completas replicadas en Markdown |

## Regla de oro

Abre el repositorio en VS Code, instala las extensiones recomendadas y abre GitHub Copilot Chat en modo **Agent**. Lee primero **[INSTRUCCIONES-PARA-VSCODE.md](INSTRUCCIONES-PARA-VSCODE.md)** y sigue el setup desde el terminal PowerShell integrado.

**No le pidas a Copilot “resolver el laboratorio”.** Pídele preparar el entorno, explicar requisitos, revisar tu código después de que lo implementes o darte pistas graduales. Los ejercicios no incluyen respuestas ni SQL resuelto.

## Empezar con el primer laboratorio

El primer reto es **SQL-001 — Exploración controlada y filtros**. Antes de empezar, completa el setup, aplica las migraciones, carga el seed `tiny` y confirma que la base está disponible. Luego:

1. Lee el enunciado en [docs/07-LABS-SQL-BASE.md](docs/07-LABS-SQL-BASE.md) y consulta el esquema en [docs/04-MODELO-DE-DATOS.md](docs/04-MODELO-DE-DATOS.md).
2. Usa Copilot para aclarar el contrato y preparar `workspaces/sql/SQL-001.sql` **solo si se lo pides**, sin escribir la consulta.
3. Diseña tu consulta para un tenant, un rango UTC, estados y moneda; incluye paginación estable y orden explícito.
4. Comprueba los casos de aceptación del enunciado y documenta tus decisiones. Pide revisión o pistas, no una solución.

El proyecto contiene el enunciado, pero no la solución. No se crea el archivo del laboratorio hasta que decidas activarlo.

## Puntos de atención

- Las migraciones son código de **infraestructura entregado**, no respuestas a ejercicios.
- `scripts/seed.py` genera datos para entrenar; no calcula KPIs ni genera informes finales.
- `analytics.daily_sales` y `analytics.data_quality_issues` empiezan vacías a propósito.
- No está diseñado para producción ni para datos reales; secretos de `.env` son solo locales.
- `--scale` controla **cantidad por tenant**, no total; lee el documento de seeds antes de cargar `large`.
