from fastapi import FastAPI

from app.api.routes import router
from app.db.session import Base, engine
from app.models.post import Post
from shared.db.startup import create_all_with_retry

app = FastAPI(title="Post Service")


@app.on_event("startup")
def on_startup() -> None:
    create_all_with_retry(Base.metadata, engine)


@app.get("/health")
def health():
    return {"status": "ok", "service": "post-service"}


app.include_router(router)
