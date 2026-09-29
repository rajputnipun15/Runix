RUNIX — Error Handling Specification

Document: 18-ERROR-HANDLING.md
Product: RUNIX
Status: Implementation Specification
Version: 1.0
Audience: Frontend, Backend, Runtime, Worker, Infrastructure, QA, DevOps
Depends On:

03-SYSTEM-ARCHITECTURE.md
06-API-SPECIFICATION.md
07-WEBSOCKET-SPECIFICATION.md
08-RUNTIME-ENGINE.md
09-WORKSPACE-FILESYSTEM.md
10-GITHUB-INTEGRATION.md
11-AI-AGENT-SPECIFICATION.md
12-SECURITY-ARCHITECTURE.md
15-PROJECT-TEMPLATES.md
16-TESTING-STRATEGY.md
17-OBSERVABILITY.md
1. Purpose

RUNIX is a distributed cloud development platform where failures can occur across multiple layers:

Browser
   ↓
Next.js Frontend
   ↓
FastAPI Control Plane
   ↓
PostgreSQL / Redis / Workers
   ↓
Runtime Manager
   ↓
Docker Runtime
   ↓
User Application
   ↓
Preview / GitHub / AI / External Services

This document defines how RUNIX detects, classifies, translates, logs, exposes, retries, and recovers from failures.

The objective is to ensure that:

Users receive clear and actionable errors.
Internal implementation details are not leaked.
Errors remain traceable through request IDs and trace IDs.
Runtime failures do not compromise the control plane.
Transient infrastructure failures can recover automatically.
Permanent failures are surfaced clearly.
Frontend behavior remains consistent with the Stitch design.
Errors are observable through logs, metrics, traces, and audit events.
Every critical failure has a defined recovery strategy.
Tests cover expected and unexpected failure paths.
2. Error Handling Principles

RUNIX follows these principles.

2.1 Fail explicitly

Do not silently ignore errors.

Bad:

Runtime failed

Better:

The runtime stopped unexpectedly.

Runtime: Node.js 22
Reason: Process exited with code 1

Actions:
[Restart runtime]
[Open terminal]
[View logs]
2.2 Separate user errors from system errors

User-caused errors:

invalid project name
invalid file path
insufficient permissions
invalid Git branch
conflicting file update
unsupported template

System-caused errors:

database unavailable
runtime manager failure
Docker unavailable
Redis unavailable
GitHub outage
worker failure
internal programming error

The UI must not present internal infrastructure failures as if the user caused them.

2.3 Never expose sensitive internals

Never expose:

stack traces
database connection strings
SQL statements
API keys
OAuth tokens
GitHub credentials
runtime secrets
environment variables
host filesystem paths
Docker socket information
internal service credentials
internal IP addresses unless intentionally public
full exception objects
internal source code
2.4 Every error should be actionable

Where recovery is possible, provide a recovery action.

Examples:

Runtime stopped
[Restart]
File changed externally
[Reload file] [Compare changes]
Git push rejected
[Pull changes]
Preview unavailable
[Restart runtime]

Not every error requires a button.

For example:

You do not have permission to perform this action.

may simply provide:

Error ID: ERR-8F3A21
3. Error Taxonomy

RUNIX errors are divided into the following categories.

Category	Description
VALIDATION	Invalid request data
AUTHENTICATION	User is not authenticated
AUTHORIZATION	User lacks permission
NOT_FOUND	Resource does not exist
CONFLICT	Current state conflicts with requested operation
RATE_LIMIT	Request frequency exceeded
FILESYSTEM	Workspace/file operation failure
RUNTIME	Runtime/container failure
COMMAND	User command execution failure
PREVIEW	Live preview failure
GIT	Local Git operation failure
GITHUB	GitHub integration failure
TEMPLATE	Template resolution/materialization failure
AI	AI agent failure
DATABASE	PostgreSQL failure
CACHE	Redis failure
QUEUE	Worker/job queue failure
NETWORK	Network/external dependency failure
TIMEOUT	Operation exceeded configured timeout
INTERNAL	Unexpected internal failure
UNAVAILABLE	Required service temporarily unavailable
4. Error Code Convention

Every API-visible error must have a stable machine-readable error code.

Format:

<DOMAIN>_<ERROR>

Examples:

AUTH_INVALID_CREDENTIALS
AUTH_SESSION_EXPIRED
PROJECT_NOT_FOUND
PROJECT_ACCESS_DENIED
FILE_NOT_FOUND
FILE_CHANGED
FILE_TOO_LARGE
PATH_TRAVERSAL
WORKSPACE_QUOTA_EXCEEDED
RUNTIME_NOT_RUNNING
RUNTIME_START_FAILED
COMMAND_TIMEOUT
COMMAND_FAILED
GIT_CONFLICT
GIT_PUSH_REJECTED
GITHUB_RATE_LIMITED
GITHUB_REPOSITORY_NOT_FOUND
TEMPLATE_NOT_FOUND
TEMPLATE_VERSION_UNAVAILABLE
AI_APPROVAL_REQUIRED
AI_PATCH_CONFLICT
PREVIEW_UNAVAILABLE
JOB_FAILED
SERVICE_UNAVAILABLE
INTERNAL_ERROR

Error codes are API contracts.

Changing an existing error code requires an API compatibility review.

5. Standard API Error Envelope

All API errors must use a consistent response structure.

5.1 Standard response
{
  "error": {
    "code": "PROJECT_NOT_FOUND",
    "message": "The requested project could not be found.",
    "details": null,
    "request_id": "req_01JABC123",
    "retryable": false
  }
}
6. Error Response Schema

Recommended Pydantic model:

from typing import Any
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Any | None = None
    request_id: str
    retryable: bool = False


class ErrorEnvelope(BaseModel):
    error: ErrorResponse
7. Error Response Rules
7.1 code

Stable machine-readable identifier.

Example:

FILE_CHANGED
7.2 message

Safe human-readable message.

Example:

The file was modified after you opened it.

Do not include:

sqlalchemy.exc.IntegrityError(...)
7.3 details

Optional structured information.

Example:

{
  "path": "src/App.tsx",
  "expected_hash": "abc123",
  "current_hash": "def456"
}

Only include information safe for the authenticated user.

7.4 request_id

Used to correlate the UI error with backend logs.

Example:

req_01JABC123
7.5 retryable

Indicates whether retrying the operation may succeed.

Example:

{
  "retryable": true
}

Do not mark permanent validation errors as retryable.

8. HTTP Status Mapping

RUNIX uses standard HTTP status semantics.

Status	Meaning	Example
400	Malformed request	Invalid JSON
401	Not authenticated	Expired/missing session
403	Not authorized	Project access denied
404	Resource unavailable	Project/file not found
409	State conflict	File changed
410	Resource permanently gone	Deleted runtime/session
413	Payload too large	File exceeds limit
415	Unsupported media type	Unsupported upload
422	Validation failure	Invalid field value
429	Rate limit	Too many requests
500	Unexpected server error	Unhandled exception
502	Upstream failure	GitHub gateway failure
503	Temporarily unavailable	Runtime service unavailable
504	Gateway timeout	Long-running upstream timeout
9. Status Code Rules

Do not use 500 for expected user errors.

Bad:

POST /files
→ 500 FILE_TOO_LARGE

Correct:

413 FILE_TOO_LARGE

Bad:

GET /projects/123
→ 500 PROJECT_NOT_FOUND

Correct:

404 PROJECT_NOT_FOUND

Bad:

PUT /files/content
→ 500 FILE_CHANGED

Correct:

409 FILE_CHANGED
10. Backend Error Architecture

The backend should separate:

HTTP Layer
    ↓
Exception Translation
    ↓
Application Services
    ↓
Domain Exceptions
    ↓
Infrastructure Exceptions

Recommended structure:

backend/
├── app/
│   ├── api/
│   ├── core/
│   │   ├── errors.py
│   │   ├── error_handlers.py
│   │   └── request_context.py
│   ├── services/
│   ├── domain/
│   │   └── exceptions.py
│   ├── infrastructure/
│   └── main.py
11. Domain Exceptions

Business logic should raise domain-specific exceptions.

Example:

class RunixError(Exception):
    code = "INTERNAL_ERROR"
    message = "An unexpected error occurred."
    status_code = 500
    retryable = False


class ProjectNotFoundError(RunixError):
    code = "PROJECT_NOT_FOUND"
    message = "The requested project could not be found."
    status_code = 404


class ProjectAccessDeniedError(RunixError):
    code = "PROJECT_ACCESS_DENIED"
    message = "You do not have access to this project."
    status_code = 403
12. Filesystem Exceptions

Example:

class FileNotFoundError(RunixError):
    code = "FILE_NOT_FOUND"
    message = "The requested file could not be found."
    status_code = 404


class FileChangedError(RunixError):
    code = "FILE_CHANGED"
    message = "The file changed after it was loaded."
    status_code = 409


class FileTooLargeError(RunixError):
    code = "FILE_TOO_LARGE"
    message = "The file exceeds the maximum allowed size."
    status_code = 413


class WorkspaceQuotaExceededError(RunixError):
    code = "WORKSPACE_QUOTA_EXCEEDED"
    message = "The workspace storage quota has been exceeded."
    status_code = 413
13. Path Traversal Errors

Unsafe paths must never reach filesystem operations.

Examples of invalid paths:

../secret
../../etc/passwd
/var/run/docker.sock
C:\Windows\System32
..\..\secret
%2e%2e%2fsecret

Return:

{
  "error": {
    "code": "PATH_TRAVERSAL",
    "message": "The requested path is not allowed.",
    "details": null,
    "request_id": "req_123",
    "retryable": false
  }
}

Do not reveal the resolved host path.

14. FastAPI Exception Handling

Register centralized exception handlers.

Example:

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.exception_handler(RunixError)
async def runix_error_handler(
    request: Request,
    exc: RunixError,
):
    request_id = getattr(request.state, "request_id", "unknown")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": None,
                "request_id": request_id,
                "retryable": exc.retryable,
            }
        },
    )
15. Unexpected Exceptions

Unexpected exceptions must be caught at the HTTP boundary.

They must:

Be logged.
Include request ID and trace ID.
Be counted in metrics.
Return a safe generic response.
Never expose the stack trace to the user.

Example response:

{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "RUNIX encountered an unexpected error.",
    "details": null,
    "request_id": "req_123",
    "retryable": true
  }
}
16. Internal Exception Logging

The actual exception is logged internally.

Example structured event:

{
  "level": "ERROR",
  "event": "unhandled_exception",
  "error_code": "INTERNAL_ERROR",
  "request_id": "req_123",
  "trace_id": "trace_456",
  "service": "api",
  "exception_type": "RuntimeError",
  "message": "internal exception",
  "project_id": "project_123"
}

Stack traces are stored in internal logs only.

17. Validation Errors

FastAPI/Pydantic validation failures must be normalized into RUNIX's error format.

Example:

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more fields are invalid.",
    "details": {
      "fields": [
        {
          "field": "name",
          "message": "Project name is required."
        }
      ]
    },
    "request_id": "req_123",
    "retryable": false
  }
}
18. Authentication Errors

Examples:

AUTH_REQUIRED
AUTH_INVALID_CREDENTIALS
AUTH_SESSION_EXPIRED
AUTH_TOKEN_INVALID
AUTH_ACCOUNT_DISABLED

Example:

{
  "error": {
    "code": "AUTH_SESSION_EXPIRED",
    "message": "Your session has expired. Please sign in again.",
    "details": null,
    "request_id": "req_123",
    "retryable": false
  }
}

Frontend behavior:

401
 ↓
attempt refresh
 ↓
success → retry original request
failure → redirect to sign-in

Never retry invalid credentials indefinitely.

19. Authorization Errors

Return:

403 PROJECT_ACCESS_DENIED

Do not reveal whether a resource exists when doing so would create an information disclosure risk.

Example:

You do not have permission to access this project.
20. Conflict Errors

Use 409 Conflict when the resource exists but its current state prevents the operation.

Examples:

FILE_CHANGED
GIT_CONFLICT
BRANCH_ALREADY_EXISTS
PROJECT_SLUG_EXISTS
RUNTIME_STATE_CONFLICT
JOB_ALREADY_RUNNING
21. Optimistic Concurrency

File updates use the previously defined base_hash.

Request:

{
  "path": "src/App.tsx",
  "content": "...",
  "base_hash": "abc123"
}

If the current file hash differs:

409 FILE_CHANGED

Response:

{
  "error": {
    "code": "FILE_CHANGED",
    "message": "The file changed after it was loaded.",
    "details": {
      "path": "src/App.tsx",
      "current_hash": "def456"
    },
    "request_id": "req_123",
    "retryable": false
  }
}

Frontend actions:

[Reload]
[Compare]
[Keep Mine]

The final action must require an explicit overwrite request.

22. Runtime Error Handling

Runtime failures are represented through runtime state.

Possible states:

creating
starting
running
stopping
stopped
failed
terminating
terminated

The runtime record must contain:

status
failure_reason
updated_at
23. Runtime Start Failure

Example:

Runtime failed to start.

The API may return:

{
  "error": {
    "code": "RUNTIME_START_FAILED",
    "message": "The development runtime could not be started.",
    "details": {
      "runtime_id": "runtime_123"
    },
    "request_id": "req_123",
    "retryable": true
  }
}

The UI should expose:

Runtime failed

The development environment could not be started.

[Retry]
[View Logs]
24. Runtime Crash

If the user process crashes:

runtime.status = running

does not automatically mean the application is healthy.

The runtime manager must distinguish:

Container healthy
User process failed
Development server unavailable

Example:

Runtime: Running
Application: Failed

This prevents misleading UI states.

25. Runtime Recovery

For recoverable runtime failures:

failed
 ↓
reconcile
 ↓
restart
 ↓
starting
 ↓
running

Automatic retries must be bounded.

Recommended:

max automatic restart attempts = 3

After repeated failures:

failed

with a user-visible recovery action.

26. Runtime Failure Reasons

Use stable categories:

IMAGE_PULL_FAILED
CONTAINER_CREATE_FAILED
CONTAINER_START_FAILED
RESOURCE_LIMIT
PROCESS_CRASH
HEALTH_CHECK_FAILED
NETWORK_FAILURE
STORAGE_FAILURE
RUNTIME_TIMEOUT
RUNTIME_SERVICE_UNAVAILABLE
UNKNOWN
27. Command Execution Errors

Commands execute inside the runtime.

A command can fail because:

Command returned non-zero exit code.
Command timed out.
Runtime stopped.
Runtime became unavailable.
Command was cancelled.
Resource limit was exceeded.
28. Command Exit Code

A normal failed command should not be treated as a backend error.

Example:

npm test

returns:

exit_code = 1

The API should report:

COMMAND_FAILED

while preserving the command result.

Example:

{
  "execution_id": "exec_123",
  "status": "failed",
  "exit_code": 1,
  "duration_ms": 8421
}

The command output remains visible in the terminal.

29. Command Timeout

Configured timeout:

RUNIX_COMMAND_TIMEOUT_SECONDS=120

On timeout:

COMMAND_TIMEOUT

Example:

{
  "error": {
    "code": "COMMAND_TIMEOUT",
    "message": "The command exceeded the maximum execution time.",
    "details": {
      "timeout_seconds": 120
    },
    "request_id": "req_123",
    "retryable": false
  }
}

The process must be terminated safely.

30. Command Cancellation

Cancellation should be explicit.

State:

queued
running
cancelling
cancelled
completed
failed
timed_out

Cancellation must not leave orphan processes.

31. WebSocket Errors

WebSocket errors follow the protocol defined in 07-WEBSOCKET-SPECIFICATION.md.

Example:

{
  "type": "error",
  "code": "RUNTIME_NOT_RUNNING",
  "message": "The runtime is not running.",
  "request_id": "req_123"
}
32. Terminal Connection Failure

Possible states:

connecting
connected
reconnecting
disconnected
failed

If the connection drops:

Terminal disconnected.

[Reconnect]

The frontend should use bounded exponential backoff.

Recommended delays:

1s
2s
4s
8s
16s
30s

Maximum:

30 seconds
33. WebSocket Authentication Failure

If authentication fails:

WS_AUTH_FAILED

The server must close the connection.

Do not repeatedly reconnect with invalid credentials.

34. Git Errors

Git operations must distinguish between:

local repository errors
remote errors
authentication errors
conflicts
network failures

Examples:

GIT_NOT_INITIALIZED
GIT_BRANCH_NOT_FOUND
GIT_COMMIT_FAILED
GIT_CONFLICT
GIT_PUSH_REJECTED
GIT_PULL_CONFLICT
GIT_AUTH_FAILED
GIT_REMOTE_UNAVAILABLE
35. Git Conflict

Example:

Your local branch and the remote branch have diverged.

UI:

Push rejected.

Remote changes exist that are not present locally.

[Pull Changes]
[View Diff]

Do not automatically destroy local changes.

36. GitHub Errors

GitHub failures must distinguish:

GITHUB_AUTH_FAILED
GITHUB_APP_NOT_INSTALLED
GITHUB_REPOSITORY_NOT_FOUND
GITHUB_PERMISSION_DENIED
GITHUB_RATE_LIMITED
GITHUB_API_UNAVAILABLE
GITHUB_IMPORT_FAILED
37. GitHub Rate Limits

For HTTP 429 or provider-specific rate-limit responses:

GITHUB_RATE_LIMITED

The backend should respect the provider's retry information where available.

Do not aggressively retry rate-limited requests.

38. GitHub Import Failure

GitHub import is asynchronous.

State:

queued
running
completed
failed
cancelled

Example:

Repository import failed.

The repository could not be imported into the workspace.

[Retry Import]

The user should not receive raw Git output unless explicitly shown in a safe diagnostic area.

39. Template Errors

Template operations can fail at:

template lookup
version resolution
integrity verification
workspace creation
materialization
runtime initialization

Errors:

TEMPLATE_NOT_FOUND
TEMPLATE_VERSION_NOT_FOUND
TEMPLATE_VERSION_UNAVAILABLE
TEMPLATE_INTEGRITY_FAILED
TEMPLATE_MATERIALIZATION_FAILED
TEMPLATE_RUNTIME_FAILED
40. Template Integrity Failure

If the template integrity hash does not match:

TEMPLATE_INTEGRITY_FAILED

Do not materialize or execute the template.

This is a security failure and must generate an internal security event.

41. Preview Errors

Preview failures include:

PREVIEW_RUNTIME_UNAVAILABLE
PREVIEW_PORT_NOT_FOUND
PREVIEW_GATEWAY_UNAVAILABLE
PREVIEW_AUTH_FAILED
PREVIEW_TIMEOUT
PREVIEW_APP_CRASHED

Example:

Preview unavailable.

RUNIX could not connect to the development server on port 5173.

[Restart Runtime]
[Open Terminal]
42. Preview Port Detection

If the expected port is not listening:

PORT_NOT_READY

Do not immediately report a permanent error.

The system should allow a startup grace period.

Example:

starting
 ↓
waiting for port
 ↓
port detected
 ↓
preview ready

If the grace period expires:

PREVIEW_TIMEOUT
43. AI Agent Errors

AI-specific errors include:

AI_PROVIDER_UNAVAILABLE
AI_PROVIDER_TIMEOUT
AI_CONTEXT_LIMIT
AI_TOOL_FAILED
AI_APPROVAL_REQUIRED
AI_PATCH_CONFLICT
AI_PATCH_INVALID
AI_TEST_FAILED
AI_REQUEST_CANCELLED
44. AI Approval Errors

If an operation requires approval:

AI_APPROVAL_REQUIRED

This is not a system failure.

The UI should show:

Approval required

The requested change will modify project files.

[Review Changes]
[Approve]
[Reject]
45. AI Patch Conflict

If files changed after the AI generated a patch:

AI_PATCH_CONFLICT

Do not overwrite user changes automatically.

Recovery:

[Review Diff]
[Regenerate Patch]
[Cancel]
46. AI Provider Failure

If the external model provider fails:

AI_PROVIDER_UNAVAILABLE

Example:

The AI coding service is temporarily unavailable.

Your project files were not changed.

If safe, offer:

[Retry]
47. AI Must Not Fake Success

The frontend must never show:

AI changes applied

unless the backend confirms:

Patch generated.
Patch validated.
Patch applied.
Files persisted.
Result returned successfully.

Likewise:

Tests passed

must only appear after an actual test result.

48. Database Errors

Database failures must be classified.

Examples:

DATABASE_UNAVAILABLE
DATABASE_TIMEOUT
DATABASE_CONSTRAINT
DATABASE_TRANSACTION_FAILED

User-facing responses should remain generic.

Example:

RUNIX could not complete this operation because the service is temporarily unavailable.

Internal logs contain the database exception.

49. Database Constraint Errors

Expected constraints should be translated into domain errors.

Example:

unique project slug violation

becomes:

PROJECT_SLUG_EXISTS

Never expose:

psycopg.errors.UniqueViolation

to the frontend.

50. Redis Errors

Redis is not the source of truth.

If Redis becomes unavailable:

API authentication/session features must follow configured fallback policy.
Queue operations should fail safely.
Runtime state must remain authoritative in PostgreSQL.
Cached information may be temporarily unavailable.
Do not treat Redis state as authoritative runtime state.

Error:

CACHE_UNAVAILABLE

or:

QUEUE_UNAVAILABLE

depending on the affected subsystem.

51. Worker Errors

Workers process asynchronous jobs.

Every job must have:

status
attempt_count
started_at
completed_at
error

Possible states:

queued
running
completed
failed
retrying
cancelled
52. Job Retry Policy

Retry only transient failures.

Retryable:

network timeout
temporary GitHub failure
Redis connection reset
temporary runtime service failure
database connection reset

Not retryable:

invalid input
permission denied
repository does not exist
file conflict
invalid template
authentication failure
53. Exponential Backoff

Recommended:

delay = min(base * 2^attempt + jitter, max_delay)

Example:

Attempt 1 → 1s
Attempt 2 → 2s
Attempt 3 → 4s
Attempt 4 → 8s

Use random jitter to avoid synchronized retries.

54. Retry Limits

Default asynchronous retry policy:

max_attempts = 3

Certain integrations may use a higher limit when justified.

Never create infinite retries.

55. Dead-Letter Handling

Jobs that repeatedly fail should move to a dead-letter state.

Example:

queued
 ↓
running
 ↓
failed
 ↓
retrying
 ↓
failed
 ↓
retrying
 ↓
failed
 ↓
dead_letter

The job must remain inspectable by operators.

56. Idempotency

Operations that may be retried must be idempotent where possible.

Examples:

runtime.start
workspace initialization
GitHub import
deployment creation
job enqueue

Use idempotency keys for operations where duplicate execution could cause damage.

Example:

Idempotency-Key: 01JABC123
57. Duplicate Runtime Creation

The runtime manager must prevent:

POST /runtime/start
POST /runtime/start

from creating two runtime containers for the same project.

Expected result:

existing runtime is reused

or:

RUNTIME_STATE_CONFLICT

depending on current state.

58. Timeout Handling

Every remote or long-running operation needs an explicit timeout.

Examples:

HTTP request timeout
GitHub API timeout
database query timeout
Redis timeout
runtime start timeout
command timeout
preview readiness timeout
AI provider timeout
job execution timeout

Never allow unbounded waits.

59. Cancellation

Long-running operations should support cancellation where practical.

Examples:

AI task
GitHub import
test run
deployment
command
runtime startup

Cancellation must be propagated through all relevant layers.

Example:

Browser
  ↓ cancel
API
  ↓
Job
  ↓
Runtime Manager
  ↓
Process
60. Circuit Breakers

Circuit breakers may be used for unstable external dependencies.

Recommended targets:

GitHub API
AI provider
external deployment providers

States:

closed
open
half-open

Do not use circuit breakers as a substitute for proper timeout and retry configuration.

61. Bulkheads

RUNIX should isolate failures between subsystems.

Example:

AI provider failure

must not make:

file editing
terminal
Git status

unavailable.

Likewise:

GitHub outage

must not prevent:

local project editing
local runtime execution
terminal
62. Graceful Degradation

RUNIX should continue operating when non-critical dependencies fail.

Examples:

GitHub unavailable

Still allow:

editing
terminal
runtime
local Git
AI unavailable

Still allow:

editing
runtime
terminal
tests
Git
Preview unavailable

Still allow:

terminal
editor
runtime
tests
Metrics backend unavailable

Application functionality should continue.

Observability must not become a single point of failure.

63. Frontend Error Architecture

Frontend errors should pass through a consistent API client.

Recommended:

frontend/
├── lib/
│   ├── api-client.ts
│   ├── errors.ts
│   └── error-mapper.ts
├── components/
│   └── errors/
│       ├── ErrorBoundary.tsx
│       ├── ErrorState.tsx
│       ├── ErrorToast.tsx
│       └── RetryButton.tsx
64. API Client Error

Example:

export class RunixApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public status: number,
    public requestId?: string,
    public retryable: boolean = false,
    public details?: unknown,
  ) {
    super(message);
    this.name = "RunixApiError";
  }
}
65. Frontend Error Mapping

Map backend codes to UX behavior.

Example:

const errorActions = {
  FILE_CHANGED: "conflict",
  RUNTIME_START_FAILED: "runtime-retry",
  AUTH_SESSION_EXPIRED: "reauthenticate",
  GITHUB_RATE_LIMITED: "rate-limit",
  PREVIEW_UNAVAILABLE: "preview-retry",
  AI_APPROVAL_REQUIRED: "approval",
};

The frontend must not duplicate backend business logic.

66. Error Boundary

Unexpected React errors must be caught by an error boundary.

Example user experience:

Something went wrong

RUNIX could not render this section.

Error ID: ERR-8F3A21

[Try Again]

Do not display React stack traces.

67. Next.js Error Handling

Use route/page-level error boundaries where appropriate.

Critical areas:

Dashboard
Project workspace
Editor
Terminal
Preview
AI panel
Settings

An error in one secondary panel should not necessarily destroy the entire IDE.

Example:

AI panel failed

should not prevent:

Editor
Terminal
Preview

from working.

68. UI Error Presentation Rules

Use the appropriate UI primitive.

Error type	UI
Minor transient	Toast
Field validation	Inline field error
Save failure	Inline editor/banner
Runtime failure	Runtime status panel
Git conflict	Git panel/banner
Authentication	Auth redirect/modal
Destructive action failure	Modal/dialog
Page failure	Error state
IDE subsystem failure	Panel-level error state
Critical system outage	Global banner
69. Toast Rules

Toasts should be used for short-lived feedback.

Example:

File saved

or:

Failed to save file
[Retry]

Do not put long diagnostic information in a toast.

70. Inline Errors

Use inline errors for context-sensitive problems.

Example:

Project name

[My Project................]

Project name already exists.

This is better than a generic global toast.

71. Global Error Banner

Use global banners only for platform-wide conditions.

Example:

RUNIX services are experiencing degraded availability.

Some runtime operations may be delayed.

Do not display global banners for individual project errors.

72. Error Modals

Use modals when user decisions are required.

Example:

File Conflict

The file changed outside the editor.

Your changes:
Current workspace:
Remote changes:

[Cancel] [Compare] [Overwrite]
73. Error Pages

Required states:

404
403
500
503
offline
maintenance
project unavailable
runtime unavailable

All pages must remain visually consistent with the approved Stitch design.

74. Stitch Alignment

Error states must use the existing RUNIX visual language defined by the Stitch project.

Do not introduce a separate error-page design system.

Maintain:

existing typography
existing spacing
existing dark surfaces
existing borders
existing status indicators
existing button hierarchy
existing iconography
existing panel structure
existing responsive behavior

Errors should feel like part of RUNIX rather than a separate application.

75. Offline Handling

The frontend should detect network loss where practical.

Example:

You are offline.

Changes may not be synchronized until the connection is restored.

The UI must clearly distinguish:

browser offline
API unavailable
WebSocket disconnected
runtime unavailable

These are different failure conditions.

76. Autosave Failures

If an editor save fails:

Save failed

must not silently discard local editor state.

The frontend should preserve the unsaved content in memory.

Where supported, show:

Unsaved changes

and:

[Retry Save]
77. WebSocket Reconnection UX

During temporary disconnect:

Terminal
Reconnecting...

After successful connection:

Terminal
Connected

After bounded retries fail:

Terminal disconnected

[Reconnect]

Avoid excessive notifications during automatic reconnection.

78. Request ID Display

Users should receive an error/support identifier when appropriate.

Example:

Something went wrong.

Request ID: req_01JABC123

This is especially useful for:

500
502
503
504
runtime infrastructure failures
GitHub integration failures
AI provider failures
79. Error IDs

For user-visible errors, the backend request ID may be sufficient.

Optional short support ID:

ERR-8F3A21

The support ID must map internally to:

request_id
trace_id
timestamp
service
error_code

Do not expose internal database IDs unnecessarily.

80. Logging Integration

Every significant error must integrate with the observability system defined in 17-OBSERVABILITY.md.

Minimum correlation fields:

request_id
trace_id
service
environment
error_code
operation
timestamp

When applicable:

user_id
project_id
workspace_id
runtime_id
job_id
execution_id

Avoid high-cardinality metric labels even when these identifiers are available in logs.

81. Error Logging Levels

Use:

WARNING

Expected recoverable problems.

Example:

runtime restart attempt
ERROR

Operation failed.

Example:

GitHub import failed
CRITICAL

Potential system-wide or security-critical failure.

Example:

runtime isolation violation detected
82. Error Metrics

Recommended metrics:

runix_errors_total
runix_http_errors_total
runix_runtime_failures_total
runix_command_failures_total
runix_preview_failures_total
runix_github_errors_total
runix_ai_errors_total
runix_job_failures_total
runix_websocket_errors_total

Useful dimensions:

service
operation
error_code
status_class

Avoid:

user_id
project_id
runtime_id
file_path

as metric labels.

83. Error Rate Monitoring

Track:

total requests
failed requests
error percentage
retry percentage
timeout percentage

Example:

API error rate = failed requests / total requests

Break down by service and error category.

84. Audit Events

Security-sensitive errors may require audit events.

Examples:

AUTH_FAILED
AUTH_SESSION_REJECTED
PROJECT_ACCESS_DENIED
PATH_TRAVERSAL_BLOCKED
GITHUB_AUTH_FAILED
AI_APPROVAL_REJECTED

Audit events must not contain secrets.

85. Security Error Handling

Security failures must fail closed.

Examples:

invalid authorization
invalid runtime token
path traversal
invalid preview token
invalid GitHub callback state

Never fall back to:

allow anyway
86. Path Traversal Response

Do not reveal whether the attempted path exists.

Bad:

/etc/passwd exists but cannot be accessed

Correct:

The requested path is not allowed.
87. Preview Token Failure

If preview authentication fails:

PREVIEW_AUTH_FAILED

Do not reveal:

token expired
token belongs to another project
project exists
port exists

unless that information is safe and necessary.

88. Error Translation Boundary

Infrastructure exceptions must be translated before reaching the HTTP layer.

Example:

Docker exception
      ↓
RuntimeManager
      ↓
RuntimeStartError
      ↓
API error translator
      ↓
RUNTIME_START_FAILED

Not:

Docker exception
      ↓
FastAPI
      ↓
raw Docker error
89. Runtime Docker Errors

The runtime manager may receive errors such as:

image not found
container name conflict
resource unavailable
network creation failure
mount failure
permission failure

These should be normalized into RUNIX runtime errors.

Example:

CONTAINER_CREATE_FAILED

with internal diagnostic metadata.

90. Error Recovery Matrix
Error	Retry	User Action	Automatic Recovery
VALIDATION_ERROR	No	Fix input	No
AUTH_SESSION_EXPIRED	Refresh	Sign in	Yes
PROJECT_NOT_FOUND	No	Navigate elsewhere	No
FILE_CHANGED	No	Compare/reload	No
RUNTIME_START_FAILED	Yes	Restart	Limited
COMMAND_FAILED	Optional	Inspect output	No
COMMAND_TIMEOUT	Usually no	Modify command	No
GIT_CONFLICT	No	Resolve conflict	No
GITHUB_RATE_LIMITED	Delayed	Retry later	Limited
AI_PROVIDER_TIMEOUT	Yes	Retry	Limited
AI_PATCH_CONFLICT	No	Review/regenerate	No
DATABASE_UNAVAILABLE	Yes	Retry	Yes
QUEUE_UNAVAILABLE	Yes	Retry	Yes
PREVIEW_TIMEOUT	Yes	Restart/check app	Limited
INTERNAL_ERROR	Maybe	Retry	Depends
SERVICE_UNAVAILABLE	Yes	Retry	Yes
91. Retry Safety

Never automatically retry:

DELETE operations
financial operations
destructive filesystem operations
Git commits
Git pushes
deployment operations
AI destructive actions

unless the operation has an explicit idempotency mechanism.

92. Retry-After

For rate limiting or temporary service availability, use:

Retry-After: 30

when an appropriate retry time is known.

Frontend should respect this value.

93. Backoff in Frontend

The frontend should not create retry storms.

For automatic retries:

attempt 1 → 1s
attempt 2 → 2s
attempt 3 → 4s

Then stop.

User-triggered retry can restart the process.

94. API Client Retry Policy

Retry only:

408
429
502
503
504

and only when the operation is safe to retry.

Do not automatically retry:

400
401
403
404
409
422
95. Error Handling for Long Operations

Long operations should preferably return a job.

Examples:

GitHub import
runtime creation
test suite
deployment
AI task
large project initialization

Response:

{
  "job_id": "job_123",
  "status": "queued"
}

The frontend then observes job status.

96. Job Failure UI

Example:

Import repository

Failed

The repository could not be imported.

[Retry]
[View Details]

View Details should show safe diagnostic information.

97. Error Details Panel

A diagnostic panel may contain:

Operation
Status
Error code
Request ID
Time
Safe provider/runtime message

Example:

Operation
GitHub repository import

Status
Failed

Error
GITHUB_IMPORT_FAILED

Request ID
req_123

Time
2026-09-29 10:32:11

Do not expose secrets or internal stack traces.

98. Development Environment

Development environments may expose more diagnostics to developers, but still must never expose secrets.

Allowed:

exception type
stack trace
request ID
database error details
Docker error details

Only in developer/operator tooling, not normal end-user responses.

99. Production Environment

Production responses must be sanitized.

Example:

{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "RUNIX encountered an unexpected error.",
    "details": null,
    "request_id": "req_123",
    "retryable": true
  }
}
100. Error Handling in Background Workers

Workers must never terminate silently.

Every failed task must:

Catch exception.
Record error state.
Increment attempt count.
Log structured error.
Retry if retryable.
Move to dead-letter after retry exhaustion.
Emit job failure event.
101. Runtime Reconciliation Errors

The runtime manager periodically reconciles database state with Docker state.

Example:

PostgreSQL:
runtime = running

Docker:
container missing

The runtime manager should mark:

runtime = failed

or recreate the runtime according to recovery policy.

The discrepancy must be observable.

102. Orphan Container Errors

If Docker contains:

runix.managed=true

but no corresponding database runtime exists, the runtime manager must not blindly execute or expose it.

It should:

Detect orphan.
Log the event.
Verify labels.
Apply cleanup policy.
Emit reconciliation metrics.
103. Workspace Errors

Workspace operations must preserve data whenever possible.

For failed writes:

write temporary file
 ↓
fsync
 ↓
atomic rename

If write fails:

original file remains intact
104. Partial Failure

If an operation affects multiple resources, define rollback behavior.

Example:

Create project
 ↓
Create workspace
 ↓
Initialize template
 ↓
Create runtime

If runtime creation fails:

project remains
workspace remains
runtime = failed

Do not delete the user's project automatically unless explicitly defined.

105. Project Creation Failure

Possible stages:

project record
workspace creation
template materialization
runtime initialization

The system must distinguish:

project created
workspace failed

from:

project creation failed

The UI must show the actual state.

106. No Fake Progress

Never show:

Creating...
Installing...
Almost done...

unless backed by actual backend state.

Use actual job states:

queued
running
completed
failed

If detailed progress is unavailable:

Initializing workspace...

must represent a real state, not fabricated progress.

107. Error State Synchronization

Frontend state must be derived from authoritative backend events where applicable.

Examples:

runtime.status
job.status
test_run.status
terminal connection state
preview readiness

Do not infer:

runtime is healthy

simply because the start request returned 202.

108. Test Failure Is Not System Failure

A user test command returning:

exit_code = 1

should be displayed as:

Tests failed

not:

RUNIX server error

This distinction is important.

109. User Application Errors

If a user's application throws:

Error: Cannot connect to database

RUNIX should show it as application/runtime output.

RUNIX must not classify it as a platform infrastructure failure unless RUNIX itself caused the failure.

110. Preview Application Crash

If the user's server crashes:

Preview unavailable

with an option:

[Open Terminal]

The terminal should contain the actual application output.

Do not replace user application errors with generic RUNIX errors.

111. Test Runner Errors

Differentiate:

TEST_RUN_FAILED

from:

TESTS_FAILED
TESTS_FAILED

Tests executed successfully but assertions failed.

TEST_RUN_FAILED

The test framework could not execute.

Examples:

missing dependency
invalid command
runtime unavailable
test process crash
timeout
112. Error Contract Versioning

Error codes are part of the public API contract.

If error structure changes:

API version

must be considered.

Do not randomly change:

error.code

between releases.

113. Error Documentation

Every public error code should be documented.

Recommended registry:

backend/app/core/error_codes.py

or:

docs/api/errors.md

Example:

class ErrorCode:
    PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND"
    PROJECT_ACCESS_DENIED = "PROJECT_ACCESS_DENIED"
    FILE_CHANGED = "FILE_CHANGED"
    RUNTIME_START_FAILED = "RUNTIME_START_FAILED"
114. Frontend Error Registry

The frontend should not hardcode hundreds of business rules.

It may contain presentation mappings:

const errorPresentation = {
  FILE_CHANGED: {
    severity: "warning",
    surface: "editor",
  },
  RUNTIME_START_FAILED: {
    severity: "error",
    surface: "runtime",
  },
};

Unknown errors must fall back safely.

115. Unknown Error Handling

If the frontend receives an unknown code:

UNKNOWN_ERROR

or an unrecognized backend error:

Something went wrong.

Request ID: req_123

Do not crash because an error code was not recognized.

116. API Example — Successful Error Translation

Request:

PUT /api/v1/projects/project_123/files/content

Backend detects hash conflict.

Response:

HTTP/1.1 409 Conflict
Content-Type: application/json
X-Request-ID: req_123
{
  "error": {
    "code": "FILE_CHANGED",
    "message": "The file changed after it was loaded.",
    "details": {
      "path": "src/App.tsx"
    },
    "request_id": "req_123",
    "retryable": false
  }
}
117. API Example — Runtime Unavailable
HTTP/1.1 503 Service Unavailable
{
  "error": {
    "code": "RUNTIME_SERVICE_UNAVAILABLE",
    "message": "The development runtime service is temporarily unavailable.",
    "details": null,
    "request_id": "req_456",
    "retryable": true
  }
}
118. API Example — Authorization
HTTP/1.1 403 Forbidden
{
  "error": {
    "code": "PROJECT_ACCESS_DENIED",
    "message": "You do not have access to this project.",
    "details": null,
    "request_id": "req_789",
    "retryable": false
  }
}
119. API Example — Rate Limit
HTTP/1.1 429 Too Many Requests
Retry-After: 30
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Please try again later.",
    "details": {
      "retry_after_seconds": 30
    },
    "request_id": "req_999",
    "retryable": true
  }
}
120. Error Handling and Security

The following must never be returned to the browser:

DATABASE_URL
JWT signing key
GitHub private key
OAuth client secret
runtime environment secrets
Docker socket path
host filesystem paths
full environment variables
internal stack traces
raw SQL
121. Error Handling and Source Code Privacy

RUNIX must never include the entire user source tree in an error response.

Bad:

{
  "error": {
    "details": {
      "source": "entire source tree..."
    }
  }
}

Correct:

{
  "error": {
    "details": {
      "path": "src/api.ts",
      "line": 42
    }
  }
}

Only include source snippets when explicitly required by the feature and safe to expose.

122. Error Handling and Observability Privacy

Logs must follow the same redaction requirements defined in 17-OBSERVABILITY.md.

Never log:

password
access token
refresh token
API key
GitHub credential
private key
full .env
secret environment variables
terminal secrets
123. Error Handling and Audit Privacy

Audit events should contain:

action
actor
project
timestamp
result
safe metadata

not:

raw request body
password
source code
credentials
terminal output
124. Error Handling Tests

Every error code must have at least one test.

Example:

def test_project_not_found(client):
    response = client.get("/api/v1/projects/nonexistent")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "PROJECT_NOT_FOUND"
125. Error Envelope Tests

Test:

code
message
details
request_id
retryable

Example:

assert "error" in response.json()
assert "code" in response.json()["error"]
assert "request_id" in response.json()["error"]
assert "retryable" in response.json()["error"]
126. Security Error Tests

Required tests:

path traversal
authorization bypass
invalid preview token
invalid WebSocket auth
expired session
invalid GitHub callback state
runtime isolation violation
secret leakage
127. Error Leakage Tests

Automated tests should verify that responses do not contain:

DATABASE_URL
SECRET_KEY
PRIVATE_KEY
Authorization:
password
Docker socket
host filesystem path
stack trace
128. Retry Tests

Test:

retryable error
non-retryable error
maximum attempts
backoff
jitter
Retry-After
idempotency
duplicate job prevention
129. Runtime Error Tests

Required:

runtime image missing
container creation failure
container start failure
runtime timeout
process crash
resource limit
container disappearance
runtime reconciliation
runtime restart
130. Filesystem Error Tests

Required:

file not found
directory not found
file too large
workspace quota
path traversal
absolute path
encoded traversal
symlink escape
file hash conflict
atomic write failure
131. Git Error Tests

Required:

branch missing
commit failure
push rejection
pull conflict
merge conflict
remote unavailable
credential failure
dirty working tree
132. GitHub Error Tests

Required:

installation missing
repository unavailable
permission denied
rate limit
provider outage
import failure
callback failure
invalid state
133. AI Error Tests

Required:

provider timeout
provider unavailable
context limit
tool failure
approval required
patch conflict
invalid patch
test failure
cancellation
134. Frontend Error Tests

Required:

API error parsing
unknown error code
401 refresh
403 state
404 state
409 file conflict
429 retry
500 error boundary
503 service state
WebSocket reconnect
offline state
runtime failure state
preview failure state
135. E2E Error Scenarios

Playwright must cover at least:

Scenario 1 — Runtime Failure
Login
→ Open project
→ Start runtime
→ Simulate runtime failure
→ Verify failed state
→ Restart
→ Verify recovery
Scenario 2 — File Conflict
Open file
→ Modify externally
→ Save
→ Receive FILE_CHANGED
→ Compare
→ Resolve
Scenario 3 — Git Conflict
Modify project
→ Push
→ Simulate remote divergence
→ Verify push rejection
→ Pull
→ Show conflict
Scenario 4 — API Outage
Disable API
→ Open workspace
→ Verify service error
→ Restore API
→ Retry
136. Visual Regression for Errors

Error states must be included in visual regression testing.

At minimum:

runtime failed
terminal disconnected
preview unavailable
file conflict
Git conflict
AI approval
AI failure
API unavailable
empty project
404
500

Visual tests must compare against the approved RUNIX/Stitch visual language.

137. Accessibility

Errors must be accessible.

Requirements:

visible error messages
keyboard navigation
focus management
semantic alerts where appropriate
screen-reader announcements for important asynchronous failures
sufficient contrast
no error information conveyed only by color
keyboard-accessible retry actions

Example:

<div role="alert">
  Failed to save the file.
</div>

Use role="status" for non-critical status updates where appropriate.

138. Error Focus Management

For form validation:

focus first invalid field

For modal errors:

focus dialog

For major page failures:

focus error heading

Do not unexpectedly steal focus for minor toasts.

139. Reduced Motion

Error animations must respect:

prefers-reduced-motion

Do not use excessive error animations.

140. Error Message Writing Rules

Messages should be:

concise
factual
actionable
non-blaming
specific enough to understand
free of internal implementation details

Prefer:

The runtime could not start.

Avoid:

Oops! Something totally broke!

Prefer:

The file changed after you opened it.

Avoid:

Someone messed with your file.
141. Do Not Blame the User

Avoid:

You entered an invalid thing.

Prefer:

Project name must contain between 1 and 100 characters.
142. Error Message Structure

When possible:

What happened
Why it matters
What can be done

Example:

Runtime failed to start.

The development container could not be initialized.

[Retry]
143. Error Severity

RUNIX may use:

info
success
warning
error
critical

Examples:

Info
Reconnecting to terminal...
Warning
Runtime memory usage is high.
Error
Failed to save file.
Critical
RUNIX runtime isolation service is unavailable.
144. Runtime Resource Errors

If memory reaches the configured limit:

RUNTIME_RESOURCE_LIMIT

User-facing:

The runtime exceeded its memory limit.

Current limit: 1 GB

Try stopping unused processes or restarting the runtime.

Do not expose host memory information.

145. Storage Limit Error

If workspace storage exceeds the quota:

WORKSPACE_QUOTA_EXCEEDED

UI:

Workspace storage limit reached.

Delete unused files or increase the workspace limit if your plan allows it.
146. Process Limit Error

If PID limit is exceeded:

RUNTIME_PROCESS_LIMIT

User-facing:

The runtime has reached its process limit.
147. Network Failure

Differentiate:

user application network failure
RUNIX service network failure
external provider network failure

Do not automatically attribute all network errors to RUNIX.

148. External Dependency Failure

For:

GitHub
AI provider
deployment provider
package registry

the UI should identify the affected integration.

Example:

GitHub is temporarily unavailable.

Local project functionality remains available.
149. Error State Persistence

Important asynchronous failures must remain visible until resolved or dismissed.

Examples:

runtime failure
Git conflict
failed import
failed deployment
AI patch conflict

Transient toast notifications do not replace persistent state.

150. Error Recovery Priority

Recovery actions should be ordered:

Safe automatic recovery.
Retry.
Reconnect.
Restart subsystem.
User resolution.
Operator intervention.

Example:

Terminal disconnect
→ automatic reconnect
→ manual reconnect
→ runtime restart
151. Error Handling Checklist

Before merging a feature, verify:

API

Expected errors have stable error codes.

Correct HTTP status codes are used.

Error envelope is consistent.

Request ID is included.

Retryability is accurate.

Sensitive information is excluded.

Unexpected exceptions are caught.

Frontend

Errors are mapped to appropriate UI.

Unknown errors do not crash the application.

Retry actions are safe.

Error boundaries exist.

Offline state is handled.

Loading/error/success states are real.

Stitch visual language is preserved.

Runtime

Runtime failures are persisted.

Runtime recovery is bounded.

Containers cannot escape isolation.

Commands cannot execute on the API host.

Orphan runtimes are reconciled.

Resource-limit failures are handled.

Filesystem

Traversal is blocked.

Quotas are enforced.

File conflicts use hashes.

Failed writes do not corrupt existing files.

Sensitive files are not logged.

Git/GitHub

Conflicts are explicit.

Push rejection is handled.

Provider failures are normalized.

Rate limits are respected.

Credentials are protected.

AI

Provider failures are handled.

Patch conflicts are detected.

Approval requirements are enforced.

No fake completion state exists.

AI cannot bypass runtime security.

Observability

Errors are logged.

Request IDs are available.

Trace IDs are available.

Metrics exist for important error categories.

Security errors create audit events where required.

Secrets are redacted.

Testing

Unit tests exist.

Integration tests exist.

E2E failure scenarios exist.

Security tests exist.

Visual error states are tested.

Retry behavior is tested.

Failure recovery is tested.

152. Definition of Done

Error handling for a RUNIX feature is complete only when:

Expected failures are classified
        ↓
Stable error codes exist
        ↓
Correct HTTP/WS protocol exists
        ↓
Backend exceptions are translated
        ↓
Frontend state is implemented
        ↓
Recovery behavior is defined
        ↓
Sensitive information is protected
        ↓
Logs/metrics/traces exist
        ↓
Audit events exist where required
        ↓
Unit tests pass
        ↓
Integration tests pass
        ↓
E2E failure tests pass
        ↓
Visual regression passes
        ↓
Accessibility checks pass
153. Final Error Handling Rules

The following rules are mandatory for RUNIX:

Never expose raw exceptions to end users.
Every public error must have a stable error code.
Every API error must include a request ID.
Use correct HTTP status semantics.
Do not use 500 for expected user errors.
Never expose secrets, credentials, or internal infrastructure details.
User code must never execute on the API host.
Runtime failures must be represented by authoritative runtime state.
Command failures must be distinguished from RUNIX infrastructure failures.
File conflicts must use optimistic concurrency protection.
Git conflicts must never silently overwrite user work.
AI changes must not bypass approval requirements.
Retries must be bounded and safe.
Non-idempotent operations must not be blindly retried.
Workers must never silently discard failed jobs.
Redis and Docker state must not become the source of truth over PostgreSQL.
Frontend error states must follow the approved Stitch design.
No fake progress or fake success states are permitted.
Every critical failure must be observable.
Every critical recovery path must be tested.
Errors should be actionable whenever recovery is possible.
Subsystem failures should be isolated through graceful degradation.
Security failures must fail closed.
Error handling must preserve user work whenever possible.
A failure in one IDE subsystem must not unnecessarily take down the entire workspace.
154. Implementation Priority

Implement error handling in this order:

Phase 1 — Foundation
Error codes
Domain exceptions
API error envelope
FastAPI handlers
Request ID propagation
Frontend API error parser
Phase 2 — Core Product
Authentication errors
Project errors
Filesystem errors
Runtime errors
Command errors
WebSocket errors
Phase 3 — Developer Integrations
Git errors
GitHub errors
Preview errors
Template errors
Job errors
Phase 4 — Advanced Features
AI errors
Deployment errors
Collaboration errors
Billing errors
Phase 5 — Reliability
Retries
Backoff
Circuit breakers
Dead-letter jobs
Reconciliation
Failure injection
Chaos testing
155. Canonical Error Flow

The canonical RUNIX error flow is:

Operation
   ↓
Exception / Failure
   ↓
Classify
   ↓
Domain Exception
   ↓
Service Boundary
   ↓
API / WebSocket Error Translation
   ↓
Stable Error Code
   ↓
Safe User Message
   ↓
Request ID
   ↓
Frontend Error State
   ↓
Recovery Action

In parallel:

Failure
   ↓
Structured Log
   ↓
Metric
   ↓
Trace
   ↓
Audit Event when required
   ↓
Alert when threshold is exceeded

This architecture ensures that RUNIX remains understandable to users, diagnosable by developers, secure under failure, and resilient across the distributed cloud development stack.