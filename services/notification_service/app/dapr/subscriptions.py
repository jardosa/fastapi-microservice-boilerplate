from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.notification_service import (
    NEW_COMMENT_ON_POST,
    NEW_POST_FROM_FOLLOWED_USER,
    create_notification,
)
from shared.dapr.client import invoke_service

router = APIRouter()


@router.get("/dapr/subscribe")
def subscribe():
    return [
        {"pubsubname": "pubsub", "topic": "post.created", "route": "events/post-created"},
        {"pubsubname": "pubsub", "topic": "comment.created", "route": "events/comment-created"},
    ]


@router.post("/events/post-created")
async def post_created(payload: dict, db: Session = Depends(get_db)):
    data = payload.get("data", payload)
    author_id = UUID(data["author_id"])
    followers = await invoke_service("user-service", f"/users/{author_id}/followers")
    for user in followers.get("users", []):
        create_notification(
            db,
            UUID(user["id"]),
            NEW_POST_FROM_FOLLOWED_USER,
            f"New post from user {author_id}: {data.get('content_preview', '')}",
            UUID(data["post_id"]),
        )
    return {"status": "SUCCESS"}


@router.post("/events/comment-created")
async def comment_created(payload: dict, db: Session = Depends(get_db)):
    data = payload.get("data", payload)
    post = await invoke_service("post-service", f"/posts/{data['post_id']}")
    post_author_id = UUID(post["author_id"])
    comment_author_id = UUID(data["author_id"])
    if post_author_id != comment_author_id:
        create_notification(
            db,
            post_author_id,
            NEW_COMMENT_ON_POST,
            f"New comment on your post: {data.get('content_preview', '')}",
            UUID(data["comment_id"]),
        )
    return {"status": "SUCCESS"}

