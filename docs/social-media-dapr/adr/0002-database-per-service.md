# ADR 0002: Database Per Service

Last updated: 2026-05-03 13:51 Asia/Manila

## Decision

Each service owns its own database and schema.

## Consequences

- Services do not join across service-owned tables.
- Cross-service reads use Dapr service invocation.
- Event consumers maintain their own local state when needed.
- Local Compose startup waits for each service-owned database to report healthy before starting the owning app.
