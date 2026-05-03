from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserProfileCreate(BaseModel):
    id: UUID
    email: EmailStr
    display_name: str | None = None


class UserProfileUpdate(BaseModel):
    display_name: str | None = Field(default=None, max_length=120)
    bio: str | None = Field(default=None, max_length=500)


class UserProfileResponse(BaseModel):
    id: UUID
    email: EmailStr
    display_name: str | None
    bio: str | None
    status: str | None = None


class FollowResponse(BaseModel):
    follower_id: UUID
    followed_id: UUID


class UserListResponse(BaseModel):
    users: list[UserProfileResponse]

