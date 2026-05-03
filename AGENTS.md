# Repository Agent Guide

Last updated: 2026-05-03 04:45 Asia/Manila

## Conventions

- Keep each microservice independently deployable.
- Do not share database tables across services.
- Put cross-service payload contracts in `shared/contracts`.
- Use Dapr pub/sub for domain events and Dapr service invocation for synchronous lookups.
- Keep service-owned database models inside the service that owns them.
- Add or update tests with behavior changes.

## Living Documentation

When changing APIs, event payloads, database schemas, service boundaries, Docker Compose, Dapr components, or testing workflows, update the relevant living docs under `docs/social-media-dapr/` in the same change.

Every living document must include:

```md
Last updated: YYYY-MM-DD HH:mm Asia/Manila
```

