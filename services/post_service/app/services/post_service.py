from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.post import Post


def create_post(db: Session, author_id: UUID, content: str) -> Post:
    post = Post(author_id=str(author_id), content=content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_post(db: Session, post_id: UUID) -> Post | None:
    return db.get(Post, str(post_id))


def list_posts(db: Session, author_id: UUID | None = None) -> list[Post]:
    query = db.query(Post)
    if author_id is not None:
        query = query.filter(Post.author_id == str(author_id))
    return query.order_by(Post.created_at.desc()).all()


def update_post(db: Session, post_id: UUID, content: str) -> Post | None:
    post = get_post(db, post_id)
    if post is None:
        return None
    post.content = content
    post.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: UUID) -> bool:
    post = get_post(db, post_id)
    if post is None:
        return False
    db.delete(post)
    db.commit()
    return True


def content_preview(content: str) -> str:
    return content[:140]

