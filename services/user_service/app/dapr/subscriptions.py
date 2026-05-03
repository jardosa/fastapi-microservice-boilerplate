from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.user_service import create_profile, set_status

router = APIRouter()


@router.get("/dapr/subscribe")
def subscribe():
    return [
        {"pubsubname": "pubsub", "topic": "auth.user_registered", "route": "events/auth/user-registered"},
        {"pubsubname": "pubsub", "topic": "auth.user_logged_in", "route": "events/auth/user-logged-in"},
    ]


@router.post("/events/auth/user-registered")
def user_registered(payload: dict, db: Session = Depends(get_db)):
    data = payload.get("data", payload)
    try:
        create_profile(db, UUID(data["user_id"]), data["email"])
    except IntegrityError:
        db.rollback()
    return {"status": "SUCCESS"}


@router.post("/events/auth/user-logged-in")
def user_logged_in(payload: dict, db: Session = Depends(get_db)):
    data = payload.get("data", payload)
    set_status(db, UUID(data["user_id"]), "online")
    return {"status": "SUCCESS"}

