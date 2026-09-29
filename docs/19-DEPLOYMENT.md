RUNIX — Deployment Specification

Document: 19-DEPLOYMENT.md
Product: RUNIX
Status: Implementation Specification
Version: 1.0
Audience: Backend, Frontend, Runtime, Infrastructure, DevOps, QA
Depends On:

03-SYSTEM-ARCHITECTURE.md
04-TECHNICAL-STACK.md
08-RUNTIME-ENGINE.md
09-WORKSPACE-FILESYSTEM.md
12-SECURITY-ARCHITECTURE.md
15-PROJECT-TEMPLATES.md
16-TESTING-STRATEGY.md
17-OBSERVABILITY.md
18-ERROR-HANDLING.md
1. Purpose

This document defines how RUNIX is developed, built, deployed, upgraded, monitored, and recovered across environments.

RUNIX deployment must support:

Local development
CI validation
Development environments
Staging
Production
Database migrations
Runtime image builds
Frontend deployment
Backend deployment
Worker deployment
Runtime manager deployment
Redis
PostgreSQL
Persistent workspace storage
Reverse proxy/API gateway
Preview gateway
Observability
Secrets management
Health checks
Rollbacks
Disaster recovery

The deployment architecture must preserve the core RUNIX security boundary:

Browser
   ↓
RUNIX Frontend
   ↓
Control Plane
   ↓
Runtime Manager
   ↓
Isolated User Runtime

User code must never execute on the control-plane host.

2. Deployment Goals

RUNIX deployment must provide:

Reproducible builds.
Immutable application artifacts.
Versioned runtime images.
Safe database migrations.
Secure secret handling.
Health-based deployments.
Automatic failure detection.
Controlled rollbacks.
Persistent user workspace storage.
Observable infrastructure.
Environment isolation.
Minimal production privileges.
Repeatable local development.
CI-enforced quality gates.
3. Environment Model

RUNIX uses the following environments:

local
   ↓
development
   ↓
staging
   ↓
production

Not every deployment requires a permanent development environment.

Minimum recommended environments:

Environment	Purpose
Local	Developer implementation
CI	Automated validation
Staging	Production-like validation
Production	Real users
4. Environment Isolation

Each environment must have separate:

PostgreSQL database
Redis instance
application configuration
secrets
GitHub integration configuration where possible
AI provider configuration
runtime infrastructure
workspace storage
telemetry environment
domain configuration

Never connect staging to production PostgreSQL.

Never connect local development to production resources.

5. Production Architecture

Recommended initial architecture:

                         Internet
                            │
                            ▼
                     ┌──────────────┐
                     │ DNS / CDN    │
                     └──────┬───────┘
                            │
                  ┌─────────▼─────────┐
                  │ Reverse Proxy /   │
                  │ Load Balancer     │
                  └──────┬──────┬─────┘
                         │      │
                 ┌───────▼─┐  ┌─▼──────────┐
                 │ Next.js │  │ FastAPI    │
                 │ Frontend│  │ API        │
                 └─────────┘  └─────┬──────┘
                                    │
                     ┌──────────────┼──────────────┐
                     │              │              │
                     ▼              ▼              ▼
                PostgreSQL       Redis         Worker
                                                   │
                                                   ▼
                                            Runtime Manager
                                                   │
                                                   ▼
                                           Docker Runtime
                                                   │
                                           ┌───────┴───────┐
                                           ▼               ▼
                                     User Runtime     User Runtime
                                           │               │
                                           └───────┬───────┘
                                                   ▼
                                            Preview Gateway
6. Control Plane

The control plane contains:

Frontend
API
Authentication
Project management
Workspace metadata
Git integration
GitHub integration
AI orchestration
Job management
Runtime orchestration
Observability

The control plane must not execute arbitrary user code.

7. Execution Plane

The execution plane contains:

Runtime Manager
Docker
User runtime containers
PTY sessions
User development servers
Build processes
Test processes
Preview processes

User code executes only here.

8. Initial Infrastructure Model

For the first production implementation, RUNIX may use:

Frontend
FastAPI API
Worker
Runtime Manager
PostgreSQL
Redis
Docker host
Persistent workspace storage
Reverse proxy
Preview gateway

These may initially run on separate processes/services on a controlled infrastructure platform.

As scale increases, services may be separated across hosts or orchestration infrastructure.

9. Containerization

All RUNIX services should have reproducible container images.

Recommended images:

runix/frontend:<version>
runix/api:<version>
runix/worker:<version>
runix/runtime-manager:<version>

Runtime images:

runix/node:22-<version>
runix/python:3.12-<version>
runix/mern:<version>
runix/blank:<version>

Do not use mutable production tags such as:

latest

for runtime execution.

10. Immutable Image References

Production deployments should reference immutable image versions.

Preferred:

runix/api:1.4.0

Better:

runix/api@sha256:<digest>

Runtime images should be pinned by digest where practical.

11. Dockerfile Requirements

Production Dockerfiles must:

use a minimal base image
pin important dependencies
avoid unnecessary packages
run as non-root where practical
contain no secrets
use multi-stage builds where useful
include health checks where appropriate
avoid development tooling in production images
produce deterministic artifacts
12. Frontend Build

RUNIX frontend uses:

Next.js
React
TypeScript
Tailwind CSS

Production build:

npm ci
npm run lint
npm run typecheck
npm run test
npm run build

Only validated builds may be deployed.

13. Frontend Runtime

The production frontend should run in an optimized production mode.

Example:

npm run start

If deployed using a platform supporting Next.js natively, the deployment may use the platform's optimized runtime.

The selected deployment model must preserve:

environment configuration
secure cookies
API routing
WebSocket connectivity
preview URLs
static asset delivery
14. Backend Build

Backend production build must include:

Python
FastAPI
Pydantic
SQLAlchemy
Alembic

Recommended production command:

uvicorn app.main:app --host 0.0.0.0 --port 8000

For multi-worker deployments, worker count must be based on infrastructure capacity.

Do not use development reload mode in production.

Never use:

uvicorn app.main:app --reload

in production.

15. Worker Deployment

Workers process asynchronous jobs such as:

GitHub import
template initialization
test jobs
AI jobs
runtime lifecycle jobs
deployment jobs
cleanup jobs

Workers should run independently from API processes.

The API should enqueue work rather than performing long-running operations synchronously.

16. Runtime Manager Deployment

The runtime manager controls:

container creation
container start
container stop
container restart
resource limits
runtime status
runtime reconciliation
port discovery
cleanup

It requires controlled access to the container runtime.

This privilege must be isolated.

17. Docker Socket Security

The user runtime must never receive access to:

/var/run/docker.sock

The runtime manager may require controlled Docker access.

The runtime manager itself must be considered a highly privileged service.

It must:

validate all runtime parameters
reject privileged containers
reject arbitrary host mounts
reject host networking
enforce resource limits
enforce allowed images
validate runtime labels
prevent arbitrary Docker API exposure
18. Runtime Image Allowlist

V1 runtime creation must use an allowlist.

Example:

runix/node:22
runix/python:3.12
runix/mern:<approved-version>
runix/blank:<approved-version>

Do not allow users to submit:

{
  "image": "any-public-image"
}

in V1.

19. Production Runtime Restrictions

Every user runtime must enforce:

CPU limit
memory limit
storage quota
PID limit
command timeout
idle timeout
network policy
non-root user where practical
no privileged mode
no Docker socket
no host root mount
no arbitrary host mounts

Initial defaults:

CPU: 1 vCPU
RAM: 1 GB
Workspace: 2 GB
PIDs: 256
Command timeout: 120 seconds
Idle timeout: 30 minutes
20. Runtime Labels

Every runtime container must include:

runix.managed=true
runix.runtime_id=<uuid>
runix.project_id=<uuid>
runix.user_id=<uuid>
runix.runtime_type=<type>
runix.version=1

These labels are required for reconciliation and safe cleanup.

21. Workspace Storage

Workspace data must persist independently of runtime container lifecycle.

Example:

/var/lib/runix/workspaces/<project-id>

Runtime:

workspace host path
       ↓
/workspace

Stopping a runtime must not delete the workspace.

22. Workspace Backup

Production workspace storage should support backups or snapshots.

Minimum objectives:

daily backup
retention policy
restore testing

Backup frequency may be increased as product requirements evolve.

Git repositories remain an additional recovery mechanism but must not be treated as the only workspace backup.

23. PostgreSQL Deployment

RUNIX requires PostgreSQL 16+.

Production PostgreSQL should use:

encrypted connections
automated backups
restricted network access
separate application credentials
connection pooling
monitoring
disk monitoring
replication where required by availability objectives
24. PostgreSQL Source of Truth

PostgreSQL is the source of truth for control-plane metadata.

It stores:

users
sessions
projects
memberships
workspaces
runtimes
jobs
Git metadata
test runs
deployments
audit logs

It does not store the entire source tree.

25. Redis Deployment

Redis is used for transient coordination.

Potential uses:

job queues
caching
rate limiting
temporary coordination
WebSocket/session coordination

Redis must not be the authoritative source for:

project ownership
runtime state
workspace contents
Git history
user permissions
26. Redis Persistence

Whether Redis persistence is enabled depends on workload.

Transient queues must have recovery behavior even if Redis is lost.

Critical state must already exist in PostgreSQL.

27. Database Migrations

RUNIX uses Alembic.

Migration workflow:

model change
   ↓
Alembic migration
   ↓
CI validation
   ↓
staging migration
   ↓
staging tests
   ↓
production migration

Never manually modify production schema without a migration.

28. Migration Rules

Migrations must be:

version controlled
reviewed
tested
reversible where practical
safe for rolling deployments

Avoid destructive migrations in the same deployment as application code that still depends on the old schema.

29. Expand-and-Contract Migration Strategy

For breaking schema changes:

Step 1 — Expand

Add new schema without removing old schema.

Step 2 — Deploy

Deploy application supporting both formats.

Step 3 — Migrate

Backfill data.

Step 4 — Switch

Application starts using new fields.

Step 5 — Contract

Remove obsolete schema in a later release.

Example:

Release A:
old_column + new_column

Release B:
application uses new_column

Release C:
remove old_column
30. Migration Command

Production migration should be explicit.

Example:

alembic upgrade head

The deployment pipeline must verify the migration completed successfully before considering the deployment healthy.

31. Migration Failure

If migration fails:

deployment = failed

Do not start application instances that require schema changes that did not complete.

For complex migrations, use a dedicated migration job before application rollout.

32. Database Backup Before Risky Migration

For high-risk migrations:

backup/snapshot
   ↓
migration
   ↓
validation

The backup must be verified as restorable according to operational procedures.

33. Environment Variables

Application configuration uses environment variables.

Example:

RUNIX_ENV=production
RUNIX_API_URL=
RUNIX_FRONTEND_URL=
RUNIX_DATABASE_URL=
RUNIX_REDIS_URL=
RUNIX_RUNTIME_CPU_LIMIT=1
RUNIX_RUNTIME_MEMORY_MB=1024
RUNIX_RUNTIME_STORAGE_MB=2048
RUNIX_RUNTIME_PIDS_LIMIT=256
RUNIX_COMMAND_TIMEOUT_SECONDS=120
RUNIX_RUNTIME_IDLE_TIMEOUT_SECONDS=1800
34. Secrets

Secrets include:

database credentials
session signing keys
GitHub private key
GitHub client secret
webhook secret
AI provider keys
deployment provider credentials
encryption keys

Secrets must never be committed to Git.

Never place production secrets in:

.env
README.md
Dockerfile
frontend source
GitHub repository
client-side JavaScript
logs
35. .env.example

The repository should contain:

.env.example

containing variable names but not actual credentials.

Example:

RUNIX_ENV=development
RUNIX_DATABASE_URL=
RUNIX_REDIS_URL=
RUNIX_GITHUB_APP_ID=
RUNIX_GITHUB_PRIVATE_KEY=
RUNIX_GITHUB_CLIENT_ID=
RUNIX_GITHUB_CLIENT_SECRET=
RUNIX_GITHUB_WEBHOOK_SECRET=
RUNIX_AI_PROVIDER=
RUNIX_AI_API_KEY=
36. Frontend Environment Variables

Only explicitly public configuration may be exposed to the browser.

Example:

NEXT_PUBLIC_RUNIX_API_URL
NEXT_PUBLIC_RUNIX_PREVIEW_BASE_URL

Never expose:

database URL
GitHub private key
AI provider secret
JWT signing secret
internal service credentials
37. Secret Rotation

Secrets must support rotation.

Rotation should be possible without rebuilding user projects.

Potential rotation targets:

session signing keys
GitHub credentials
AI provider keys
database credentials
webhook secrets
38. GitHub Production Configuration

Production GitHub integration should prefer:

GitHub App

with minimal permissions.

Configuration:

RUNIX_GITHUB_APP_ID=
RUNIX_GITHUB_PRIVATE_KEY=
RUNIX_GITHUB_CLIENT_ID=
RUNIX_GITHUB_CLIENT_SECRET=
RUNIX_GITHUB_WEBHOOK_SECRET=
RUNIX_GITHUB_CALLBACK_URL=

Secrets remain server-side.

39. Runtime Image Build Pipeline

Runtime images should be built independently from the API.

Example:

Dockerfile
   ↓
CI build
   ↓
Security scan
   ↓
Test
   ↓
Tag
   ↓
Push registry
   ↓
Digest generated
   ↓
Template registry updated
40. Runtime Image Validation

Before publishing a runtime image, verify:

correct language/runtime version
non-root execution
expected shell
package manager
workspace directory
port behavior
resource compatibility
no unnecessary secrets
no privileged configuration
startup command
health behavior
41. Runtime Image Security Scanning

Images should be scanned for:

known vulnerabilities
unexpected packages
secrets
malicious files
outdated dependencies

Critical findings must block release according to the project's security policy.

42. Runtime Image Versioning

Example:

runix/node:22.1.0
runix/python:3.12.1
runix/mern:1.0.0
runix/blank:1.0.0

Template versions reference approved runtime images.

Published template versions must be immutable.

43. CI/CD Architecture

Recommended pipeline:

Pull Request
   ↓
Lint
   ↓
Typecheck
   ↓
Unit Tests
   ↓
Integration Tests
   ↓
Security Tests
   ↓
Build
   ↓
Docker Image Build
   ↓
Image Scan
   ↓
E2E
   ↓
Staging
   ↓
Smoke Tests
   ↓
Production Approval
   ↓
Production Deployment
44. Pull Request Gates

Every pull request must pass:

frontend lint
frontend typecheck
frontend unit tests
backend lint
backend typecheck
backend unit tests
backend integration tests
security tests
build validation

Runtime-related changes must additionally run runtime isolation tests.

45. Main Branch Rules

The production branch must require:

pull request review
CI success
no unresolved required checks
migration review for schema changes
security review for runtime/security changes

Direct production changes should be avoided.

46. Build Artifacts

Each release should produce immutable artifacts:

frontend image
API image
worker image
runtime-manager image
runtime images

Each artifact should have:

version
commit SHA
build timestamp
dependency metadata
image digest
47. Release Versioning

RUNIX application releases should use semantic versioning where appropriate:

MAJOR.MINOR.PATCH

Example:

1.0.0
1.1.0
1.1.1

Runtime image versions may follow their own compatibility scheme.

48. Git Commit Metadata

Production artifacts should be traceable to source.

Recommended metadata:

RUNIX_VERSION=1.2.0
RUNIX_COMMIT_SHA=<sha>
RUNIX_BUILD_ID=<id>

This allows an operator to answer:

Which source revision is currently running?
49. Deployment Strategy

Initial production deployment may use:

rolling deployment

For higher availability, use:

blue/green

or:

canary

as infrastructure maturity increases.

50. Rolling Deployment

Example:

Current:
API v1

Deploy:
API v2

Instance 1 → v2
Health check
Instance 2 → v2
Health check
...

Traffic should only reach healthy instances.

51. Health Checks

Every service must expose appropriate health endpoints.

API:

GET /health
GET /health/ready
52. Liveness vs Readiness
Liveness

Answers:

Is the process alive?

Example:

GET /health
Readiness

Answers:

Can this instance safely receive traffic?

Example:

GET /health/ready

Readiness may verify:

database connectivity
required configuration
critical dependencies

Do not make liveness depend on every external dependency.

53. Example Health Response
{
  "status": "ok"
}

Readiness:

{
  "status": "ready",
  "dependencies": {
    "database": "ok",
    "redis": "ok"
  }
}

Do not expose credentials or internal connection details.

54. Runtime Health

Runtime health should include:

container running
expected process
resource state
workspace mount
port readiness

A runtime may be:

container healthy
application unhealthy

These states must remain distinct.

55. Preview Health

Preview gateway should verify:

runtime exists
project matches
port is authorized
preview token/session valid
target service available

Never expose arbitrary container ports.

56. Deployment Health Checks

After deployment:

health
 ↓
readiness
 ↓
authentication
 ↓
project API
 ↓
workspace API
 ↓
runtime lifecycle
 ↓
terminal
 ↓
preview

At least a smoke subset must run automatically.

57. Production Smoke Test

Recommended smoke flow:

GET /health
GET /health/ready
authenticate
create/test project where safe
fetch project
fetch files
start runtime
verify runtime running
stop runtime
logout

The production smoke test must use a controlled test account/project and must not modify real user projects.

58. Deployment Failure

If new instances fail readiness:

deployment = failed

Traffic must not be routed to unhealthy instances.

Depending on deployment platform:

rollback

or:

halt rollout
59. Rollback

Rollback should restore:

application version
worker version
runtime-manager version

where compatible.

Example:

v1.5.0
   ↓
v1.6.0
   ↓ failure
rollback
   ↓
v1.5.0
60. Database Rollback

Database rollback requires additional care.

Application rollback is not automatically equivalent to database rollback.

Prefer backward-compatible migrations so that:

old application
new schema

remains temporarily compatible.

Do not blindly execute:

alembic downgrade -1

in production without reviewing data compatibility.

61. Runtime Image Rollback

If a runtime image introduces a regression:

template version
        ↓
previous approved runtime image

New projects may temporarily resolve to the previous runtime image.

Existing projects retain their pinned template/runtime configuration unless explicitly migrated.

62. Existing Project Stability

Deployment changes must not unexpectedly modify existing user environments.

Do not automatically:

upgrade runtime
change dependencies
rewrite workspace
change template

when RUNIX itself is deployed.

63. Template Updates

Template versions are immutable.

Example:

react-vite-ts
  ├── 1.0.0
  └── 1.1.0

Existing project:

template_version = 1.0.0

remains unchanged.

New project:

template_version = 1.1.0

uses the newer version.

64. Deployment and Workspace Data

RUNIX application deployment must not modify:

/var/lib/runix/workspaces/*

except through authorized workspace services.

Deployment scripts must never run destructive workspace cleanup.

65. Deployment and User Containers

Application deployment must not delete active user runtime containers unless explicitly part of a controlled runtime-manager migration.

API rollout should be independent from user runtime lifecycle where possible.

66. Runtime Manager Upgrade

Runtime manager changes require special testing.

Before production rollout:

runtime create
runtime start
runtime stop
runtime restart
terminal
command
preview
resource limits
cleanup
reconciliation

must pass.

67. Runtime Manager Compatibility

Runtime manager should preserve compatibility with:

database runtime records
runtime labels
runtime state machine
workspace mounts
template image references

Schema changes must use migration compatibility.

68. Worker Deployment

Workers should use graceful shutdown.

On termination:

stop accepting new jobs
finish current safe operation
acknowledge/cancel job appropriately
close connections
exit

Do not abruptly terminate workers while they are modifying project state.

69. API Graceful Shutdown

API shutdown should:

stop accepting new work
finish active requests
close DB connections
close Redis connections
close background resources

WebSocket connections should receive appropriate closure behavior.

70. Terminal WebSocket Deployment

If WebSocket connections are routed through multiple API instances, the deployment must support:

sticky routing where required, or
shared connection state/coordination
graceful connection draining
client reconnect behavior

The frontend already supports bounded reconnect behavior.

71. WebSocket Draining

Before terminating an API instance:

mark instance draining
        ↓
stop new WebSocket connections
        ↓
allow existing connections to close
        ↓
terminate

Long-lived terminal sessions should not be abruptly destroyed where avoidable.

72. CDN

Static frontend assets may be served through a CDN.

Cache:

immutable hashed JS
CSS
images
fonts
static assets

Do not cache:

authenticated API responses
private project data
workspace contents
terminal output

unless explicitly designed and securely controlled.

73. HTTP Security

Production should use HTTPS.

Recommended:

TLS 1.2+
HSTS
secure cookies
HTTP-only cookies where applicable
SameSite protection
CSRF protection where cookie-based auth requires it
74. Domain Architecture

Example conceptual domains:

runix.example
api.runix.example
preview.runix.example

Potential separation:

www/runix.example
→ frontend

api.runix.example
→ control plane

*.preview.runix.example
→ preview gateway

Actual domain names are deployment configuration.

75. Preview Domain Security

Preview domains must prevent:

cross-project access
preview token reuse
host access
internal service access
arbitrary port forwarding

Each preview request must resolve:

preview identifier
 ↓
project
 ↓
runtime
 ↓
authorized port
76. Network Architecture

Production should isolate:

public network
control-plane network
database network
runtime network
management network

PostgreSQL should not be publicly accessible.

Redis should not be publicly accessible.

Runtime containers should not directly access internal control-plane services unless explicitly required.

77. Runtime Egress

Runtime internet access may be allowed for:

package installation
dependency downloads
development APIs

but should not expose internal infrastructure.

Runtime network policies should prevent access to:

database
Redis
Docker management API
host metadata services
internal administrative services

unless explicitly required and secured.

78. Resource Monitoring

Production must monitor:

CPU
memory
disk
network
Docker containers
PostgreSQL
Redis
API
workers
runtime manager
preview gateway

See:

17-OBSERVABILITY.md

for telemetry requirements.

79. Disk Monitoring

Workspace storage is critical.

Alert thresholds should include:

70% warning
80% high
90% critical

Exact operational thresholds may be adjusted based on infrastructure.

Disk exhaustion must be treated as a production-critical failure.

80. Runtime Capacity

The infrastructure must monitor:

available CPU
available memory
container count
storage
PID capacity
network capacity

Before starting a runtime, the runtime manager should verify that sufficient capacity exists.

81. Capacity Failure

If insufficient capacity exists:

RUNTIME_CAPACITY_UNAVAILABLE

User-facing:

RUNIX cannot start the development environment right now.

Runtime capacity is temporarily unavailable.

[Retry]

Do not create a partially initialized runtime record without cleanup/reconciliation.

82. Scaling

Initial scaling may be vertical.

As usage increases:

API
 ↓
horizontal scaling
Workers
 ↓
horizontal scaling
Runtime hosts
 ↓
horizontal scaling

Runtime scheduling should eventually support:

runtime host selection
capacity awareness
placement
draining
health
83. Distributed Runtime Evolution

The runtime abstraction should allow:

Runtime Manager
       ↓
Runtime Scheduler
       ↓
Runtime Host A
Runtime Host B
Runtime Host C

without changing the frontend runtime API.

84. Runtime Host Draining

Before removing a runtime host:

mark host draining
        ↓
stop scheduling new runtimes
        ↓
migrate/restart runtimes where supported
        ↓
wait for active runtimes
        ↓
remove host
85. Disaster Recovery

RUNIX must identify recovery targets for:

PostgreSQL
workspace storage
Git metadata
configuration
runtime images
source code repositories
86. Recovery Priority

Recommended recovery order:

1. Infrastructure
2. PostgreSQL
3. Redis
4. Workspace storage
5. API
6. Workers
7. Runtime manager
8. Preview gateway
9. Frontend

Actual sequencing may vary depending on outage type.

87. Recovery Objectives

Initial planning targets:

RPO: 24 hours or better for workspace backups
RTO: 4 hours or better for full control-plane restoration

These are initial targets and should be tightened as production maturity increases.

Git repositories may provide a stronger recovery path for projects that have been pushed.

88. Backup Testing

Backups are not considered valid until restoration is tested.

Required:

backup
 ↓
restore test
 ↓
validate database
 ↓
validate workspace
 ↓
document result
89. Disaster Recovery Test

At least periodically test:

PostgreSQL restoration
workspace restoration
application redeployment
runtime image availability
secret recovery
GitHub integration recovery
DNS/domain recovery
90. Incident Deployment Freeze

During a critical incident:

deployment freeze

may be activated.

Only changes directly required to resolve the incident should be deployed until the system stabilizes.

91. Production Access

Production access must use:

authenticated operator accounts
least privilege
MFA where supported
audited access
restricted network paths
short-lived credentials where practical

Do not share production credentials.

92. SSH / Host Access

If host-level access is required:

use individual operator identities
disable shared accounts
use key-based authentication
log access
restrict permissions
rotate credentials
avoid direct manipulation of application data
93. Infrastructure as Code

Production infrastructure should eventually be represented as code.

Recommended categories:

network
database
Redis
compute
runtime hosts
storage
load balancer
DNS
monitoring
secrets references

Terraform or another approved infrastructure-as-code tool may be used.

94. Configuration as Code

Non-secret configuration should be version controlled.

Examples:

resource defaults
runtime limits
allowed images
health thresholds
feature flags
deployment configuration

Secrets remain in a secure secret manager.

95. Feature Flags

Feature flags may control incomplete or risky features.

Examples:

RUNIX_AI_ENABLED
RUNIX_GITHUB_ENABLED
RUNIX_DEPLOYMENTS_ENABLED
RUNIX_COLLABORATION_ENABLED

Feature flags must not be used to fake functionality.

Disabled features should show a truthful state.

96. Production Feature Rollout

For risky features:

disabled
 ↓
internal
 ↓
staging
 ↓
small production cohort
 ↓
general availability

Do not expose incomplete functionality to all users accidentally.

97. Deployment Observability

Every deployment should emit:

deployment.started
deployment.completed
deployment.failed
deployment.rolled_back

Metadata:

version
commit_sha
environment
operator/automation
timestamp
98. Deployment Metrics

Recommended:

runix_deployments_total
runix_deployment_failures_total
runix_deployment_duration_seconds
runix_rollbacks_total
runix_build_failures_total
runix_migration_failures_total
99. Deployment Logs

Deployment logs must include:

deployment_id
version
commit_sha
environment
service
stage
status
duration

Do not include secrets.

100. Deployment Traceability

Given a production incident, operators must be able to determine:

Which release is running?
Which commit created it?
Which runtime image is active?
Which migration version is active?
Which configuration version is active?
101. Release Manifest

Each production release should generate a manifest.

Example:

{
  "version": "1.4.0",
  "commit_sha": "abc123",
  "frontend": "runix/frontend@sha256:...",
  "api": "runix/api@sha256:...",
  "worker": "runix/worker@sha256:...",
  "runtime_manager": "runix/runtime-manager@sha256:...",
  "created_at": "2026-09-29T00:00:00Z"
}
102. Production Deployment Sequence

Recommended sequence:

1. Validate release
2. Build artifacts
3. Scan artifacts
4. Run tests
5. Publish images
6. Create deployment manifest
7. Backup/snapshot if required
8. Run database migration
9. Deploy API
10. Deploy workers
11. Deploy runtime manager
12. Deploy frontend
13. Run health checks
14. Run smoke tests
15. Verify telemetry
16. Mark deployment successful
103. Frontend Deployment Sequence
build
 ↓
test
 ↓
publish
 ↓
deploy
 ↓
health check
 ↓
static asset validation
 ↓
API connectivity test
 ↓
production smoke test
104. API Deployment Sequence
build
 ↓
unit/integration tests
 ↓
image scan
 ↓
migration compatibility check
 ↓
deploy
 ↓
readiness
 ↓
smoke tests
105. Worker Deployment Sequence
build
 ↓
test
 ↓
deploy
 ↓
connect Redis
 ↓
connect PostgreSQL
 ↓
process controlled test job
 ↓
mark healthy
106. Runtime Manager Deployment Sequence
build
 ↓
security tests
 ↓
runtime isolation tests
 ↓
deploy
 ↓
Docker connectivity
 ↓
controlled runtime creation
 ↓
terminal test
 ↓
preview test
 ↓
cleanup test
107. Local Development

Local development should use Docker Compose where possible.

Recommended services:

frontend
api
worker
runtime-manager
postgres
redis

Docker itself runs the development runtimes.

108. Local Project Structure
RUNIX/
├── frontend/
├── backend/
├── worker/
├── runtime/
├── infrastructure/
├── scripts/
├── tests/
├── docs/
├── docker-compose.yml
├── .env.example
└── README.md
109. Local Docker Compose

Conceptual services:

services:
  postgres:
    ...

  redis:
    ...

  api:
    ...

  worker:
    ...

  runtime-manager:
    ...

  frontend:
    ...

Exact configuration should be maintained in the repository.

110. Local Development Database

Local PostgreSQL should use a dedicated database.

Example:

runix_dev

Do not connect local development to production.

111. Local Runtime Storage

Example:

./.runix/workspaces

mapped to the runtime manager's workspace storage.

This directory must be excluded from Git.

112. Local Runtime Images

Local development may use:

runix/node:22-dev
runix/python:3.12-dev

or locally built equivalent images.

Production images must remain immutable and separately versioned.

113. Development Hot Reload

Development may use:

Next.js dev server
FastAPI reload
worker development mode

Production must not.

114. Local Commands

Recommended:

docker compose up -d

Check services:

docker compose ps

View logs:

docker compose logs -f

Stop:

docker compose down
115. Local Database Migration
alembic upgrade head

Developers should run migrations before testing features requiring new schema.

116. CI Environment

CI must create isolated dependencies.

Recommended:

PostgreSQL service/container
Redis service/container
Docker runtime where required

Tests must not depend on a developer's local environment.

117. CI Database

CI database must be disposable.

Example:

create
 ↓
migrate
 ↓
test
 ↓
destroy
118. CI Runtime Tests

Runtime-related CI jobs may require Docker.

They must verify:

runtime isolation
resource limits
workspace mount
terminal
commands
port discovery
cleanup
119. CI Security Tests

Run:

dependency scanning
secret scanning
SAST
container scanning
path traversal tests
authorization tests
runtime isolation tests
120. Deployment Gate

A release cannot deploy to production unless:

lint              PASS
typecheck         PASS
unit tests        PASS
integration tests PASS
security tests    PASS
build             PASS
image scan        PASS
E2E               PASS
migration checks  PASS

Critical runtime tests are mandatory for runtime-related changes.

121. Failed CI

If a required check fails:

production deployment blocked

No manual bypass should be used without explicit emergency procedure.

122. Emergency Deployment

Emergency deployment may be allowed for:

security vulnerability
critical outage
data integrity issue
production-breaking bug

Emergency deployments must still:

be documented
be traceable
be tested as much as practical
be followed by a full post-incident review
123. Production Rollback Checklist

Before rollback:

identify failing release
identify failure scope
check database compatibility
check runtime compatibility
check workspace impact
check active jobs

Then:

stop rollout
 ↓
restore previous application version
 ↓
verify readiness
 ↓
run smoke tests
 ↓
monitor errors
124. Rollback Verification

After rollback verify:

authentication
projects
workspace API
runtime manager
terminal
preview
Git
GitHub
jobs
observability
125. Deployment and Active Jobs

Before changing worker/runtime-manager versions, inspect:

queued jobs
running jobs
runtime operations
GitHub imports
test runs
AI tasks

Gracefully drain where possible.

126. Deployment and Active Runtimes

A normal API deployment should not require terminating active user runtimes.

If runtime-manager changes require runtime restarts, this must be explicitly planned and communicated.

127. Deployment and Sessions

Session behavior must remain compatible across rolling API deployments.

If session signing keys change:

rotation strategy

must prevent unnecessary mass logout unless security policy requires it.

128. Deployment Security Checklist

Before production:

HTTPS enabled.

Production secrets configured securely.

No secrets in images.

No secrets in Git.

Database not publicly accessible.

Redis not publicly accessible.

Runtime containers not privileged.

Docker socket not exposed to user runtimes.

Host filesystem mounts blocked.

Runtime image allowlist enabled.

API authentication enabled.

Authorization enforced.

Preview authorization enabled.

Rate limiting enabled.

Audit logging enabled.

Security monitoring enabled.

129. Deployment Reliability Checklist

Health checks enabled.

Readiness checks enabled.

Database backups enabled.

Workspace backups enabled.

Restore procedure documented.

Rollback tested.

Migration process tested.

Worker graceful shutdown implemented.

Runtime reconciliation enabled.

Disk monitoring enabled.

Runtime capacity monitoring enabled.

Alerts configured.

Production smoke tests automated.

130. Production Readiness Checklist
Application

Frontend production build passes.

API production build passes.

Worker production build passes.

Runtime manager production build passes.

Infrastructure

PostgreSQL ready.

Redis ready.

Runtime hosts ready.

Workspace storage ready.

Reverse proxy ready.

Preview gateway ready.

Security

Secrets configured.

Runtime isolation validated.

Network controls validated.

Authentication validated.

Authorization validated.

Observability

Logs available.

Metrics available.

Traces available.

Audit events available.

Alerts configured.

Recovery

Backup tested.

Rollback tested.

Disaster recovery documented.

131. Deployment Definition of Done

A deployment implementation is complete when:

Source
  ↓
CI
  ↓
Tests
  ↓
Security
  ↓
Build
  ↓
Immutable artifacts
  ↓
Migration
  ↓
Deployment
  ↓
Health
  ↓
Smoke tests
  ↓
Observability
  ↓
Release verification

all operate successfully.

132. Final Deployment Rules

The following rules are mandatory:

Production artifacts must be immutable.
Production images must not use mutable latest tags.
User code must never execute on the API host.
User containers must never receive Docker socket access.
Production runtime images must be allowlisted.
Workspace data must survive runtime termination.
PostgreSQL is the control-plane source of truth.
Redis is not the source of truth for persistent state.
All database schema changes must use migrations.
Breaking schema changes should use expand-and-contract migration patterns.
Production secrets must remain outside source control.
Frontend bundles must never contain server-side secrets.
Every service must expose appropriate health/readiness information.
Unhealthy instances must not receive production traffic.
Deployments must be traceable to a commit and artifact digest.
Runtime image versions must be traceable to template versions.
Existing projects must not be silently migrated to new templates.
Active user runtimes should remain independent from normal API deployments.
Workers and WebSocket services must support graceful shutdown.
Deployments must have a tested rollback strategy.
Backups must be tested through restoration, not merely created.
Production deployment must be blocked when critical CI/security checks fail.
Runtime isolation tests are mandatory for runtime-related releases.
Deployment telemetry must integrate with RUNIX observability.
No deployment process may silently destroy user project data.
133. Canonical Production Deployment Flow
Developer
   │
   ▼
Git Pull Request
   │
   ▼
CI
   ├── Lint
   ├── Typecheck
   ├── Unit Tests
   ├── Integration Tests
   ├── Security Tests
   ├── Runtime Isolation Tests
   ├── Build
   └── E2E
   │
   ▼
Release Artifact
   │
   ├── Frontend Image
   ├── API Image
   ├── Worker Image
   └── Runtime Manager Image
   │
   ▼
Image Security Scan
   │
   ▼
Artifact Registry
   │
   ▼
Staging
   │
   ├── Migration
   ├── Deployment
   ├── Health Checks
   ├── Smoke Tests
   └── E2E
   │
   ▼
Production Approval
   │
   ▼
Production Migration
   │
   ▼
Production Deployment
   │
   ├── API
   ├── Workers
   ├── Runtime Manager
   └── Frontend
   │
   ▼
Readiness Checks
   │
   ▼
Production Smoke Tests
   │
   ▼
Telemetry Verification
   │
   ▼
Release Complete
134. Canonical Runtime Deployment Flow
Template
   │
   ▼
Template Version
   │
   ▼
Approved Runtime Image
   │
   ▼
Immutable Image Digest
   │
   ▼
Runtime Manager
   │
   ▼
Capacity Check
   │
   ▼
Container Creation
   │
   ├── CPU Limit
   ├── Memory Limit
   ├── PID Limit
   ├── Storage
   ├── Network Policy
   ├── Workspace Mount
   └── Security Restrictions
   │
   ▼
Container Start
   │
   ▼
Health / Process Check
   │
   ▼
Port Detection
   │
   ▼
Preview Authorization
   │
   ▼
Runtime Ready
135. Final Architecture Principle

RUNIX deployment must preserve one fundamental boundary:

                 CONTROL PLANE
┌──────────────────────────────────────────────┐
│ Frontend                                     │
│ API                                          │
│ PostgreSQL                                   │
│ Redis                                        │
│ Workers                                      │
│ Runtime Manager                              │
│ GitHub / AI integrations                     │
└──────────────────────┬───────────────────────┘
                       │
                       │ controlled orchestration
                       ▼
                 EXECUTION PLANE
┌──────────────────────────────────────────────┐
│ User Runtime                                 │
│ User Source Code                             │
│ User Commands                                │
│ Development Server                           │
│ Tests                                        │
│ Builds                                       │
│ Preview                                      │
└──────────────────────────────────────────────┘

The control plane manages what should happen.

The execution plane performs user code execution.

The deployment architecture must never collapse these boundaries.