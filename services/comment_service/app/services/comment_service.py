from uuid import UUID

from sqlalchemy.orm import Session

from app.models.comment import Comment


def create_comment(db: Session, post_id: UUID, author_id: UUID, content: str) -> Comment:
    comment = Comment(post_id=str(post_id), author_id=str(author_id), content=content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comment(db: Session, comment_id: UUID) -> Comment | None:
    return db.get(Comment, str(comment_id))


def list_comments(db: Session, post_id: UUID | None = None) -> list[Comment]:
    query = db.query(Comment)
    if post_id is not None:
        query = query.filter(Comment.post_id == str(post_id))
    return query.order_by(Comment.created_at.asc()).all()


def content_preview(content: str) -> str:
    return content[:140]

