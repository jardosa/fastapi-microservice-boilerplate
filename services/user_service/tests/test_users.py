from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.session import Base, SessionLocal, engine
from app.main import app
from app.services.user_service import create_profile


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_follow_and_list_followers():
    client = TestClient(app)
    follower_id = uuid4()
    followed_id = uuid4()
    with SessionLocal() as db:
        create_profile(db, follower_id, "follower@example.com")
        create_profile(db, followed_id, "followed@example.com")

    response = client.post(f"/users/{followed_id}/follow", params={"follower_id": str(follower_id)})
    assert response.status_code == 201

    followers = client.get(f"/users/{followed_id}/followers")
    assert followers.status_code == 200
    assert followers.json()["users"][0]["id"] == str(follower_id)


def test_user_registered_event_creates_profile():
    client = TestClient(app)
    user_id = uuid4()

    response = client.post("/events/auth/user-registered", json={"data": {"user_id": str(user_id), "email": "new@example.com"}})

    assert response.status_code == 200
    assert client.get(f"/users/{user_id}").status_code == 200

