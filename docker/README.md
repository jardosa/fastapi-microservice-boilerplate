# Docker Notes

Last updated: 2026-05-03 13:51 Asia/Manila

Docker Compose is defined at the repository root. Service-specific Dockerfiles live with each service under `services/*/Dockerfile`.

PostgreSQL containers expose `pg_isready` health checks, and FastAPI services use `depends_on.condition: service_healthy` so they do not start before their database is accepting connections.
