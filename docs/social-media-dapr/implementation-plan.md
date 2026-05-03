# Implementation Plan

Last updated: 2026-05-03 13:51 Asia/Manila

## Sequence

1. Scaffold service folders, shared contracts, Docker Compose, and Dapr components.
2. Implement service-local settings, database sessions, SQLAlchemy models, and health endpoints.
3. Implement Authentication Service endpoints and auth lifecycle events.
4. Implement User Service profiles, follows, and auth event consumers.
5. Implement Post Service CRUD and `post.created` publishing.
6. Implement Comment Service create/read/list and `comment.created` publishing.
7. Implement Notification Service event consumers and notification APIs.
8. Add unit tests and e2e health smoke tests.
9. Keep docs and timestamps current with behavior changes.

## Notes

- Dapr pub/sub is used for asynchronous domain events.
- Dapr service invocation is used by Notification Service to resolve followers and post authors.
- Each service owns its database and does not import another service's database models.
- Docker Compose gates service startup on PostgreSQL health checks, and each service retries schema creation during startup.
