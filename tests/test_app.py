import re

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_returns_translation_with_timestamp() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers.get("content-type", "").startswith("text/plain")
    assert "hello world" in response.text.lower()
    assert re.search(r"@\s*\d{4}-\d{2}-\d{2}T", response.text)
