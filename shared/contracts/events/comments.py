from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CommentCreatedEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    comment_id: UUID
    post_id: UUID
    author_id: UUID
    content_preview: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

