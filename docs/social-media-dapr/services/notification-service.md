# Notification Service

Last updated: 2026-05-03 04:45 Asia/Manila

## Responsibilities

- Consume post and comment events.
- Resolve recipients through Dapr service invocation.
- Store notifications.
- Expose notification read APIs.

## Endpoints

- `GET /notifications?user_id=...`
- `PATCH /notifications/{notification_id}/read`
- `GET /health`

## Events Consumed

- `post.created`
- `comment.created`

