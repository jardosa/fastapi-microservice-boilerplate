# Post Service

Last updated: 2026-05-03 23:18 Asia/Manila

## Responsibilities

- Store posts.
- Provide post CRUD endpoints.
- Publish post-created events.
- Log post-created publish success with `post_id` and `author_id`.

## Endpoints

- `POST /posts`
- `GET /posts/{post_id}`
- `GET /posts?author_id=...`
- `PATCH /posts/{post_id}`
- `DELETE /posts/{post_id}`
- `GET /health`

## Events Published

- `post.created`
