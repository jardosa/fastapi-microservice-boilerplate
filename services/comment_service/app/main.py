from fastapi import FastAPI

from app.api.routes import router
from app.db.session import Base, engine
from app.models.comment import Comment
from shared.db.startup import create_all_with_retry

app = FastAPI(title="Comment Service")


@app.on_event("startup")
def on_startup() -> None:
    create_all_with_retry(Base.metadata, engine)


@app.get("/health")
def health():
    return {"status": "ok", "service": "comment-service"}


app.include_router(router)
