from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.notification import NotificationListResponse, NotificationResponse
from app.services.notification_service import list_notifications, mark_read

router = APIRouter()


def to_response(notification) -> NotificationResponse:
    return NotificationResponse(
        id=UUID(notification.id),
        user_id=UUID(notification.user_id),
        type=notification.type,
        message=notification.message,
        source_id=UUID(notification.source_id),
        is_read=notification.is_read,
        created_at=notification.created_at,
    )


@router.get("/notifications", response_model=NotificationListResponse)
def browse(user_id: UUID, db: Session = Depends(get_db)):
    return NotificationListResponse(notifications=[to_response(row) for row in list_notifications(db, user_id)])


@router.patch("/notifications/{notification_id}/read", response_model=NotificationResponse)
def read(notification_id: UUID, db: Session = Depends(get_db)):
    notification = mark_read(db, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return to_response(notification)

