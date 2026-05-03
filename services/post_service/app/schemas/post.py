from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    author_id: UUID
    content: str = Field(min_length=1, max_length=5000)


class PostUpdate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)


class PostResponse(BaseModel):
    id: UUID
    author_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime


class PostListResponse(BaseModel):
    posts: list[PostResponse]

