from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    post_id: UUID
    author_id: UUID
    content: str = Field(min_length=1, max_length=2000)


class CommentResponse(BaseModel):
    id: UUID
    post_id: UUID
    author_id: UUID
    content: str
    created_at: datetime


class CommentListResponse(BaseModel):
    comments: list[CommentResponse]

