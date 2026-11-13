# Guía de inicio — MercadoOps Labs en VS Code

## Objetivo

Este repositorio es un laboratorio práctico sin soluciones. GitHub Copilot debe preparar y verificar la infraestructura y actuar como mentor; tú implementas los ejercicios.

## 1. Abrir el proyecto

1. Abre en VS Code la carpeta que contiene `pyproject.toml`.
2. Instala las extensiones recomendadas desde **Extensions: Show Recommended Extensions** (`Ctrl+Shift+X`).
3. Abre GitHub Copilot Chat y selecciona el modo **Agent** para tareas de repositorio. Las reglas de `.github/copilot-instructions.md` se aplican automáticamente.
4. Abre una terminal PowerShell integrada desde **Terminal > New Terminal**.

## 2. Revisar el proyecto y preparar el entorno

Lee `README.md`, `docs/00-CONTRATO-AGENTE.md`, `docs/01-ARQUITECTURA.md`, `docs/02-INSTALACION.md` y `docs/19-CHECKLIST-IMPLEMENTACION.md`.

Desde PowerShell, en la raíz:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv python install 3.12
uv sync --python 3.12
docker compose config
docker compose up -d
docker compose ps
uv run alembic upgrade head
uv run alembic current
uv run python scripts/seed.py --scale tiny --seed 20261101
uv run pytest -q
uv run ruff check src scripts tests
```

No continúes con migraciones o seed si Docker/PostgreSQL no está healthy. No ejecutes `docker compose down -v`, no sobrescribas `.env` y no uses la escala `large` sin revisar primero sus recursos.

Para comprobar la API, inicia en una terminal:

```powershell
uv run uvicorn mercadoops.main:app --reload --host 127.0.0.1 --port 8000
```

En otra terminal:

```powershell
Invoke-RestMethod http://localhost:8000/health/live
Invoke-RestMethod http://localhost:8000/health/ready
```

La documentación de la API está en `http://localhost:8000/docs`.

## 3. Empezar con SQL-001

El primer laboratorio es **SQL-001 — Exploración controlada y filtros**, descrito en `docs/07-LABS-SQL-BASE.md`. Requiere que las migraciones y el seed `tiny` estén listos.

1. Lee el enunciado y revisa `docs/04-MODELO-DE-DATOS.md`.
2. Antes de escribir SQL, define cómo vas a manejar tenant, rango UTC, estados, moneda, orden y paginación.
3. Cuando quieras activarlo, pide a Copilot: “Activa SQL-001. Crea solo el stub `workspaces/sql/SQL-001.sql` con el enunciado y `TODO(student)`, sin escribir SQL de solución”.
4. Implementa tú la consulta y prueba cada caso de aceptación. Después solicita una revisión sin que Copilot la reescriba.

No pidas simplemente “haz el laboratorio”. Una preparación, explicación o revisión no autoriza a Copilot a resolverlo. Los directorios de `workspaces/` se mantienen vacíos hasta que actives un reto.

## Prompt inicial sugerido para Copilot Chat

> Analiza este repositorio para usarlo en VS Code. Lee las instrucciones de `.github/copilot-instructions.md` y la documentación de instalación. No resuelvas ningún laboratorio. Primero informa qué requisitos parecen disponibles y qué comandos propones ejecutar. No sobrescribas `.env`, no borres datos y reporta solo resultados que hayas comprobado.
