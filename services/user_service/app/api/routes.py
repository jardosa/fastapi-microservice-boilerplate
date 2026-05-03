from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import FollowResponse, UserListResponse, UserProfileResponse, UserProfileUpdate
from app.services.user_service import (
    follow_user,
    get_profile,
    list_followers,
    list_following,
    status_for,
    unfollow_user,
    update_profile,
)

router = APIRouter()


def to_response(db: Session, profile) -> UserProfileResponse:
    return UserProfileResponse(
        id=UUID(profile.id),
        email=profile.email,
        display_name=profile.display_name,
        bio=profile.bio,
        status=status_for(db, UUID(profile.id)),
    )


@router.get("/users/{user_id}", response_model=UserProfileResponse)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    profile = get_profile(db, user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="User not found")
    return to_response(db, profile)


@router.patch("/users/{user_id}", response_model=UserProfileResponse)
def patch_user(user_id: UUID, payload: UserProfileUpdate, db: Session = Depends(get_db)):
    profile = update_profile(db, user_id, payload.display_name, payload.bio)
    if profile is None:
        raise HTTPException(status_code=404, detail="User not found")
    return to_response(db, profile)


@router.post("/users/{user_id}/follow", response_model=FollowResponse, status_code=status.HTTP_201_CREATED)
def follow(user_id: UUID, follower_id: UUID, db: Session = Depends(get_db)):
    if user_id == follower_id:
        raise HTTPException(status_code=400, detail="Users cannot follow themselves")
    if get_profile(db, user_id) is None or get_profile(db, follower_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        follow_user(db, follower_id, user_id)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Follow already exists") from exc
    return FollowResponse(follower_id=follower_id, followed_id=user_id)


@router.delete("/users/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
def unfollow(user_id: UUID, follower_id: UUID, db: Session = Depends(get_db)):
    if not unfollow_user(db, follower_id, user_id):
        raise HTTPException(status_code=404, detail="Follow not found")


@router.get("/users/{user_id}/followers", response_model=UserListResponse)
def followers(user_id: UUID, db: Session = Depends(get_db)):
    return UserListResponse(users=[to_response(db, profile) for profile in list_followers(db, user_id)])


@router.get("/users/{user_id}/following", response_model=UserListResponse)
def following(user_id: UUID, db: Session = Depends(get_db)):
    return UserListResponse(users=[to_response(db, profile) for profile in list_following(db, user_id)])

