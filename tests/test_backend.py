from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_agents_returns_registry_metadata() -> None:
    response = client.get("/api/agents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    ids = {agent["id"] for agent in data}
    assert "drafter" in ids
    assert "rag" in ids


def test_drafter_health_endpoint() -> None:
    response = client.get("/api/agents/drafter/health")
    assert response.status_code == 200
    assert "ready" in response.json()


def test_drafter_draft_rejects_empty_message() -> None:
    response = client.post("/api/agents/drafter/draft", json={"message": "   "})
    assert response.status_code == 400
