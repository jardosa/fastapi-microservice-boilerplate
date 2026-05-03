# ADR 0001: Use Dapr

Last updated: 2026-05-03 04:45 Asia/Manila

## Decision

Use Dapr for pub/sub and service invocation between FastAPI services.

## Consequences

- Services can avoid broker-specific SDK code.
- Local development uses Dapr sidecars in Docker Compose.
- Event routes must expose `/dapr/subscribe` for Dapr topic discovery.

