from fastapi.testclient import TestClient

from app.api import routes
from app.db.session import Base, engine
from app.main import app


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_register_and_login(monkeypatch):
    async def noop_publish(topic, payload):
        return None

    monkeypatch.setattr(routes, "publish_event", noop_publish)
    client = TestClient(app)

    created = client.post("/auth/register", json={"email": "a@example.com", "password": "password123"})
    assert created.status_code == 201

    token = client.post("/auth/login", json={"email": "a@example.com", "password": "password123"})
    assert token.status_code == 200
    assert token.json()["access_token"]

    current_user = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token.json()['access_token']}"},
    )
    assert current_user.status_code == 200
    assert current_user.json()["email"] == "a@example.com"


def test_me_requires_bearer_token():
    client = TestClient(app)

    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing bearer token"


def test_login_rejects_invalid_password(monkeypatch):
    async def noop_publish(topic, payload):
        return None

    monkeypatch.setattr(routes, "publish_event", noop_publish)
    client = TestClient(app)
    client.post("/auth/register", json={"email": "a@example.com", "password": "password123"})

    response = client.post("/auth/login", json={"email": "a@example.com", "password": "wrong"})

    assert response.status_code == 401
