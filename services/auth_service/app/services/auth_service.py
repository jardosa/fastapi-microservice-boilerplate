from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.auth_user import AuthUser


def register_user(db: Session, email: str, password: str) -> AuthUser:
    user = AuthUser(email=email.lower(), password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> AuthUser | None:
    return db.query(AuthUser).filter(AuthUser.email == email.lower()).one_or_none()


def get_user_by_id(db: Session, user_id: UUID) -> AuthUser | None:
    return db.get(AuthUser, str(user_id))


def authenticate_user(db: Session, email: str, password: str) -> AuthUser | None:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user


def issue_token(user: AuthUser) -> str:
    return create_access_token(UUID(user.id))

