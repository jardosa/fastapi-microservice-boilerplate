# E2E Testing Agent

Last updated: 2026-05-03 04:45 Asia/Manila

## Ownership

- Docker Compose smoke tests.
- Dapr sidecar health checks.
- Cross-service workflows.
- Pub/sub delivery verification.
- Failure-path scenarios across service boundaries.

## Checklist

- [ ] Start the full local stack before running e2e tests.
- [ ] Verify all `/health` endpoints.
- [ ] Verify register, login, follow, post, comment, and notification workflows.
- [ ] Confirm Dapr service invocation between services.
- [ ] Confirm Redis-backed pub/sub delivery.

