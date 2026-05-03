from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import routes
from app.db.session import Base, engine
from app.main import app


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_post_publishes_event(monkeypatch):
    published = {}

    async def fake_publish(topic, payload):
        published["topic"] = topic
        published["payload"] = payload

    monkeypatch.setattr(routes, "publish_event", fake_publish)
    client = TestClient(app)

    response = client.post("/posts", json={"author_id": str(uuid4()), "content": "hello world"})

    assert response.status_code == 201
    assert published["topic"] == "post.created"

