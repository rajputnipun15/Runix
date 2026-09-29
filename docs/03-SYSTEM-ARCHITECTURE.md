# RUNIX — System Architecture

## 1. Architecture Style

RUNIX uses a modular service architecture.

V1 should remain operationally simple.

Do not create unnecessary microservices.

Recommended V1 components:

1. Frontend
2. API
3. Worker
4. Runtime Manager
5. PostgreSQL
6. Redis
7. Docker runtime

---

# 2. Frontend

Technology:

Next.js
React
TypeScript

Responsibilities:

- render UI
- manage user interaction
- call APIs
- maintain WebSocket connections
- render editor
- render terminal
- render preview
- display runtime state

The frontend must never contain server secrets.

---

# 3. API

Technology:

FastAPI

Responsibilities:

- authentication
- authorization
- projects
- workspaces
- file operations
- runtime lifecycle requests
- GitHub integration
- job creation
- test requests

The API should remain stateless wherever practical.

---

# 4. Worker

Responsibilities:

- Git clone
- dependency installation
- test execution
- build
- cleanup
- long-running operations

The worker communicates through Redis-backed jobs.

---

# 5. Runtime Manager

The runtime manager controls containers.

Responsibilities:

- create
- start
- stop
- restart
- inspect
- terminate
- resource limits
- health checks

The runtime manager is the only component allowed to perform approved
container lifecycle operations.

---

# 6. PostgreSQL

Stores:

- users
- sessions
- projects
- workspace metadata
- runtimes
- jobs
- tests
- GitHub integration metadata
- audit logs

PostgreSQL does not store the complete project filesystem as the primary
workspace storage mechanism.

---

# 7. Redis

Redis is used for:

- asynchronous jobs
- short-lived coordination state
- queues
- rate limiting where appropriate
- runtime event coordination

Redis is not the system of record.

---

# 8. Docker

Docker provides isolated execution environments.

Each runtime belongs to one project.

The API host and worker host must not expose arbitrary host filesystem access
to user containers.

---

# 9. Request Flow

Example: Start Runtime

Browser
  |
  | POST /runtime/start
  v
API
  |
  | validate/authenticate
  v
Runtime Manager
  |
  | create/start
  v
Docker
  |
  v
Runtime
  |
  | status
  v
API
  |
  v
Browser

---

# 10. Terminal Flow

Browser
  |
  | WebSocket
  v
API WebSocket endpoint
  |
  v
Runtime session
  |
  v
PTY / shell

Output returns through the same controlled connection.

---

# 11. Preview Flow

Application inside runtime:

localhost:5173

        ↓

RUNIX preview proxy

        ↓

Authenticated preview route

        ↓

Browser iframe

---

# 12. Architectural Rules

1. User code never executes on the host.
2. Every project request is authorization-checked.
3. Runtime lifecycle is controlled by Runtime Manager.
4. Long-running operations are asynchronous.
5. PostgreSQL is the metadata source of truth.
6. Redis is not the source of truth.
7. Secrets are server-side only.
8. Frontend does not communicate directly with Docker.