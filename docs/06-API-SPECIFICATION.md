The RUNIX API reconciles external runtime state with PostgreSQL.


---

## 06 — API SPECIFICATION
# RUNIX API Specification

## 1. API Identity

Base API:

```text
/api/v1

Example development server:

http://localhost:8000/api/v1

Production API domain must be configured through environment variables.

2. API Principles

The RUNIX API is the control plane.

It is responsible for:

authentication
authorization
project management
workspace operations
runtime lifecycle requests
GitHub integration
Git operations
test execution
job management
audit logging

The API must NOT directly execute arbitrary user commands on the host.

User execution must be delegated to the Runtime Manager.

3. Authentication

RUNIX uses authenticated sessions.

Preferred architecture:

Browser
   │
   ├── access token / secure session
   │
   ▼
RUNIX API

For browser applications, authentication credentials should be protected against JavaScript token theft.

Avoid storing long-lived authentication tokens in localStorage.

4. Standard Response Format

Successful response:

{
  "data": {},
  "error": null,
  "request_id": "req_01H..."
}

Error response:

{
  "data": null,
  "error": {
    "code": "PROJECT_NOT_FOUND",
    "message": "Project was not found."
  },
  "request_id": "req_01H..."
}

The request_id must be included in server logs for troubleshooting.

5. HTTP Status Codes

Use:

200 OK
201 Created
202 Accepted
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Unprocessable Entity
429 Too Many Requests
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
6. Authentication Endpoints
POST /auth/register

Create a new RUNIX account.

Request:

{
  "email": "developer@example.com",
  "password": "strong-password",
  "display_name": "Nipun"
}

Validation:

email required
email normalized
password minimum length enforced
display name required
duplicate email rejected

Response:

{
  "data": {
    "user": {
      "id": "uuid",
      "email": "developer@example.com",
      "display_name": "Nipun",
      "email_verified": false
    }
  },
  "error": null,
  "request_id": "req_123"
}
7. POST /auth/login

Request:

{
  "email": "developer@example.com",
  "password": "strong-password"
}

Success:

{
  "data": {
    "user": {
      "id": "uuid",
      "email": "developer@example.com",
      "display_name": "Nipun"
    }
  },
  "error": null,
  "request_id": "req_124"
}

Invalid credentials:

{
  "data": null,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password."
  },
  "request_id": "req_125"
}

Do not reveal whether an email exists.

8. POST /auth/logout

Invalidates the current authenticated session.

Response:

204 No Content
9. POST /auth/refresh

Refreshes the authenticated session.

Response:

{
  "data": {
    "authenticated": true
  },
  "error": null,
  "request_id": "req_126"
}

Refresh tokens must be rotated when appropriate.

10. GET /auth/me

Returns current authenticated user.

Response:

{
  "data": {
    "id": "uuid",
    "email": "developer@example.com",
    "display_name": "Nipun",
    "avatar_url": null
  },
  "error": null,
  "request_id": "req_127"
}
11. Project APIs
GET /projects

Returns projects accessible to the current user.

Optional query parameters:

?page=1
&page_size=20
&search=portfolio
&status=active

Response:

{
  "data": {
    "items": [
      {
        "id": "uuid",
        "name": "Portfolio",
        "slug": "portfolio",
        "template": "react-vite-ts",
        "visibility": "private",
        "status": "active",
        "updated_at": "2026-09-28T10:00:00Z"
      }
    ],
    "page": 1,
    "page_size": 20,
    "total": 1
  },
  "error": null,
  "request_id": "req_128"
}
12. POST /projects

Create a project.

Request:

{
  "name": "Portfolio",
  "description": "Personal developer portfolio",
  "template": "react-vite-ts",
  "visibility": "private"
}

Supported templates:

react-vite-ts
node-ts
python-fastapi
mern
blank-docker

Response:

201 Created
{
  "data": {
    "id": "uuid",
    "name": "Portfolio",
    "slug": "portfolio",
    "template": "react-vite-ts",
    "status": "active"
  },
  "error": null,
  "request_id": "req_129"
}

Project creation should create:

Project
Workspace
Initial files

The process may use a background job for large templates.

13. GET /projects/{project_id}

Returns project details.

Authorization is mandatory.

Response:

{
  "data": {
    "id": "uuid",
    "name": "Portfolio",
    "slug": "portfolio",
    "description": "Personal developer portfolio",
    "template": "react-vite-ts",
    "visibility": "private",
    "status": "active",
    "created_at": "2026-09-28T10:00:00Z",
    "updated_at": "2026-09-28T10:20:00Z"
  },
  "error": null,
  "request_id": "req_130"
}
14. PATCH /projects/{project_id}

Update project metadata.

Request:

{
  "name": "My Portfolio",
  "description": "Developer portfolio and experiments"
}

Only allowed fields should be accepted.

The client must not update:

owner_id
created_at
runtime status
storage_path
15. DELETE /projects/{project_id}

Deletes a project.

Required sequence:

authorize
    ↓
stop runtime
    ↓
terminate runtime
    ↓
close terminal sessions
    ↓
delete workspace
    ↓
delete project metadata

Response:

204 No Content
16. File APIs
GET /projects/{project_id}/files

Returns workspace tree.

Example:

{
  "data": {
    "items": [
      {
        "path": "src",
        "type": "directory"
      },
      {
        "path": "package.json",
        "type": "file",
        "size_bytes": 842
      }
    ]
  },
  "error": null,
  "request_id": "req_131"
}
17. GET /projects/{project_id}/files/content

Query:

?path=src/App.tsx

Response:

{
  "data": {
    "path": "src/App.tsx",
    "content": "import React from 'react';",
    "encoding": "utf-8",
    "size_bytes": 28
  },
  "error": null,
  "request_id": "req_132"
}

Path validation is mandatory.

Reject:

../
../../
absolute host paths
symlinks escaping workspace
18. PUT /projects/{project_id}/files/content

Request:

{
  "path": "src/App.tsx",
  "content": "export default function App() {}"
}

Backend responsibilities:

authorize project
normalize path
validate path remains inside workspace
validate file size
write atomically
update metadata
return updated metadata

Response:

{
  "data": {
    "path": "src/App.tsx",
    "saved": true,
    "size_bytes": 39
  },
  "error": null,
  "request_id": "req_133"
}
19. POST /projects/{project_id}/files

Create file or directory.

Request:

{
  "path": "src/components/Button.tsx",
  "type": "file",
  "content": "export function Button() {}"
}

For directory:

{
  "path": "src/components",
  "type": "directory"
}
20. DELETE /projects/{project_id}/files

Request:

{
  "path": "src/old-component.tsx"
}

Deletion must be restricted to the project workspace.

21. Runtime APIs
GET /projects/{project_id}/runtime

Returns runtime state.

Response:

{
  "data": {
    "id": "uuid",
    "status": "running",
    "runtime_type": "node",
    "image": "runix/node:22",
    "cpu_limit": 1,
    "memory_limit_mb": 1024,
    "storage_limit_mb": 2048,
    "started_at": "2026-09-28T10:30:00Z"
  },
  "error": null,
  "request_id": "req_134"
}
22. POST /projects/{project_id}/runtime/start

Starts a runtime.

Response:

202 Accepted
{
  "data": {
    "runtime_id": "uuid",
    "status": "starting"
  },
  "error": null,
  "request_id": "req_135"
}

The API should not block until the container is fully ready.

23. POST /projects/{project_id}/runtime/stop

Response:

202 Accepted
{
  "data": {
    "runtime_id": "uuid",
    "status": "stopping"
  },
  "error": null,
  "request_id": "req_136"
}
24. POST /projects/{project_id}/runtime/restart

Response:

202 Accepted
{
  "data": {
    "runtime_id": "uuid",
    "status": "starting"
  },
  "error": null,
  "request_id": "req_137"
}
25. Command API
POST /projects/{project_id}/commands

Request:

{
  "command": "npm test",
  "timeout_seconds": 120
}

The command is executed inside the project's isolated runtime.

Response:

202 Accepted
{
  "data": {
    "execution_id": "uuid",
    "status": "queued"
  },
  "error": null,
  "request_id": "req_138"
}

The API host must never execute this command directly.

26. GET /projects/{project_id}/commands/{execution_id}

Response:

{
  "data": {
    "id": "uuid",
    "command": "npm test",
    "status": "completed",
    "exit_code": 0,
    "started_at": "2026-09-28T10:40:00Z",
    "finished_at": "2026-09-28T10:40:04Z"
  },
  "error": null,
  "request_id": "req_139"
}
27. GitHub Integration
GET /github/install

Starts GitHub authorization/install flow.

The actual GitHub implementation may use OAuth or GitHub App installation.

Production preference:

GitHub App

because permissions can be scoped more precisely.

28. GET /github/repositories

Returns repositories accessible to the authenticated user through the configured GitHub integration.

Response:

{
  "data": {
    "repositories": [
      {
        "id": "123456",
        "name": "my-project",
        "full_name": "username/my-project",
        "clone_url": "https://github.com/username/my-project.git",
        "default_branch": "main",
        "private": true
      }
    ]
  },
  "error": null,
  "request_id": "req_140"
}

Never expose GitHub access tokens.

29. POST /projects/{project_id}/github/import

Request:

{
  "repository_id": "123456",
  "branch": "main"
}

Response:

202 Accepted
{
  "data": {
    "job_id": "uuid",
    "status": "queued"
  },
  "error": null,
  "request_id": "req_141"
}

The repository is imported inside the workspace.

Imported repositories must be treated as untrusted code.

30. Git Status
GET /projects/{project_id}/git/status

Response:

{
  "data": {
    "branch": "main",
    "ahead": 0,
    "behind": 0,
    "staged": [],
    "modified": [
      "src/App.tsx"
    ],
    "untracked": [
      "src/components/Button.tsx"
    ]
  },
  "error": null,
  "request_id": "req_142"
}
31. POST /projects/{project_id}/git/commit

Request:

{
  "message": "Add dashboard layout"
}

Response:

{
  "data": {
    "commit_sha": "abc123..."
  },
  "error": null,
  "request_id": "req_143"
}

Git commands execute inside the runtime/workspace environment.

32. POST /projects/{project_id}/git/push

Response:

202 Accepted
{
  "data": {
    "job_id": "uuid",
    "status": "queued"
  },
  "error": null,
  "request_id": "req_144"
}

Credentials must be injected securely.

They must never be written into project files.

33. POST /projects/{project_id}/git/pull

Response:

202 Accepted
34. GET /projects/{project_id}/git/branches

Response:

{
  "data": {
    "branches": [
      {
        "name": "main",
        "is_current": true
      },
      {
        "name": "feature/dashboard",
        "is_current": false
      }
    ]
  },
  "error": null,
  "request_id": "req_145"
}
35. POST /projects/{project_id}/git/checkout

Request:

{
  "branch": "feature/dashboard"
}

The backend must validate the branch name before execution.

36. Test APIs
POST /projects/{project_id}/tests/run

Request:

{
  "command": "npm test"
}

Response:

202 Accepted
{
  "data": {
    "test_run_id": "uuid",
    "status": "queued"
  },
  "error": null,
  "request_id": "req_146"
}
37. GET /projects/{project_id}/tests

Returns recent test runs.

Query:

?page=1&page_size=20
38. GET /projects/{project_id}/tests/{test_run_id}

Returns test details.

Example:

{
  "data": {
    "id": "uuid",
    "status": "passed",
    "framework": "vitest",
    "total_tests": 24,
    "passed_tests": 24,
    "failed_tests": 0,
    "duration_ms": 3810,
    "exit_code": 0
  },
  "error": null,
  "request_id": "req_147"
}
39. Jobs
GET /jobs/{job_id}

Returns background job status.

Response:

{
  "data": {
    "id": "uuid",
    "type": "github.import",
    "status": "completed",
    "result": {
      "files_imported": 142
    }
  },
  "error": null,
  "request_id": "req_148"
}
40. Health APIs
GET /health

Basic process health.

Response:

{
  "status": "ok"
}

This endpoint should remain lightweight.

41. GET /health/ready

Checks required dependencies.

Example:

{
  "status": "ready",
  "dependencies": {
    "postgres": "ok",
    "redis": "ok",
    "runtime_manager": "ok"
  }
}

Returns 503 if required dependencies are unavailable.

42. Authorization

Every project endpoint must verify:

authenticated user
        ↓
project exists
        ↓
user owns project OR is project member
        ↓
role permits requested operation

Example:

project = await project_repository.get(project_id)

if project is None:
    raise ProjectNotFound()

membership = await membership_repository.get(
    project_id=project.id,
    user_id=current_user.id,
)

if membership is None:
    raise ProjectAccessDenied()
43. Rate Limiting

Rate-limit sensitive endpoints.

Especially:

/auth/login
/auth/register
/auth/forgot-password
/projects
/runtime/start
/runtime/restart
/commands
/tests/run
/github/*

Runtime start and command execution should have stricter limits than ordinary metadata requests.

44. Request Validation

Use Pydantic models.

Never pass raw request bodies directly to:

SQL
Docker
filesystem
shell
Git
GitHub

Every boundary must validate input.

45. API Layer Structure

Recommended:

backend/app/
├── main.py
├── api/
│   └── v1/
│       ├── auth.py
│       ├── projects.py
│       ├── files.py
│       ├── runtimes.py
│       ├── commands.py
│       ├── github.py
│       ├── git.py
│       ├── tests.py
│       ├── jobs.py
│       └── health.py
│
├── schemas/
│   ├── auth.py
│   ├── projects.py
│   ├── files.py
│   ├── runtime.py
│   ├── git.py
│   └── tests.py
│
├── services/
│   ├── auth_service.py
│   ├── project_service.py
│   ├── workspace_service.py
│   ├── runtime_service.py
│   ├── github_service.py
│   ├── git_service.py
│   └── test_service.py
│
├── repositories/
│   ├── user_repository.py
│   ├── project_repository.py
│   ├── runtime_repository.py
│   └── job_repository.py
│
└── core/
    ├── config.py
    ├── security.py
    └── dependencies.py
46. Service Boundary Rule

Routes should remain thin.

Preferred:

HTTP Request
    ↓
Router
    ↓
Schema validation
    ↓
Service
    ↓
Repository / Runtime Manager
    ↓
Database / Runtime

Avoid putting business logic directly inside route handlers.

47. API Documentation

FastAPI automatically exposes:

/docs

and:

/openapi.json

Development documentation should remain enabled.

Production exposure should be configurable.

The OpenAPI specification must remain synchronized with the actual API implementation.

48. API Versioning

Initial:

/api/v1

Breaking API changes require:

/api/v2

Do not silently break existing V1 contracts.

49. Request IDs

Every API request must receive a request ID.

Example:

X-Request-ID: req_01J...

If the client supplies a valid request ID, the backend may propagate it subject to validation.

The request ID must appear in:

API response
application logs
relevant worker logs
audit records where appropriate
50. API Security Rules

The API must never:

execute shell commands on the API host
expose Docker socket access
return secrets
trust client-provided ownership
trust client-provided filesystem paths
trust client-provided runtime IDs without authorization
allow arbitrary container configuration
allow arbitrary host paths
allow unrestricted host networking
expose internal service credentials

All execution must pass through approved runtime abstractions.


---

### Next sequence

The next files are the execution-critical ones:

1. `07-WEBSOCKET-SPECIFICATION.md` — terminal/PTTY protocol
2. `08-RUNTIME-ENGINE.md` — Docker isolation, lifecycle, resource limits, port detection
3. `09-WORKSPACE-FILESYSTEM.md` — persistent project filesystem and secure path handling

These three define the part that makes **RUNIX an actual cloud IDE rather than just a dashboard U