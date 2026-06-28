from uuid import UUID

import logging
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.post import PostCreate, PostListResponse, PostResponse, PostUpdate
from app.services.post_service import content_preview, create_post, delete_post, get_post, list_posts, update_post
from shared.contracts.events.posts import PostCreatedEvent
from shared.dapr.client import publish_event

router = APIRouter()
logger = logging.getLogger("uvicorn.error")


def to_response(post) -> PostResponse:
    return PostResponse(
        id=UUID(post.id),
        author_id=UUID(post.author_id),
        content=post.content,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: PostCreate, db: Session = Depends(get_db)):
    post = create_post(db, payload.author_id, payload.content)
    event = PostCreatedEvent(post_id=UUID(post.id), author_id=UUID(post.author_id), content_preview=content_preview(post.content))
    await publish_event("post.created", event)
    logger.info("Created post and published post.created post_id=%s author_id=%s", post.id, post.author_id)
    return to_response(post)


@router.get("/posts/{post_id}", response_model=PostResponse)
def read(post_id: UUID, db: Session = Depends(get_db)):
    post = get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return to_response(post)


@router.get("/posts", response_model=PostListResponse)
def browse(author_id: UUID | None = None, db: Session = Depends(get_db)):
    return PostListResponse(posts=[to_response(post) for post in list_posts(db, author_id)])


@router.patch("/posts/{post_id}", response_model=PostResponse)
def patch(post_id: UUID, payload: PostUpdate, db: Session = Depends(get_db)):
    post = update_post(db, post_id, payload.content)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return to_response(post)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(post_id: UUID, db: Session = Depends(get_db)):
    if not delete_post(db, post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
