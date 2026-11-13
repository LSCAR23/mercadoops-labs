"""Baseline only; this file must never contain lab exercise solutions."""
from fastapi.testclient import TestClient

from mercadoops.main import app


def test_live_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
