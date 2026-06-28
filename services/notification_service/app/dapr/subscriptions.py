from uuid import UUID

import logging
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
logger = logging.getLogger("uvicorn.error")


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
    logger.info("Received post.created event post_id=%s author_id=%s", data["post_id"], author_id)
    followers = await invoke_service("user-service", f"/users/{author_id}/followers")
    follower_rows = followers.get("users", [])
    logger.info("Resolved followers for post.created author_id=%s follower_count=%s", author_id, len(follower_rows))
    for user in follower_rows:
        create_notification(
            db,
            UUID(user["id"]),
            NEW_POST_FROM_FOLLOWED_USER,
            f"New post from user {author_id}: {data.get('content_preview', '')}",
            UUID(data["post_id"]),
        )
        logger.info("Created post notification user_id=%s post_id=%s", user["id"], data["post_id"])
    return {"status": "SUCCESS"}


@router.post("/events/comment-created")
async def comment_created(payload: dict, db: Session = Depends(get_db)):
    data = payload.get("data", payload)
    logger.info("Received comment.created event comment_id=%s post_id=%s", data["comment_id"], data["post_id"])
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
        logger.info("Created comment notification user_id=%s comment_id=%s", post_author_id, data["comment_id"])
    else:
        logger.info("Skipped comment notification because author commented on own post user_id=%s", post_author_id)
    return {"status": "SUCCESS"}
