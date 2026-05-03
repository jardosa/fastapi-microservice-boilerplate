from fastapi import FastAPI

from app.api.routes import router as api_router
from app.dapr.subscriptions import router as dapr_router
from app.db.session import Base, engine
from app.models.user import UserFollow, UserProfile, UserStatus
from shared.db.startup import create_all_with_retry

app = FastAPI(title="User Service")


@app.on_event("startup")
def on_startup() -> None:
    create_all_with_retry(Base.metadata, engine)


@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}


app.include_router(api_router)
app.include_router(dapr_router)
