# Process Overview

Last updated: 2026-05-03 14:32 Asia/Manila

This living document explains how requests, events, and service-to-service calls move through the system. Update this file whenever routing, API gateway behavior, Dapr invocation, pub/sub topics, service ownership, or deployment topology changes.

## Current External Request Flow

The current local Docker setup exposes each service directly on a separate host port. There is no API gateway yet.

```text
Client -> localhost:8001 -> Authentication Service
Client -> localhost:8002 -> User Service
Client -> localhost:8003 -> Post Service
Client -> localhost:8004 -> Comment Service
Client -> localhost:8005 -> Notification Service
```

Current responsibility of the client:

- Knows which service owns each route.
- Sends auth requests directly to Auth Service.
- Sends profile and follow requests directly to User Service.
- Sends post requests directly to Post Service.
- Sends comment requests directly to Comment Service.
- Sends notification reads directly to Notification Service.

Current limitation:

- There is no single public base URL.
- There is no centralized request routing.
- There is no external load balancing across service replicas.
- Cross-cutting concerns like request logging, rate limiting, auth enforcement, and CORS are not centralized.

## Current Internal Service Flow

Services communicate internally through Dapr for synchronous lookup calls and asynchronous event delivery.

```text
Service -> local Dapr sidecar -> target service Dapr sidecar -> target FastAPI service
```

Current Dapr service invocation usage:

- Notification Service calls User Service to resolve followers for `post.created`.
- Notification Service calls Post Service to resolve the post owner for `comment.created`.

Current Dapr pub/sub usage:

- Auth Service publishes `auth.user_registered`.
- Auth Service publishes `auth.user_logged_in`.
- User Service consumes auth events to create profiles and update status.
- Post Service publishes `post.created`.
- Comment Service publishes `comment.created`.
- Notification Service consumes post/comment events and stores notifications.

## Main User Processes

### Register User

```text
Client
  -> Auth Service: POST /auth/register
  -> Auth DB: create auth user
  -> Dapr Pub/Sub: publish auth.user_registered
  -> User Service: consume event
  -> User DB: create user profile and offline status
```

### Login User

```text
Client
  -> Auth Service: POST /auth/login
  -> Auth DB: validate credentials
  -> Auth Service: issue JWT
  -> Dapr Pub/Sub: publish auth.user_logged_in
  -> User Service: consume event
  -> User DB: mark user online
```

### Follow User

```text
Client
  -> User Service: POST /users/{target_user_id}/follow?follower_id=...
  -> User DB: create follow relationship
```

### Create Post

```text
Client
  -> Post Service: POST /posts
  -> Post DB: create post
  -> Dapr Pub/Sub: publish post.created
  -> Notification Service: consume event
  -> User Service via Dapr invocation: get followers
  -> Notification DB: create notifications for followers
```

### Create Comment

```text
Client
  -> Comment Service: POST /comments
  -> Comment DB: create comment
  -> Dapr Pub/Sub: publish comment.created
  -> Notification Service: consume event
  -> Post Service via Dapr invocation: get post owner
  -> Notification DB: create notification for post owner
```

### Read Notifications

```text
Client
  -> Notification Service: GET /notifications?user_id=...
  -> Notification DB: return notifications for user
```

## Future API Gateway Upgrade

When an API gateway is added, clients should stop calling service ports directly. The gateway becomes the single public entrypoint.

Target external flow:

```text
Client
  -> API Gateway: localhost:8080
  -> Route by path to internal service
```

Recommended path routing:

```text
/auth/*          -> auth-service:8000
/users/*         -> user-service:8000
/posts/*         -> post-service:8000
/comments/*      -> comment-service:8000
/notifications/* -> notification-service:8000
```

Gateway responsibilities in the first upgrade:

- Provide one public base URL.
- Route requests to the correct internal service by path.
- Keep direct service ports optional for debugging only.
- Preserve existing service APIs so route handlers do not need to change.

Gateway responsibilities that can be added later:

- JWT validation before forwarding protected routes.
- Request and response logging.
- Rate limiting.
- CORS policy.
- Request IDs and trace headers.
- TLS termination.
- Load balancing across multiple replicas of the same service.

## Load Balancing Model

Current local model:

- One container per service.
- No external gateway-level load balancing.
- Dapr can resolve service-to-service calls by app ID, but local Compose is not currently running multiple replicas.

Future gateway model:

- Run multiple replicas for selected stateless services.
- Gateway routes to available replicas.
- Databases remain service-owned and shared by replicas of the same service.
- Dapr sidecars remain attached to each service replica for internal invocation and pub/sub.

## Documentation Update Rules

Update this file when any of these change:

- A new API gateway or reverse proxy is introduced.
- Public URLs or ports change.
- Path routing rules change.
- Service ownership of an endpoint changes.
- Dapr invocation paths change.
- Pub/sub topics or event consumers change.
- Load balancing or replica strategy changes.

