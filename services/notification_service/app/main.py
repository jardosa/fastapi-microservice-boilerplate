from fastapi import FastAPI

from app.api.routes import router as api_router
from app.dapr.subscriptions import router as dapr_router
from app.db.session import Base, engine
from app.models.notification import Notification
from shared.db.startup import create_all_with_retry

app = FastAPI(title="Notification Service")


@app.on_event("startup")
def on_startup() -> None:
    create_all_with_retry(Base.metadata, engine)


@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service"}


app.include_router(api_router)
app.include_router(dapr_router)
