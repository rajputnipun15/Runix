RUNIX — Observability Specification

Document: 17-OBSERVABILITY.md
Product: RUNIX
Version: 1.0
Status: Implementation Specification
Depends On:

03-SYSTEM-ARCHITECTURE.md
04-TECHNICAL-STACK.md
06-API-SPECIFICATION.md
07-WEBSOCKET-SPECIFICATION.md
08-RUNTIME-ENGINE.md
09-WORKSPACE-FILESYSTEM.md
10-GITHUB-INTEGRATION.md
11-AI-AGENT-SPECIFICATION.md
12-SECURITY-ARCHITECTURE.md
16-TESTING-STRATEGY.md
1. Purpose

RUNIX is a distributed cloud development platform with multiple components:

Browser
   ↓
Frontend
   ↓
API
   ↓
Services
   ├── PostgreSQL
   ├── Redis
   ├── Worker
   ├── Runtime Manager
   ├── Docker
   ├── GitHub
   ├── AI Provider
   └── Preview Gateway

Observability provides the ability to answer:

Is RUNIX healthy?
Which component is failing?
Which project is affected?
Which runtime is failing?
How long did an operation take?
Did a deployment introduce a regression?
Why did a runtime fail?
Why did a terminal disconnect?
Why did a GitHub import fail?
Why did an AI operation fail?
Are resource limits being reached?
Are users experiencing increased latency?

Observability is therefore a core platform capability rather than an optional monitoring layer.

2. Observability Pillars

RUNIX uses four primary observability pillars:

Logs
Metrics
Traces
Audit Events

Additionally:

Health Checks
Runtime Events
Alerts
Frontend Telemetry

should be integrated into the platform.

3. Observability Architecture

Recommended architecture:

                         RUNIX
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
          Logs          Metrics         Traces
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                 Observability Stack
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Search         Dashboards     Alerts

The implementation should remain provider-neutral where practical.

4. Observability Goals

RUNIX observability must provide:

service health;
runtime health;
API performance;
database performance;
queue health;
WebSocket health;
preview health;
GitHub integration health;
AI operation health;
security event visibility;
frontend error visibility;
resource utilization.
5. Request Correlation

Every incoming HTTP request should receive a request ID.

Example:

X-Request-ID: req_01HXYZ...

If a trusted request ID is provided by an upstream service, RUNIX may propagate it according to the platform's trust policy.

Otherwise RUNIX should generate one.

6. Request ID Requirements

A request ID must be:

unique enough for operational correlation;
safe to expose to the client;
included in logs;
included in relevant errors;
propagated to internal service calls;
propagated to asynchronous jobs where appropriate.

Example:

{
  "request_id": "req_123456"
}
7. Correlation IDs

RUNIX should distinguish:

request_id
project_id
runtime_id
job_id
execution_id
workspace_id
user_id
trace_id

These identifiers should allow an operator to follow an operation across services.

Example:

request_id
   ↓
project_id
   ↓
runtime_id
   ↓
command_execution_id
   ↓
trace_id
8. User Privacy

Observability data must not become a source of sensitive data leakage.

Do not log:

passwords;
authentication tokens;
GitHub private keys;
API keys;
database credentials;
full environment variables;
private SSH keys;
raw secrets;
unnecessary source-code contents.
9. Structured Logging

RUNIX backend services should emit structured logs.

Preferred format:

{
  "timestamp": "2026-09-29T10:00:00Z",
  "level": "INFO",
  "service": "runtime-manager",
  "event": "runtime.started",
  "request_id": "req_123",
  "project_id": "project_123",
  "runtime_id": "runtime_123",
  "duration_ms": 842,
  "status": "success"
}

Avoid unstructured messages such as:

runtime started successfully somehow
10. Log Levels

RUNIX uses:

DEBUG
INFO
WARNING
ERROR
CRITICAL
10.1 DEBUG

Use for development and detailed diagnostics.

Examples:

file indexing details
runtime reconciliation details
Git command diagnostics

Debug logs should not expose secrets.

Production DEBUG logging should normally be disabled or tightly controlled.

10.2 INFO

Normal operational events:

project.created
runtime.started
runtime.stopped
github.import.completed
job.completed
10.3 WARNING

Unexpected but recoverable conditions:

runtime restart required
GitHub API retry
slow database query
preview connection retry
10.4 ERROR

Operation failed but service remains operational.

Examples:

runtime.start.failed
github.import.failed
file.write.failed
job.failed
10.5 CRITICAL

System-level failure requiring immediate attention.

Examples:

database unavailable
runtime manager unavailable
control-plane startup failure
security boundary failure
11. Standard Log Fields

Common fields:

timestamp
level
service
environment
version
event
request_id
trace_id
user_id
project_id
workspace_id
runtime_id
job_id
execution_id
duration_ms
status
error_code

Not every event needs every field.

Only include identifiers relevant to the operation.

12. Service Identity

Every service must identify itself.

Examples:

frontend
api
worker
runtime-manager
terminal-service
preview-gateway
github-service
ai-service

The actual service boundaries may be combined during V1 deployment.

The logical identity should still be preserved in telemetry.

13. Environment Identification

Telemetry must include:

development
test
staging
production

This prevents accidental mixing of environments.

14. Application Version

Services should expose their version.

Example:

RUNIX_VERSION=1.0.0

Logs and traces should include the deployed version where practical.

This allows operators to correlate incidents with releases.

15. Metrics

RUNIX should expose application metrics through a standard metrics endpoint.

Recommended:

/metrics

The endpoint must not expose secrets or sensitive request data.

16. Metric Naming

Use a consistent naming convention.

Examples:

runix_http_requests_total
runix_http_request_duration_seconds
runix_runtime_starts_total
runix_runtime_failures_total
runix_runtime_start_duration_seconds
runix_terminal_connections
runix_workspace_operations_total

Counters should end with:

_total

Durations should generally use:

_seconds
17. HTTP Metrics

Required metrics:

runix_http_requests_total
runix_http_request_duration_seconds
runix_http_request_errors_total

Useful dimensions:

method
route
status_code

Avoid using arbitrary user IDs or project IDs as metric labels.

18. HTTP Latency

Track:

p50
p90
p95
p99

This helps identify tail-latency problems.

Example:

POST /projects
p95 = 420ms
19. Runtime Metrics

Required metrics:

runix_runtime_created_total
runix_runtime_started_total
runix_runtime_stopped_total
runix_runtime_failed_total
runix_runtime_active
runix_runtime_start_duration_seconds
runix_runtime_lifetime_seconds
20. Runtime Resource Metrics

Track:

CPU usage
memory usage
storage usage
PID count
network usage where available

Example conceptual metrics:

runix_runtime_cpu_usage_ratio
runix_runtime_memory_bytes
runix_runtime_storage_bytes
runix_runtime_process_count
21. Runtime Resource Alerts

Potential warning thresholds:

Memory > 80%
Storage > 80%
CPU sustained > 90%
PID usage > 80%

These are initial operational thresholds.

They should be tuned using real workloads.

22. Runtime Failure Events

Every runtime failure should produce a structured event.

Example:

{
  "event": "runtime.failed",
  "runtime_id": "runtime_123",
  "project_id": "project_123",
  "reason": "OOM",
  "status": "failed"
}

Do not include arbitrary runtime output if it could contain secrets.

23. Runtime Reconciliation Metrics

The runtime manager should expose:

runix_runtime_reconciliation_runs_total
runix_runtime_orphans_detected_total
runix_runtime_state_mismatches_total
runix_runtime_cleanup_total

A persistent increase in state mismatches indicates an infrastructure problem.

24. Workspace Metrics

Track:

runix_workspace_operations_total
runix_workspace_operation_duration_seconds
runix_workspace_errors_total
runix_workspace_bytes_written_total
runix_workspace_bytes_read_total

Operations may include:

read
write
create
delete
rename
search

Do not use full file paths as metric labels.

25. Workspace Error Events

Examples:

workspace.path_invalid
workspace.file_too_large
workspace.quota_exceeded
workspace.file_changed
workspace.write_failed
workspace.not_found
26. Terminal Metrics

Track:

runix_terminal_connections
runix_terminal_connections_total
runix_terminal_disconnects_total
runix_terminal_errors_total
runix_terminal_message_bytes_total
runix_terminal_sessions_duration_seconds
27. Terminal Reliability

Monitor:

connection failures
unexpected disconnects
PTY failures
runtime unavailable errors
backpressure events
reconnect frequency

High reconnect rates may indicate:

runtime instability;
network instability;
WebSocket infrastructure issues.
28. Preview Metrics

Track:

runix_preview_requests_total
runix_preview_errors_total
runix_preview_request_duration_seconds
runix_preview_active_connections
runix_preview_port_detection_total
runix_preview_readiness_duration_seconds
29. Preview Security Events

Log security-relevant events:

preview.unauthorized
preview.invalid_token
preview.expired_token
preview.blocked_port
preview.cross_project_attempt

These should also contribute to security monitoring.

30. Git Metrics

Track:

runix_git_operations_total
runix_git_operation_duration_seconds
runix_git_errors_total

Operation labels may include bounded values:

status
operation

Examples:

status
diff
stage
commit
push
pull
checkout
branch
31. GitHub Metrics

Track:

runix_github_requests_total
runix_github_request_duration_seconds
runix_github_errors_total
runix_github_imports_total
runix_github_import_duration_seconds

Useful status categories:

success
rate_limited
unauthorized
not_found
server_error
timeout
32. GitHub Rate Limiting

Monitor GitHub rate-limit responses.

Repeated rate-limit events should trigger operational visibility.

Do not log access tokens or authorization headers.

33. Job Metrics

Track:

runix_jobs_created_total
runix_jobs_completed_total
runix_jobs_failed_total
runix_jobs_cancelled_total
runix_jobs_active
runix_job_duration_seconds
runix_job_queue_wait_seconds
34. Queue Health

Redis-backed job queues should expose:

queue depth
active jobs
failed jobs
retry count
oldest queued job age

A growing queue indicates worker capacity or dependency problems.

35. Database Metrics

Track:

connection count
connection pool utilization
query latency
transaction duration
query errors
deadlocks
lock waits

Slow-query logging should be enabled according to the deployment environment.

36. Database Alerts

Potential alerts:

database unavailable
connection pool exhausted
high transaction latency
deadlock spike
storage nearing capacity
replication failure

Only applicable metrics should be enabled for the actual PostgreSQL deployment architecture.

37. Redis Metrics

Track:

Redis availability
memory usage
connection count
command latency
queue depth
evictions

Redis should not be treated as the source of truth for project files or persistent project metadata.

38. Frontend Observability

The frontend should track:

JavaScript errors
unhandled promise rejections
API failures
WebSocket failures
workspace load failures
runtime connection failures
preview failures

Telemetry should avoid collecting unnecessary source code.

39. Frontend Performance

Track useful browser performance metrics:

navigation timing
page load
workspace initialization
API latency
WebSocket connection time
editor initialization

Do not capture keystrokes or full editor contents as telemetry.

40. Frontend Error Example

Example event:

{
  "event": "frontend.error",
  "route": "/projects/123/workspace",
  "error_code": "WORKSPACE_LOAD_FAILED",
  "request_id": "req_123",
  "trace_id": "trace_123"
}

Do not include full source files or secrets.

41. Distributed Tracing

RUNIX should use distributed tracing for important service operations.

Recommended technology:

OpenTelemetry

Trace flow example:

Browser
 ↓
API
 ↓
Project Service
 ↓
Workspace Service
 ↓
Runtime Manager
 ↓
Docker
42. Trace Context

Trace context should propagate through:

HTTP;
internal service calls;
asynchronous jobs;
WebSocket-related operations where practical.

Use standard OpenTelemetry context propagation.

43. Important Traces

Trace:

project creation
workspace creation
runtime start
runtime stop
runtime restart
command execution
file write
GitHub import
Git push
Git pull
test execution
AI task
preview readiness
44. Trace Attributes

Useful bounded attributes:

service.name
deployment.environment
http.method
http.route
http.status_code
runix.operation
runix.project_id
runix.runtime_id
runix.job_type

Sensitive values must not be added as trace attributes.

45. Trace Sampling

Production tracing should use controlled sampling.

Possible strategy:

Normal requests → sampled
Errors → higher sampling
Slow requests → higher sampling
Critical operations → retained

Do not retain every request indefinitely.

46. Runtime Trace Correlation

Runtime operations should connect application traces to runtime events.

Example:

POST /runtime/start
       │
       └── trace_id
             │
             ├── runtime.create
             ├── docker.create
             ├── docker.start
             ├── healthcheck
             └── runtime.ready

This makes runtime startup failures diagnosable.

47. Audit Events

Audit events are distinct from normal application logs.

Audit events represent security or user-visible actions.

Examples:

user.login
user.logout
project.created
project.deleted
member.added
member.removed
runtime.started
runtime.stopped
github.connected
github.imported
git.push
git.pull
ai.approved
deployment.created
48. Audit Event Structure

Example:

{
  "event": "project.created",
  "user_id": "user_123",
  "project_id": "project_123",
  "timestamp": "2026-09-29T10:00:00Z",
  "metadata": {
    "template": "react-vite-ts",
    "template_version": "1.0.0"
  }
}
49. Audit vs Application Logs

Do not treat all logs as audit records.

Application log:

runtime.start.failed

Audit event:

runtime.started
user_id=...
project_id=...

Audit records should be more durable and access-controlled.

50. Runtime Event Stream

The runtime manager should produce structured lifecycle events:

runtime.created
runtime.starting
runtime.running
runtime.stopping
runtime.stopped
runtime.failed
runtime.terminated

These events can drive:

UI status;
logs;
metrics;
audit records;
alerting.
51. Event Consistency

Runtime state in PostgreSQL is the durable source of truth.

Docker state is runtime infrastructure state.

Telemetry must not assume that a Docker event alone represents the final RUNIX state.

The runtime manager must reconcile state.

52. Health Checks

RUNIX requires multiple health levels.

Liveness
Readiness
Dependency health
Runtime health
53. Liveness

Example:

GET /health

Purpose:

Determine whether the process is alive.

It should remain lightweight.

54. Readiness

Example:

GET /health/ready

Readiness may verify:

PostgreSQL
Redis
required configuration
critical dependencies

Do not make readiness checks unnecessarily expensive.

55. Dependency Health

The platform should distinguish:

API process healthy

from:

API dependencies unavailable

This prevents misleading health dashboards.

56. Runtime Health

A project runtime should have states such as:

creating
starting
running
stopping
stopped
failed
terminating
terminated

The frontend should use backend state rather than inferring state from arbitrary UI timers.

57. Alerting

Alerts should focus on actionable conditions.

Examples:

API error rate elevated
Database unavailable
Redis unavailable
Runtime failure rate elevated
Runtime startup latency elevated
Queue backlog growing
Preview failure rate elevated
GitHub integration failing
WebSocket disconnect rate elevated
Storage capacity critical
58. Alert Severity

Recommended:

INFO
WARNING
CRITICAL
INFO

Useful operational information.

WARNING

Condition requires investigation.

CRITICAL

Condition requires immediate response.

59. Example Alert
Alert:
RUNIX Runtime Failure Rate High

Condition:
runtime failures > 10% over 10 minutes

Severity:
WARNING

Thresholds must be calibrated after observing actual production behavior.

60. Error Budgets

For mature deployments, RUNIX can define service-level objectives.

Example:

API availability
99.9%

Workspace API success
99.9%

Runtime startup success
99%

Preview readiness
99%

These are initial planning targets, not guarantees.

61. SLO Measurement

SLOs should be measured from user-visible outcomes.

For example:

Runtime startup success
=
successful runtime starts
/
requested runtime starts

Do not count internal retries as separate user requests.

62. Operational Dashboard

RUNIX should eventually provide an internal observability dashboard.

Suggested sections:

System Health
API
Database
Redis
Workers
Runtimes
Terminal
Preview
GitHub
AI
Security
63. System Health Dashboard

Display:

API status
Database status
Redis status
Worker status
Runtime Manager status
Preview status
GitHub integration status
AI provider status

Use actual health data.

No fake green indicators.

64. Runtime Dashboard

Display:

Active runtimes
Starting runtimes
Failed runtimes
Average startup time
CPU usage
Memory usage
Storage usage
Runtime failures

Operators should be able to identify unhealthy runtime clusters quickly.

65. API Dashboard

Display:

Request rate
Error rate
p50 latency
p95 latency
p99 latency
5xx count
4xx count
Top slow endpoints

Routes should be grouped using normalized route patterns.

Do not create a separate metric label for every project ID.

66. Queue Dashboard

Display:

Queue depth
Active jobs
Failed jobs
Retry count
Oldest queued job
Average job duration
67. Security Dashboard

Display security events such as:

authentication failures
authorization failures
path traversal attempts
preview authorization failures
suspicious runtime events
GitHub authentication failures
AI approval violations

Security dashboards must be access-controlled.

68. Log Retention

Retention should be environment-specific.

Example starting policy:

Development → 7 days
Staging → 14 days
Production → 30 days
Audit logs → longer according to security/compliance policy

Actual retention should be determined by infrastructure cost and applicable requirements.

69. Log Redaction

Implement centralized redaction.

Sensitive field names may include:

password
token
access_token
refresh_token
authorization
private_key
client_secret
api_key
secret
database_url
mongodb_uri

Redaction should happen before logs are persisted or transmitted.

70. Source Code Privacy

RUNIX must not automatically log full source files.

For debugging, log:

file count
file path metadata where safe
file size
hash
operation

instead of full source contents.

71. Terminal Privacy

Do not persist full terminal streams by default.

Terminal output can contain:

passwords
tokens
environment variables
private data

Only retain terminal output when explicitly required by a controlled operation, and apply strict redaction.

72. AI Privacy

AI telemetry must not automatically record:

full prompts containing source code;
full repository contents;
secrets;
environment variables;
credentials.

Telemetry should record:

task_id
operation
tool
status
duration
error_code
files_changed_count
tests_result
73. AI Observability

Track:

runix_ai_tasks_total
runix_ai_tasks_completed_total
runix_ai_tasks_failed_total
runix_ai_task_duration_seconds
runix_ai_tool_calls_total
runix_ai_approval_requests_total
runix_ai_patch_apply_failures_total
runix_ai_test_failures_total
74. AI Failure Events

Examples:

ai.provider_timeout
ai.provider_error
ai.tool_denied
ai.approval_required
ai.patch_conflict
ai.patch_failed
ai.tests_failed
ai.task_cancelled
75. GitHub Observability

Track the lifecycle:

OAuth/App authentication
↓
repository listing
↓
repository selection
↓
import
↓
clone
↓
checkout
↓
index
↓
ready

Failures should identify the stage.

76. Slow Operation Detection

RUNIX should identify slow operations automatically.

Examples:

API > threshold
runtime startup > threshold
GitHub import > threshold
workspace write > threshold
preview readiness > threshold
AI task > threshold

Slow operations should be correlated with traces.

77. Error Classification

Errors should have stable codes.

Examples:

AUTH_INVALID
PROJECT_NOT_FOUND
FILE_CHANGED
WORKSPACE_QUOTA_EXCEEDED
RUNTIME_START_FAILED
RUNTIME_TIMEOUT
TERMINAL_CONNECTION_FAILED
PREVIEW_UNAUTHORIZED
GITHUB_IMPORT_FAILED
AI_PROVIDER_ERROR

Stable error codes allow reliable dashboards and alerts.

78. Incident Investigation Flow

When an incident occurs:

Alert
↓
Identify service
↓
Identify request
↓
Find trace
↓
Find related logs
↓
Identify project/runtime if relevant
↓
Inspect metrics
↓
Determine failure stage
↓
Mitigate
↓
Fix
↓
Add regression test
79. Example Runtime Incident

Suppose a user reports:

"Preview is not loading."

The operator should be able to trace:

Project
 ↓
Runtime ID
 ↓
Runtime status
 ↓
Port detection
 ↓
Preview gateway
 ↓
HTTP request
 ↓
Error

This should not require manually guessing which container is involved.

80. Example GitHub Incident

For:

"Repository import failed."

observability should identify:

request_id
job_id
project_id
GitHub repository identifier
import stage
GitHub response category
duration
failure code

Do not expose OAuth credentials.

81. Observability Configuration

Example environment variables:

RUNIX_LOG_LEVEL=INFO
RUNIX_METRICS_ENABLED=true
RUNIX_TRACING_ENABLED=true
RUNIX_TRACING_SAMPLE_RATE=0.10
RUNIX_AUDIT_LOGGING_ENABLED=true

Production configuration must be supplied securely.

82. Local Development

Local developers should be able to inspect:

logs
metrics
traces

without requiring production infrastructure.

A local Docker Compose observability profile may be provided.

83. Testing Observability

Observability itself must be tested.

Tests should verify:

request IDs are generated;
request IDs propagate;
errors produce logs;
metrics increment;
traces are generated;
secrets are redacted;
audit events are created;
runtime events are emitted.
84. Log Testing

Example assertion:

runtime start succeeds

should produce an event similar to:

runtime.started

Tests must not depend on exact timestamps.

85. Metric Testing

For an operation:

POST /projects

verify:

runix_http_requests_total

increments appropriately.

Metric tests should avoid excessive dependence on implementation details.

86. Trace Testing

For critical operations, verify:

trace exists
span exists
service name exists
status exists

Sensitive values must not appear in span attributes.

87. Alert Testing

Alert rules should be validated using controlled test data.

Do not wait for a production outage to discover that an alert rule is invalid.

88. Observability Failure Handling

If the telemetry system is temporarily unavailable:

RUNIX core functionality

should continue where safe.

Observability must not normally become a single point of failure for project execution.

However, security/audit requirements may impose stricter guarantees for specific events.

89. Telemetry Backpressure

Telemetry systems must have bounded resource usage.

RUNIX should avoid:

unbounded log queues
unbounded trace buffers
unbounded terminal telemetry

Telemetry overload must not crash the API or runtime manager.

90. High-Cardinality Rules

Avoid using these as metric labels:

user_id
project_id
runtime_id
file_path
repository_url
arbitrary error message

These may appear in logs/traces where appropriate.

Metrics should use bounded dimensions.

91. Data Classification

Observability data should be classified approximately as:

Public
Internal
Sensitive
Restricted

Examples:

API latency → Internal
Project ID → Sensitive
Authentication token → Restricted
Source code → Sensitive
Password → Restricted

Restricted information must not enter normal telemetry.

92. Access Control

Observability systems must enforce access control.

Not every RUNIX administrator should automatically have access to:

audit logs;
security events;
project-specific diagnostics;
user data;
source-code-related telemetry.
93. Multi-Tenant Isolation

Observability must not allow one customer to inspect another customer's data.

If user-facing diagnostics are introduced:

User A

must only see telemetry associated with resources they are authorized to access.

94. Production Readiness Checklist

Before production:

Logs

Structured logs

Request IDs

Error codes

Secret redaction

Retention policy

Metrics

API metrics

Runtime metrics

Database metrics

Queue metrics

WebSocket metrics

Preview metrics

Tracing

OpenTelemetry

Trace propagation

Runtime traces

GitHub traces

AI traces

Sampling

Audit

Authentication events

Project events

Runtime events

Git events

GitHub events

AI approval events

Alerts

API errors

Database failures

Redis failures

Runtime failures

Queue backlog

Preview failures

Storage capacity

95. Definition of Done

Observability for a RUNIX component is complete when:

structured logs exist;
important metrics exist;
critical operations are traceable;
security-sensitive operations generate audit events;
sensitive information is redacted;
health checks exist where appropriate;
actionable alerts exist;
telemetry itself is tested;
dashboards expose operational health;
documentation identifies how to investigate failures.
96. Final Observability Architecture

The final architecture is:

                           RUNIX
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
        Logs              Metrics            Traces
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
                    Observability Layer
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
    Dashboards             Alerts            Investigation
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                     Operator / Developer

The system must make it possible to move from:

"I know something is broken."

to:

"I know which component failed,
which operation triggered it,
which project/runtime was affected,
what the underlying error was,
and what changed."

That is the operational standard for RUNIX.

97. Final Rules
Every important operation must be observable.
Every request should be correlatable.
Logs must be structured.
Metrics must use bounded labels.
Critical workflows must be traceable.
Security-sensitive actions must generate audit events.
Secrets must never enter telemetry.
Source code must not be logged unnecessarily.
Runtime lifecycle events must be observable.
WebSocket failures must be measurable.
Preview failures must be measurable.
GitHub failures must be diagnosable.
AI operations must be observable without exposing private prompts/source unnecessarily.
PostgreSQL and Redis health must be monitored.
Runtime resource usage must be measurable.
Observability must not become a single point of failure.
Production alerts must be actionable.
The frontend must reflect actual backend/runtime health.
Stitch-derived UI must not display fake health or runtime states.
Every production incident should result in improved telemetry and, where appropriate, a regression test.