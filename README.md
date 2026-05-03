# FastAPI Social Microservices With Dapr

Last updated: 2026-05-03 13:51 Asia/Manila

This repository contains a Dockerized FastAPI microservices scaffold for a simple social media application. It uses:

- Python, FastAPI, Pydantic, SQLAlchemy, Alembic
- Dapr service invocation and pub/sub
- Redis for local Dapr pub/sub
- PostgreSQL with one database per service

## Services

- Authentication Service: registration, login, JWT issuance, auth events
- User Service: profiles, follow graph, auth event subscriptions
- Post Service: post CRUD and post-created events
- Comment Service: comment CRUD and comment-created events
- Notification Service: event consumers, recipient resolution, notification storage

## Local Development

Install Dapr and Docker, then run:

```bash
docker compose up --build
```

Primary service ports:

- Auth: http://localhost:8001
- Users: http://localhost:8002
- Posts: http://localhost:8003
- Comments: http://localhost:8004
- Notifications: http://localhost:8005

Each service exposes `GET /health`.

Docker Compose waits for each PostgreSQL database health check before starting its owning service. Services also retry schema creation during startup to tolerate brief database warm-up delays.

## Testing

Run unit tests per service from that service folder:

```bash
cd services/auth_service
pytest
```

Run e2e tests after `docker compose up --build`:

```bash
pytest tests/e2e
```

## Living Documentation Rule

Any implementation change that affects APIs, events, database tables, service responsibilities, Docker/Dapr config, or test workflows must update the relevant files in `docs/social-media-dapr/` and refresh their `Last updated` timestamp.
