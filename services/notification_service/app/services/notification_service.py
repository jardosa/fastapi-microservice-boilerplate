from uuid import UUID

from sqlalchemy.orm import Session

from app.models.notification import Notification

NEW_POST_FROM_FOLLOWED_USER = "NEW_POST_FROM_FOLLOWED_USER"
NEW_COMMENT_ON_POST = "NEW_COMMENT_ON_POST"


def create_notification(db: Session, user_id: UUID, notification_type: str, message: str, source_id: UUID) -> Notification:
    notification = Notification(
        user_id=str(user_id),
        type=notification_type,
        message=message,
        source_id=str(source_id),
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def list_notifications(db: Session, user_id: UUID) -> list[Notification]:
    return db.query(Notification).filter(Notification.user_id == str(user_id)).order_by(Notification.created_at.desc()).all()


def mark_read(db: Session, notification_id: UUID) -> Notification | None:
    notification = db.get(Notification, str(notification_id))
    if notification is None:
        return None
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification

