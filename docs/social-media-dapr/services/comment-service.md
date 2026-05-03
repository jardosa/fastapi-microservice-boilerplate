# Comment Service

Last updated: 2026-05-03 04:45 Asia/Manila

## Responsibilities

- Store comments.
- Provide comment create/read/list endpoints.
- Publish comment-created events.

## Endpoints

- `POST /comments`
- `GET /comments/{comment_id}`
- `GET /comments?post_id=...`
- `GET /health`

## Events Published

- `comment.created`

