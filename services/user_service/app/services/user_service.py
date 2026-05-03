from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import UserFollow, UserProfile, UserStatus


def create_profile(db: Session, user_id: UUID, email: str, display_name: str | None = None) -> UserProfile:
    profile = UserProfile(id=str(user_id), email=email.lower(), display_name=display_name)
    db.add(profile)
    db.add(UserStatus(user_id=str(user_id), status="offline"))
    db.commit()
    db.refresh(profile)
    return profile


def get_profile(db: Session, user_id: UUID) -> UserProfile | None:
    return db.get(UserProfile, str(user_id))


def update_profile(db: Session, user_id: UUID, display_name: str | None, bio: str | None) -> UserProfile | None:
    profile = get_profile(db, user_id)
    if profile is None:
        return None
    if display_name is not None:
        profile.display_name = display_name
    if bio is not None:
        profile.bio = bio
    profile.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(profile)
    return profile


def set_status(db: Session, user_id: UUID, status: str) -> None:
    row = db.get(UserStatus, str(user_id))
    if row is None:
        row = UserStatus(user_id=str(user_id), status=status)
        db.add(row)
    else:
        row.status = status
        row.updated_at = datetime.now(timezone.utc)
    db.commit()


def follow_user(db: Session, follower_id: UUID, followed_id: UUID) -> UserFollow:
    follow = UserFollow(follower_id=str(follower_id), followed_id=str(followed_id))
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow


def unfollow_user(db: Session, follower_id: UUID, followed_id: UUID) -> bool:
    follow = db.query(UserFollow).filter(
        UserFollow.follower_id == str(follower_id),
        UserFollow.followed_id == str(followed_id),
    ).one_or_none()
    if follow is None:
        return False
    db.delete(follow)
    db.commit()
    return True


def list_followers(db: Session, user_id: UUID) -> list[UserProfile]:
    return db.query(UserProfile).join(UserFollow, UserFollow.follower_id == UserProfile.id).filter(
        UserFollow.followed_id == str(user_id)
    ).all()


def list_following(db: Session, user_id: UUID) -> list[UserProfile]:
    return db.query(UserProfile).join(UserFollow, UserFollow.followed_id == UserProfile.id).filter(
        UserFollow.follower_id == str(user_id)
    ).all()


def status_for(db: Session, user_id: UUID) -> str | None:
    row = db.get(UserStatus, str(user_id))
    return row.status if row else None

