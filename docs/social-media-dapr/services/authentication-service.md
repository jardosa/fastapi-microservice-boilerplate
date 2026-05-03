# Authentication Service

Last updated: 2026-05-03 16:22 Asia/Manila

## Responsibilities

- Register users.
- Hash passwords.
- Authenticate credentials.
- Issue JWT access tokens.
- Publish authentication lifecycle events.

## Endpoints

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me` requires an `Authorization: Bearer <token>` header. In Swagger UI, use the Authorize button after login instead of manually adding an `authorization` parameter.
- `GET /health`

## Events Published

- `auth.user_registered`
- `auth.user_logged_in`
