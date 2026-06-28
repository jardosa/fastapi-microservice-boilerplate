# Notification Service

Last updated: 2026-05-03 23:18 Asia/Manila

## Responsibilities

- Consume post and comment events.
- Resolve recipients through Dapr service invocation.
- Store notifications.
- Expose notification read APIs.
- Log event receipt, recipient resolution counts, and notification creation.
- Notifications are created asynchronously after Dapr delivers events, so clients should treat them as eventually consistent.

## Endpoints

- `GET /notifications?user_id=...`
- `PATCH /notifications/{notification_id}/read`
- `GET /health`

## Events Consumed

- `post.created`
- `comment.created`
