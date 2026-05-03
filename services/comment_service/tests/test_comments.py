from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import routes
from app.db.session import Base, engine
from app.main import app


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_comment_publishes_event(monkeypatch):
    published = {}

    async def fake_publish(topic, payload):
        published["topic"] = topic
        published["payload"] = payload

    monkeypatch.setattr(routes, "publish_event", fake_publish)
    client = TestClient(app)

    response = client.post(
        "/comments",
        json={"post_id": str(uuid4()), "author_id": str(uuid4()), "content": "nice post"},
    )

    assert response.status_code == 201
    assert published["topic"] == "comment.created"

