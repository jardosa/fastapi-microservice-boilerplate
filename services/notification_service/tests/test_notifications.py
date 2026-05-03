from uuid import uuid4

from fastapi.testclient import TestClient

from app.dapr import subscriptions
from app.db.session import Base, engine
from app.main import app


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_post_created_creates_notifications_for_followers(monkeypatch):
    follower_id = uuid4()
    author_id = uuid4()
    post_id = uuid4()

    async def fake_invoke(app_id, method, params=None):
        assert app_id == "user-service"
        return {"users": [{"id": str(follower_id), "email": "f@example.com", "display_name": None, "bio": None, "status": "offline"}]}

    monkeypatch.setattr(subscriptions, "invoke_service", fake_invoke)
    client = TestClient(app)

    response = client.post(
        "/events/post-created",
        json={"data": {"post_id": str(post_id), "author_id": str(author_id), "content_preview": "hello"}},
    )

    assert response.status_code == 200
    notifications = client.get("/notifications", params={"user_id": str(follower_id)})
    assert notifications.json()["notifications"][0]["type"] == "NEW_POST_FROM_FOLLOWED_USER"


def test_mark_notification_read():
    user_id = uuid4()
    source_id = uuid4()
    from app.db.session import SessionLocal
    from app.services.notification_service import create_notification

    with SessionLocal() as db:
        notification = create_notification(db, user_id, "TEST", "message", source_id)
        notification_id = notification.id

    client = TestClient(app)
    response = client.patch(f"/notifications/{notification_id}/read")

    assert response.status_code == 200
    assert response.json()["is_read"] is True

