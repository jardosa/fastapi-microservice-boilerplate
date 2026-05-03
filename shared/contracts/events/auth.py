from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class UserRegisteredEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    email: EmailStr
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserLoggedInEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

