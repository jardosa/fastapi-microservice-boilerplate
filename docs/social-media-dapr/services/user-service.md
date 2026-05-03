# User Service

Last updated: 2026-05-03 04:45 Asia/Manila

## Responsibilities

- Store user profile data.
- Manage profile updates.
- Manage follow relationships.
- Track simple online/offline status from auth events.
- Provide follower and following lookups.

## Endpoints

- `GET /users/{user_id}`
- `PATCH /users/{user_id}`
- `POST /users/{user_id}/follow?follower_id=...`
- `DELETE /users/{user_id}/follow?follower_id=...`
- `GET /users/{user_id}/followers`
- `GET /users/{user_id}/following`
- `GET /health`

## Events Consumed

- `auth.user_registered`
- `auth.user_logged_in`

