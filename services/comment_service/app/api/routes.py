from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.comment import CommentCreate, CommentListResponse, CommentResponse
from app.services.comment_service import content_preview, create_comment, get_comment, list_comments
from shared.contracts.events.comments import CommentCreatedEvent
from shared.dapr.client import publish_event

router = APIRouter()


def to_response(comment) -> CommentResponse:
    return CommentResponse(
        id=UUID(comment.id),
        post_id=UUID(comment.post_id),
        author_id=UUID(comment.author_id),
        content=comment.content,
        created_at=comment.created_at,
    )


@router.post("/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create(payload: CommentCreate, db: Session = Depends(get_db)):
    comment = create_comment(db, payload.post_id, payload.author_id, payload.content)
    await publish_event(
        "comment.created",
        CommentCreatedEvent(
            comment_id=UUID(comment.id),
            post_id=UUID(comment.post_id),
            author_id=UUID(comment.author_id),
            content_preview=content_preview(comment.content),
        ),
    )
    return to_response(comment)


@router.get("/comments/{comment_id}", response_model=CommentResponse)
def read(comment_id: UUID, db: Session = Depends(get_db)):
    comment = get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return to_response(comment)


@router.get("/comments", response_model=CommentListResponse)
def browse(post_id: UUID | None = None, db: Session = Depends(get_db)):
    return CommentListResponse(comments=[to_response(comment) for comment in list_comments(db, post_id)])
