# Unit Testing Agent

Last updated: 2026-05-03 04:45 Asia/Manila

## Ownership

- Per-service unit tests.
- Database test fixtures.
- FastAPI dependency overrides.
- Event publisher mocks.
- Schema validation tests.

## Checklist

- [ ] Cover success and failure paths.
- [ ] Keep unit tests independent from Dapr sidecars.
- [ ] Use SQLite or isolated disposable databases for unit tests.
- [ ] Mock event publishing and service invocation.
- [ ] Update test documentation when test workflow changes.

