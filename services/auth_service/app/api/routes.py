from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.schemas.auth import AuthUserResponse, LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import authenticate_user, get_user_by_id, issue_token, register_user
from shared.contracts.events.auth import UserLoggedInEvent, UserRegisteredEvent
from shared.dapr.client import publish_event

router = APIRouter()
bearer_scheme = HTTPBearer(auto_error=False)


@router.post("/auth/register", response_model=AuthUserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = register_user(db, payload.email, payload.password)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email is already registered") from exc
    await publish_event("auth.user_registered", UserRegisteredEvent(user_id=UUID(user.id), email=user.email))
    return AuthUserResponse(id=UUID(user.id), email=user.email)


@router.post("/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    await publish_event("auth.user_logged_in", UserLoggedInEvent(user_id=UUID(user.id)))
    return TokenResponse(access_token=issue_token(user))


@router.get("/auth/me", response_model=AuthUserResponse)
def me(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if credentials is None or credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing bearer token")
    try:
        user_id = decode_access_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid bearer token") from exc
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return AuthUserResponse(id=UUID(user.id), email=user.email)
