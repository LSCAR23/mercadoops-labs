from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from mercadoops.db import get_engine

app = FastAPI(title="MercadoOps Labs", version="0.1.0")


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
    return {"status": "ready"}
