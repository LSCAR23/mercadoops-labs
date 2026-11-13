# 02 — Instalación reproducible en Windows 11

## Prerrequisitos

Instala Git, Docker Desktop con motor Linux/WSL2, Python 3.12 (o usa `uv python install 3.12`), uv y Cursor. Reserva al menos 4 GB libres en disco para la escala `tiny`; para `large` el consumo crece considerablemente. Los puertos locales son **5433/PostgreSQL**, **6380/Redis**, **8000/API**.

## Procedimiento con PowerShell

1. Descomprime el ZIP. Abre Cursor en la carpeta que contiene `pyproject.toml`.
2. Abre el terminal PowerShell integrado.
3. Ejecuta `git init` si todavía no es repositorio, y verifica `.gitignore`.
4. Comprueba versiones:

```powershell
python --version
uv --version
docker --version
docker compose version
git --version
```

5. Prepara variables y dependencias:

```powershell
Copy-Item .env.example .env
uv python install 3.12
uv sync --python 3.12
```

6. Arranca infraestructura:

```powershell
docker compose config
docker compose up -d
docker compose ps
```

Si el estado de Postgres es `starting`, repite `docker compose ps` hasta ver `healthy`. Si existe conflicto de puerto, cambia **simultáneamente** `docker-compose.yml` y `.env` y explica por qué.

7. Aplica migraciones y carga dataset mínimo:

```powershell
uv run alembic history
uv run alembic upgrade head
uv run alembic current
uv run python scripts/seed.py --scale tiny --seed 20261101
```

8. Arranca la API:

```powershell
uv run uvicorn mercadoops.main:app --reload --host 127.0.0.1 --port 8000
```

9. Desde un segundo terminal:

```powershell
Invoke-RestMethod http://localhost:8000/health/live
Invoke-RestMethod http://localhost:8000/health/ready
uv run pytest -q
uv run ruff check src scripts tests
```

## Consultas manuales de verificación (NO resuelven laboratorios)

Con cualquier cliente SQL conectado al puerto **5433** (por ejemplo DBeaver):

```sql
SELECT version();
SELECT schema_name FROM information_schema.schemata
WHERE schema_name IN ('core', 'events', 'ops', 'analytics') ORDER BY schema_name;
SELECT version_num FROM public.alembic_version;
SELECT count(*) FROM core.tenants;
SELECT count(*) FROM core.orders;
SELECT count(*) FROM events.web_events;
SELECT count(*) FROM analytics.raw_orders;
```

Esperado: 4 schemas; revisión actual `0005_analytics_indexes`; 2 tenants; conteos positivos después del seed.

## Comandos de mantenimiento

```powershell
# Sólo apaga contenedores; conserva los datos
docker compose down
# Volver a encender
docker compose up -d
# Ver logs (no hagas dump de secrets)
docker compose logs --tail=100 postgres
# Se necesita aprobación explícita para BORRAR datos:
# docker compose down -v
```

## Diagnóstico sistemático

| Síntoma | Comprobar | Acción segura |
|---|---|---|
| `docker` no se reconoce | Docker Desktop abierto / PATH | Reiniciar terminal, instalar Desktop |
| Postgres no healthy | `docker compose logs postgres` | Corregir variable/volumen sin borrar datos |
| `connection refused` | `docker compose ps`, puerto 5433 | Revisar puerto y cadena en `.env` |
| `password authentication failed` | usuario/clave del volumen existente | Corregir credenciales; cambiar variables **no** rota usuario de volumen previo |
| `alembic` sin env | `.env`, cwd raíz | Ejecutar desde raíz, verificar `DATABASE_URL` |
| `No module named mercadoops` | `uv sync` y build Hatchling | Reinstalar entorno de proyecto |
| test ready falla | contenedor y migración | Verificar `SELECT 1`, nunca alterar test para ocultarlo |
| linter falla en archivo nuevo | ruta/línea concreta | Corregir, repetir check |

## Reproducibilidad / lock

Después de un `uv sync` exitoso, **versiona `uv.lock`** para obtener instalaciones reproducibles. No uses `uv lock --upgrade` durante un laboratorio sin registrarlo. Nunca pegues valores reales de `.env` en un issue o prompt.
