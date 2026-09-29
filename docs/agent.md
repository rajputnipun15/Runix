RUNIX — AGENTS.md

Build. Run. Ship. Anywhere.

This file is the implementation contract for AI coding agents, Antigravity, and human developers working on the RUNIX repository.

1. Purpose

RUNIX is a browser-based cloud development platform / cloud IDE.

The repository contains the specifications required to implement RUNIX as a real, production-oriented developer platform.

The implementation must follow the documentation in /docs and the approved RUNIX Stitch project.

This file defines:

implementation rules
source-of-truth hierarchy
architecture constraints
frontend rules
security requirements
runtime isolation requirements
testing requirements
development workflow
phase boundaries
prohibited shortcuts
completion criteria

An agent MUST read this file before making substantial changes to the RUNIX codebase.

2. Product Identity
Product

RUNIX

Tagline

Build. Run. Ship. Anywhere.

Product Category

Browser-based cloud development platform / cloud IDE.

Core Experience

A developer should be able to:

Sign in.
Create or import a project.
Select a project template.
Open the cloud workspace.
Browse and edit files.
Save changes.
Start an isolated runtime.
Open an interactive terminal.
Run commands.
Start a development server.
Open a live preview.
Run tests.
Inspect Git changes.
Commit changes.
Push changes to GitHub.
Use the AI coding agent when enabled.
Deploy when deployment functionality is implemented.

RUNIX must perform these operations using real backend functionality.

Fake buttons, simulated runtime states, fake terminal output, fake Git status, fake AI responses, and fake persistence are prohibited in production functionality.

3. Source of Truth Hierarchy

When implementing RUNIX, use the following precedence order.

3.1 Security and Runtime Safety

Security requirements and runtime isolation requirements always take precedence over convenience.

Relevant documents:

12-SECURITY-ARCHITECTURE.md
08-RUNTIME-ENGINE.md
09-WORKSPACE-FILESYSTEM.md
16-TESTING-STRATEGY.md
21-DEFINITION-OF-DONE.md

Never weaken a security boundary merely to make a feature easier to implement.

3.2 Approved Product Architecture

Use:

03-SYSTEM-ARCHITECTURE.md
04-TECHNICAL-STACK.md
05-DATABASE-SCHEMA.md
06-API-SPECIFICATION.md
07-WEBSOCKET-SPECIFICATION.md

These documents define how RUNIX components communicate and where responsibilities belong.

3.3 Product Requirements

Use:

01-PRD.md
02-FUNCTIONAL-REQUIREMENTS.md
00-PROJECT-OVERVIEW.md

These define what RUNIX is supposed to do.

3.4 Frontend Visual Source of Truth

The approved RUNIX Stitch project is the primary visual source of truth.

Stitch project:

RUNIX Cloud Development Platform UI

Project ID:

2390441801388154937

Approved screens include:

Landing page
Developer sign-in
Developer dashboard
New workspace creation
Create workspace
Cloud IDE
Interactive cloud IDE
Developer profile/avatar

The frontend implementation MUST be based on this Stitch project.

Do not replace the Stitch design with a generic dashboard, generic SaaS UI, or independently invented visual system.

3.5 Frontend Technical Specification

Use:

13-FRONTEND-SPECIFICATION.md
14-DESIGN-SYSTEM.md

These documents define how the Stitch design should be implemented technically.

3.6 Delivery and Completion Rules

Use:

20-ROADMAP.md
21-DEFINITION-OF-DONE.md

These determine implementation order and completion criteria.

4. Repository Structure

The expected repository structure is:

RUNIX/
├── AGENTS.md
├── README.md
│
├── docs/
│   ├── 00-PROJECT-OVERVIEW.md
│   ├── 01-PRD.md
│   ├── 02-FUNCTIONAL-REQUIREMENTS.md
│   ├── 03-SYSTEM-ARCHITECTURE.md
│   ├── 04-TECHNICAL-STACK.md
│   ├── 05-DATABASE-SCHEMA.md
│   ├── 06-API-SPECIFICATION.md
│   ├── 07-WEBSOCKET-SPECIFICATION.md
│   ├── 08-RUNTIME-ENGINE.md
│   ├── 09-WORKSPACE-FILESYSTEM.md
│   ├── 10-GITHUB-INTEGRATION.md
│   ├── 11-AI-AGENT-SPECIFICATION.md
│   ├── 12-SECURITY-ARCHITECTURE.md
│   ├── 13-FRONTEND-SPECIFICATION.md
│   ├── 14-DESIGN-SYSTEM.md
│   ├── 15-PROJECT-TEMPLATES.md
│   ├── 16-TESTING-STRATEGY.md
│   ├── 17-OBSERVABILITY.md
│   ├── 18-ERROR-HANDLING.md
│   ├── 19-DEPLOYMENT.md
│   ├── 20-ROADMAP.md
│   └── 21-DEFINITION-OF-DONE.md
│
├── frontend/
├── backend/
├── worker/
├── runtime/
├── infrastructure/
├── scripts/
├── tests/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── ...

Do not create unnecessary top-level directories.

If the existing repository differs from this structure, inspect it before restructuring.

Do not perform a destructive repository restructuring merely to match this document.

5. Required Technology Stack
Frontend

Use:

Next.js
React
TypeScript
Tailwind CSS
Monaco Editor
xterm.js
Playwright
Vitest
React Testing Library
Backend

Use:

Python 3.11+
FastAPI
Pydantic
SQLAlchemy
Alembic
pytest
pytest-asyncio
httpx
Data Layer

Use:

PostgreSQL 16+
Redis 7+

PostgreSQL is the source of truth for control-plane state.

Redis is for transient coordination, queues, caching, locks, and other explicitly defined temporary state.

Redis MUST NOT become the authoritative project database.

Runtime

Use:

Docker
isolated runtime containers
persistent workspace storage
PTY for interactive terminals

User code MUST execute inside the runtime environment.

GitHub

Production integration should use a GitHub App where practical.

Credentials must remain server-side.

6. Fundamental Architecture Rule

RUNIX has two major planes.

Control Plane

Responsible for:

authentication
users
projects
permissions
workspace metadata
runtime lifecycle
jobs
GitHub integration
configuration
API
audit logs
orchestration
observability
Execution Plane

Responsible for:

user source code
package installation
development servers
terminal commands
tests
builds
Git commands
application processes
7. Critical Runtime Boundary
NEVER execute user code on the API host.

The following MUST NOT execute user-controlled code directly on the FastAPI/API server:

npm install
npm run dev
npm test
python app.py
pytest
pip install
node script.js
bash user-script.sh
git hooks
repository lifecycle scripts

Instead:

Browser
   ↓
RUNIX API
   ↓
Runtime Manager
   ↓
Isolated Docker Runtime
   ↓
User Code

This boundary is non-negotiable.

8. Docker Security Rules

User runtimes MUST NOT use:

--privileged

User runtimes MUST NOT receive:

/var/run/docker.sock

User runtimes MUST NOT receive:

/

or arbitrary host filesystem mounts.

Do not expose the Docker daemon to user code.

Do not provide host networking.

Do not run user code as root unless explicitly required by a controlled infrastructure operation.

Use resource limits.

Initial defaults:

CPU: 1 vCPU
RAM: 1024 MB
Workspace: 2048 MB
PIDs: 256
Command timeout: 120 seconds
Runtime idle timeout: 1800 seconds
9. Runtime Environment Variables

The runtime configuration should support:

RUNIX_RUNTIME_CPU_LIMIT=1
RUNIX_RUNTIME_MEMORY_MB=1024
RUNIX_RUNTIME_STORAGE_MB=2048
RUNIX_RUNTIME_PIDS_LIMIT=256
RUNIX_COMMAND_TIMEOUT_SECONDS=120
RUNIX_RUNTIME_IDLE_TIMEOUT_SECONDS=1800

Do not hardcode these values throughout the codebase.

Use centralized configuration.

10. Workspace Rules

Each project has one persistent workspace.

Example:

/var/lib/runix/workspaces/<project-id>

The runtime receives:

/workspace

mapped to the project workspace.

Path Security

All file APIs MUST operate on workspace-relative paths.

Reject:

/
../
../../
../../../

and equivalent encoded traversal.

Reject:

absolute Unix paths
Windows drive paths
UNC paths
null bytes
paths escaping workspace boundaries

Always resolve and verify containment.

Example

Allowed:

src/main.ts
src/components/Button.tsx
README.md
.env.example

Rejected:

../../etc/passwd
/etc/passwd
C:\Windows\System32
..\..\secret
11. Sensitive Data

Never log:

passwords
password hashes
access tokens
refresh tokens
GitHub credentials
private keys
API keys
complete environment variables
secrets
authentication cookies
terminal secrets
sensitive repository credentials

Do not expose secrets to the browser unless explicitly required and safe.

Do not place server credentials in:

NEXT_PUBLIC_*

or equivalent client-exposed configuration.

12. Authentication

All protected API routes require authentication.

Authentication must be implemented centrally.

Do not create feature-specific authentication bypasses.

Every protected request must establish:

authenticated user

before project authorization is evaluated.

13. Authorization

Authentication answers:

Who is the user?

Authorization answers:

Is this user allowed to access this resource?

Every project-scoped endpoint must verify project access.

Never trust:

project_id
user_id
workspace_id
runtime_id
job_id

from the client without server-side authorization.

14. API Architecture

The API base path is:

/api/v1

Use the documented API specification.

Routes should remain thin.

Preferred structure:

Router
   ↓
Service
   ↓
Repository / Infrastructure
   ↓
Database / Runtime / External System

Do not put large business workflows directly inside FastAPI route functions.

15. API Contract Discipline

When implementing an endpoint:

Follow 06-API-SPECIFICATION.md.
Define request schema.
Define response schema.
Validate input.
Authenticate.
Authorize.
Execute service operation.
Return documented response.
Handle documented errors.
Add tests.

Do not silently invent incompatible response structures.

16. Database Rules

PostgreSQL stores control-plane metadata.

It should contain information such as:

users
sessions
projects
project members
workspaces
runtime metadata
terminal sessions
command executions
Git repositories
branches
jobs
test runs
deployments
audit events

Do not store the entire project filesystem in PostgreSQL unless explicitly required.

Project source belongs in the workspace filesystem and Git repository.

17. Database Migration Rules

Use Alembic.

Never modify an already-applied migration casually.

For schema changes:

model change
    ↓
migration
    ↓
migration test
    ↓
application compatibility
    ↓
integration test

Production schema changes should use expand-and-contract techniques when necessary.

18. Frontend — Stitch Is the Visual Source of Truth

This is a critical RUNIX requirement.

The approved Stitch project defines the intended frontend appearance.

Project:

RUNIX Cloud Development Platform UI

Project ID:

2390441801388154937

The frontend agent must inspect and use the Stitch project before implementing major frontend screens.

19. Stitch Screens

Approved screens include:

Profile / Avatar
98d2d9499d9143c8b95657d91fb2d856
Browser Workspace
ff9274589d334fffbba97dfdec1f63e2
Interactive Workspace
7bd5aaf3cb4a4318867e64ddb7b17294
Developer Dashboard
a42d31e3c79a48a8a72729fc41fe4160
New Workspace Creation
12b851a93c9a42deb264221401ed819b
Interactive New Workspace
984a073b74c94908b31407a4d4a88df7
Create Workspace
9c89cd452097490cb97fbc6ffa35bb3f
Landing Page
9df9ed75441941a79f618295d6ca10c0
Developer Sign In
e5837e279f004f5fa918ab1812f5f056
20. Frontend Implementation Rule

When implementing a Stitch screen:

Inspect the Stitch screen.
Retrieve or inspect its generated code/assets where available.
Identify layout hierarchy.
Identify reusable components.
Identify typography.
Identify spacing.
Identify colors and surfaces.
Identify responsive behavior.
Identify animations/interactions.
Implement using the RUNIX frontend architecture.
Connect real backend data.
Compare implementation against Stitch.
Fix visual differences.
Add tests.

Do not redesign the screen while implementing it.

21. Do Not Create a Competing Design

Do NOT replace the Stitch design with:

generic Tailwind dashboard
generic admin dashboard
generic SaaS template
Bootstrap dashboard
random component library
generic AI chatbot
excessive glassmorphism
excessive neon
giant gradient hero
oversized cards
unrelated 3D decoration

The implementation should look like RUNIX.

22. Frontend Visual Language

RUNIX should preserve the established visual direction:

deep graphite / near-black base
layered dark surfaces
subtle borders
restrained indigo/blue accents
high contrast
modern sans-serif typography
monospace typography for code/runtime information
precise spacing
restrained gradients
subtle glass effects only where useful
compact professional developer tooling layout

The Stitch design overrides assumptions if there is a visual conflict.

23. Frontend Component Architecture

Prefer reusable components.

Example:

components/
├── ui/
├── layout/
├── dashboard/
├── workspace/
├── editor/
├── terminal/
├── preview/
├── git/
├── runtime/
├── tests/
├── ai/
└── command-palette/

Avoid duplicating the same UI implementation across pages.

24. Frontend State Management

Separate:

Server State

Examples:

projects
runtime status
Git status
test runs
GitHub repositories
Local UI State

Examples:

selected file
active tab
panel width
modal state
command palette state
Real-Time State

Examples:

terminal output
runtime transitions
command execution
test progress
AI execution events

Do not use one uncontrolled global state object for the entire application.

25. Monaco Editor

The editor must use Monaco.

Required behavior includes:

file tabs
syntax highlighting
line numbers
minimap where supported by Stitch
diagnostics
errors
warnings
save state
dirty state
file switching
content loading
content persistence
conflict detection

Do not implement a fake textarea as a replacement for Monaco in the real IDE.

26. Terminal

Use xterm.js.

The terminal must connect to:

/ws/projects/{project_id}/terminal

Use a real PTY inside the runtime.

Do not simulate shell output.

Terminal input must be delivered to the runtime.

Terminal output must come from the runtime.

27. Terminal Security

Initial limits:

5 connections / user
3 connections / project
64 KB maximum WebSocket message
16 KB maximum terminal input
30 minute idle timeout

Use reconnect backoff.

Do not log raw terminal output by default.

28. Runtime Lifecycle

Runtime states:

creating
starting
running
stopping
stopped
failed
terminating
terminated

Frontend status must represent actual backend/runtime state.

Never display:

Running

when the runtime is actually stopped.

Never show:

Preview Ready

without a real reachable preview.

29. Runtime Manager

The runtime manager owns container lifecycle.

It must handle:

create
start
stop
restart
terminate
inspect
health
resource limits
port discovery
cleanup
reconciliation

Docker state is not the source of truth.

PostgreSQL runtime metadata plus reconciliation determine expected state.

30. Preview

Preview URLs must be authorized.

A preview request must establish:

project
runtime
port
authorization

Do not expose arbitrary container ports publicly.

Do not create unrestricted reverse proxies.

Preview access must be scoped to the correct project/runtime.

31. Git

Git operations operate on the project workspace.

Supported operations include:

status
diff
stage
unstage
commit
push
pull
branches
checkout

Git commands involving user repositories must execute inside the controlled runtime/workspace environment.

Do not execute repository Git hooks on the API host.

32. GitHub

Production integration should use a GitHub App where practical.

Never send long-lived GitHub credentials to:

browser
project source
logs
public preview
arbitrary runtime environment

Use short-lived credentials or controlled credential injection.

33. Imported Repositories Are Untrusted

A GitHub repository can contain:

package.json
requirements.txt
Makefile
Dockerfile
scripts
git hooks
shell scripts
build scripts
postinstall scripts

Treat imported repositories as untrusted code.

Do not execute repository scripts during import on the control plane.

Dependency installation happens only inside the isolated runtime.

34. AI Coding Agent

The AI agent is a controlled coding system.

It is not a generic chatbot.

Supported tools include:

list_files
read_file
search_code
create_file
update_file
delete_file
inspect_terminal
run_tests
inspect_git

The preferred workflow is:

User request
    ↓
Repository inspection
    ↓
Plan
    ↓
Approval when required
    ↓
Patch generation
    ↓
Diff
    ↓
Approval when required
    ↓
Apply
    ↓
Tests
    ↓
Result
35. AI Approval Rules

Read-only operations can be automatic.

Potentially destructive or side-effectful operations require appropriate approval.

Examples:

deleting files
changing dependencies
modifying security configuration
changing infrastructure
executing risky commands
Git commit
Git push
deployment

Never allow the AI agent unrestricted host shell access.

Never give the AI agent direct host filesystem access.

36. AI UI

The AI panel should communicate:

current task
repository context
selected files
plan
tool activity
changes
diff
test results
approval state

Do not expose hidden chain-of-thought.

Show concise user-facing summaries rather than private reasoning.

37. Project Templates

Initial templates:

react-vite-ts
node-typescript
python-fastapi
mern
blank-docker

Template versions are immutable.

Example:

react-vite-ts@1.0.0

Do not silently change the contents of a published template version.

38. Template Frontend

The template picker MUST use the approved Stitch workspace creation UI.

Template information should come from:

GET /api/v1/templates

Do not maintain a second incompatible hardcoded template registry in the frontend.

39. Error Handling

Use:

18-ERROR-HANDLING.md

All errors should be:

classified
structured
traceable
user-safe
appropriately logged
tested

Do not expose raw Python tracebacks or infrastructure secrets to users.

40. Standard API Error Envelope

Follow the documented error format.

Include appropriate:

error code
message
request ID
trace ID where appropriate
details where safe

Do not invent unrelated error formats for individual endpoints.

41. No Silent Failure

If an operation fails:

show an appropriate error
preserve useful state
provide retry when safe
log diagnostic context
avoid falsely reporting success

Never silently swallow exceptions.

Avoid patterns such as:

try:
    ...
except Exception:
    pass

unless the exception is intentionally handled and documented.

42. No Silent Data Loss

File writes, Git operations, workspace changes, runtime termination, and project deletion must protect against accidental data loss.

For potentially destructive actions:

detect conflicts
warn the user
require confirmation where appropriate
preserve recoverable state where possible
43. Concurrency

File editing must support optimistic concurrency.

Use content hashes.

Example:

base_hash

If the server detects that the file changed since the client loaded it:

409 FILE_CHANGED

Do not silently overwrite another change.

44. Testing Requirements

Every meaningful implementation must include tests.

Use:

Vitest
React Testing Library
Playwright
pytest
pytest-asyncio
httpx
Testcontainers
Ruff
mypy
45. Minimum Testing Expectations

For backend features:

unit test
integration test where appropriate
authorization test
error test

For frontend features:

component test
interaction test
responsive test where relevant

For critical user journeys:

Playwright E2E

For runtime functionality:

runtime isolation test
resource limit test
lifecycle test
cleanup test
46. Critical E2E Flow

The application must eventually support this complete flow:

Register / Sign In
       ↓
Dashboard
       ↓
Create Project
       ↓
Choose Template
       ↓
Create Workspace
       ↓
Open IDE
       ↓
Start Runtime
       ↓
Open File
       ↓
Edit File
       ↓
Save
       ↓
Open Terminal
       ↓
Run Command
       ↓
Start Development Server
       ↓
Open Preview
       ↓
Run Tests
       ↓
Inspect Git Status
       ↓
Commit
       ↓
Push to GitHub

Each step must use real functionality.

47. Observability

Use:

17-OBSERVABILITY.md

At minimum provide:

structured logs
request IDs
trace IDs where supported
metrics
health endpoints
audit events
runtime lifecycle events
error tracking

Do not log secrets.

Do not capture source code or keystrokes unnecessarily.

48. Health Endpoints

The backend must provide:

GET /health
GET /health/ready

Health checks must reflect meaningful application state.

Readiness should verify required dependencies according to deployment requirements.

49. Performance

Initial targets:

Health endpoint: < 200ms
Simple authenticated API: < 500ms
Project list: < 500ms
File metadata: < 500ms
WebSocket connection: < 2s
Runtime start: < 30s
Preview readiness: < 45s

These are engineering targets, not permission to compromise correctness or security.

50. Responsive Design

Follow the Stitch responsive behavior.

Expected hierarchy:

Desktop

Full IDE experience.

Laptop

Reduced/collapsible secondary panels.

Tablet

Collapse non-critical panels.

Mobile

Project management and monitoring remain usable.

A full desktop IDE does not need to be forced into an unusable mobile layout.

51. Accessibility

Frontend implementations must support:

keyboard navigation
visible focus
semantic HTML
sufficient contrast
accessible labels
meaningful status messages
reduced-motion support where appropriate

Do not rely exclusively on color to communicate state.

52. Animation

Animations must support the Stitch design.

Avoid:

unnecessary motion
excessive particle effects
distracting transitions
animation everywhere

Respect reduced-motion preferences.

53. Command Palette

The command palette uses:

Ctrl/Cmd + K

Commands may include:

Create project
Open project
Start runtime
Stop runtime
Restart runtime
Run tests
Open terminal
Open preview
Toggle AI
Import GitHub repository
Commit
Push
Pull
Deploy
Open settings

Commands must only appear when the underlying capability exists.

Do not expose fake commands.

54. Feature Flags and Incomplete Features

If a feature is not implemented:

Prefer:

Coming soon
Disabled
Not configured
Unavailable

over fake behavior.

Example:

If AI provider configuration is missing:

AI Agent
Provider not configured
Configure an AI provider to enable coding assistance.

Do not generate fake AI responses.

55. Mocking Rules

Mocks are acceptable for:

unit tests
isolated frontend development
controlled development environments

Mocks must NOT silently become production behavior.

Production code must clearly distinguish:

real service
mock
development stub
56. Environment Configuration

Use:

.env.example

for configuration documentation.

Never commit:

.env
.env.local
production secrets
private keys
GitHub credentials
API keys
database passwords

Use environment variables and secret management.

57. Docker Compose

Local development should use Docker Compose for infrastructure such as:

PostgreSQL
Redis
RUNIX services

Do not require developers to manually reproduce the entire infrastructure stack unless necessary.

58. Local Development

A developer should eventually be able to perform:

git clone <repository>
cd RUNIX
cp .env.example .env
docker compose up

and access the local RUNIX environment according to the README.

If additional setup is required, document it explicitly.

59. Code Quality

Prefer:

small functions
clear names
typed interfaces
explicit error handling
testable services
dependency injection
separation of concerns
reusable frontend components

Avoid:

giant files
duplicated business logic
unexplained magic values
global mutable state
deeply nested conditionals
hidden side effects
60. Type Safety

Frontend:

TypeScript

Backend:

Pydantic
type hints
mypy where configured

Avoid:

any

unless there is a documented reason.

Avoid untyped dynamic payloads where a stable schema is possible.

61. Dependency Rules

Do not add a dependency simply because it makes one small component easier.

Before adding a package:

Determine whether existing dependencies solve the problem.
Check whether the package is necessary.
Consider security and maintenance.
Keep the dependency surface minimal.
Update lockfiles.
Test the build.
62. Security Review Before Merge

For changes involving:

authentication
authorization
filesystem
runtime
Docker
terminal
Git
GitHub
preview
secrets
AI tools
deployment

perform an explicit security review.

Ask:

Can the user escape their project?
Can user code reach the host?
Can another user access this resource?
Can a secret reach the browser?
Can an imported repository execute on the control plane?
Can this endpoint be abused without authorization?
Can this operation cause unintended data loss?
63. Implementation Workflow

Every implementation task should follow:

1. Read relevant documentation
2. Inspect existing repository
3. Inspect Stitch design if frontend-related
4. Identify affected components
5. Identify dependencies
6. Implement smallest correct change
7. Add/update tests
8. Run lint
9. Run type checks
10. Run relevant tests
11. Perform security review
12. Verify integration
13. Update documentation if behavior changed
14. Report what changed
64. Do Not Implement Everything at Once

RUNIX is a large system.

Do not attempt to generate the entire production platform in one uncontrolled pass.

Implement in phases.

Use:

20-ROADMAP.md

as the implementation sequence.

65. Implementation Phases
Phase 0 — Foundation

Implement:

repository structure
configuration
Docker Compose
linting
formatting
testing infrastructure
environment configuration
base frontend
base backend
Phase 1 — Control Plane

Implement:

PostgreSQL
SQLAlchemy models
Alembic
authentication
sessions
project CRUD
authorization
API foundation
error handling
Phase 2 — Frontend / Stitch Integration

Implement:

landing
sign in
registration
dashboard
create workspace
project management

All screens must follow Stitch.

Phase 3 — Workspace + Editor

Implement:

workspace service
file tree
file CRUD
file search
Monaco
tabs
save
dirty state
conflict detection
Phase 4 — Runtime Engine

Implement:

runtime manager
Docker runtime
lifecycle
resource limits
workspace mount
runtime health
reconciliation
Phase 5 — Terminal + Preview

Implement:

xterm.js
WebSocket
PTY
terminal input/output
command execution
port discovery
preview gateway
live preview
Phase 6 — Git + GitHub

Implement:

Git status
diff
stage
unstage
commit
branch
checkout
push
pull
GitHub authentication
repository listing
repository import
Phase 7 — Testing Platform

Implement:

test runner
test history
test results
output
failure diagnostics
test UI
Phase 8 — AI Coding Agent

Implement:

repository context
file tools
search
plan
diff
approval
patch application
test execution
audit trail

Only after the core workspace/runtime architecture is stable.

Phase 9 — Deployment

Implement:

deployment configuration
build process
deployment jobs
deployment status
deployment logs
deployment lifecycle
Phase 10 — Observability + Reliability

Implement:

metrics
traces
structured logs
runtime reconciliation
alerts
dashboards
failure recovery
operational tooling
Phase 11 — Collaboration

Future:

multiple users
project members
shared workspaces
real-time collaboration
presence
comments

Do not implement before core platform stability unless explicitly requested.

Phase 12 — Production Hardening

Implement:

security hardening
load testing
backup validation
disaster recovery
runtime host draining
deployment rollback
penetration testing
operational runbooks
66. Current Phase Discipline

When asked to implement a feature, determine which roadmap phase owns it.

Do not silently jump ahead into unrelated future phases.

Example:

If implementing the workspace editor, do not simultaneously implement:

billing
team collaboration
deployment marketplace
advanced AI autonomy

unless explicitly requested.

67. Frontend Task Discipline

For every frontend task:

Read:
13-FRONTEND-SPECIFICATION.md
14-DESIGN-SYSTEM.md
21-DEFINITION-OF-DONE.md

Then inspect:
Stitch project

Then:
Implement
Connect data
Test
Compare visually
Fix differences
68. Stitch Asset Handling

When Stitch provides hosted assets or generated code:

inspect the provided asset
preserve intended usage
download assets when required
keep local asset paths deterministic
optimize only where it does not change the design
do not replace a Stitch asset with an unrelated asset

When instructed by the project workflow, hosted resources may be downloaded using tools such as:

curl -L

Do not invent missing assets.

69. Visual Regression

For important frontend screens, compare implementation against the Stitch reference.

Check:

layout
alignment
spacing
typography
sizing
colors
borders
shadows
icons
interaction states
responsive behavior

If the implementation looks significantly different, treat that as an implementation defect.

70. Backend-Frontend Contract

Frontend components must use actual API contracts.

Do not duplicate backend business rules in the frontend.

Example:

Template availability comes from:

GET /api/v1/templates

rather than independently hardcoded template definitions.

71. Loading States

Every asynchronous operation should have an explicit state where appropriate:

idle
loading
success
error

Long-running operations may use:

queued
running
completed
failed
cancelled

Do not show false completion.

72. Empty States

Every major data-driven screen should handle empty state.

Examples:

No projects yet
No Git changes
No test runs
No branches
No terminal sessions
No GitHub repositories

Empty states should follow Stitch visual language.

73. Error States

Important frontend failures should be visible.

Examples:

Runtime failed
Preview unavailable
GitHub authorization failed
File save failed
File changed externally
Terminal disconnected
Test execution failed

Use the documented error system.

74. Runtime Reconciliation

The runtime manager must eventually reconcile:

expected database state
        vs
actual Docker state

Detect:

missing containers
orphaned containers
incorrect labels
stopped expected-running containers
stale runtime records

Do not blindly recreate everything.

Use controlled reconciliation.

75. Resource Cleanup

Every resource created by RUNIX must have a cleanup strategy.

Examples:

runtime
container
PTY
terminal session
temporary file
job
preview process
temporary credential

A failed operation must not leave uncontrolled infrastructure behind.

76. Job Execution

Long-running tasks should use the job system where appropriate.

Examples:

GitHub repository import
tests
builds
deployment
long-running AI operations

The API should not unnecessarily block while performing long-running work.

77. Queue Discipline

Queue jobs should be:

idempotent where possible
observable
retryable where safe
timeout-aware
failure-aware

Do not automatically retry:

validation failures
authentication failures
authorization failures
deterministic conflicts

Use exponential backoff with jitter for transient failures.

78. Git Conflict Handling

Do not silently overwrite user work.

Before pull/checkout:

detect uncommitted changes
warn when necessary
preserve work
handle conflicts explicitly

A Git conflict is not a successful operation.

79. File Save Semantics

File saves should:

Validate path.
Validate authorization.
Validate payload.
Verify base_hash when provided.
Detect conflicts.
Write atomically.
Update metadata.
Return updated hash.
Notify relevant subscribers where applicable.
80. File Metadata

Metadata may include:

path
size
content hash
modified time
type

Do not rely exclusively on cached metadata.

When filesystem state changes externally, reconcile appropriately.

81. Project Deletion

Project deletion is destructive.

Require appropriate authorization and confirmation.

Deletion must account for:

workspace
runtime
Git metadata
jobs
preview processes
project-specific resources

Do not leave uncontrolled containers behind.

82. Logging

Use structured logs.

Preferred fields:

timestamp
level
service
request_id
trace_id
user_id where appropriate
project_id where appropriate
runtime_id where appropriate
job_id where appropriate
event
duration
status

Avoid high-cardinality metric labels.

Do not log secrets.

83. Metrics

Use documented RUNIX metric names.

Examples:

runix_http_requests_total
runix_http_request_duration_seconds
runix_runtime_starts_total
runix_runtime_failures_total
runix_runtime_start_duration_seconds
runix_terminal_connections
runix_workspace_operations_total

Do not add user/project IDs as unrestricted metric labels.

84. Audit Logging

Audit important actions:

login
logout
project creation
project deletion
membership changes
runtime lifecycle
GitHub integration
Git push/pull
AI changes
deployment

Audit events must not contain secrets.

85. Documentation Updates

If implementation changes documented behavior:

Update the relevant documentation.
Keep examples accurate.
Update API schemas.
Update environment examples.
Update README where required.

Do not allow documentation to silently become incorrect.

86. README Requirements

The README should eventually explain:

what RUNIX is
architecture overview
local setup
prerequisites
environment configuration
development commands
testing
Docker Compose
frontend
backend
runtime
GitHub setup
deployment
security model
87. Code Review Checklist

Before considering a change complete:

Correctness
Does the implementation satisfy the requirement?
Does it integrate with existing architecture?
Are edge cases handled?
Security
Is authorization enforced?
Are secrets protected?
Can user input escape its boundary?
Can user code reach the host?
Reliability
Are failures handled?
Are retries appropriate?
Is cleanup guaranteed?
Testing
Are relevant tests present?
Do existing tests pass?
UX
Does the frontend match Stitch?
Are loading/error/empty states handled?
Maintainability
Is the code understandable?
Is logic duplicated?
Are abstractions appropriate?
88. Validation Commands

Use the repository's actual package-manager commands when established.

Typical frontend validation:

npm run lint
npm run typecheck
npm run test
npm run build

Typical backend validation:

ruff check .
mypy .
pytest

E2E:

npx playwright test

If the repository uses a different package manager or command, follow the repository configuration rather than blindly inventing commands.

89. Do Not Hide Test Failures

Never claim success when tests fail.

If a command produces:

FAILED
ERROR
TYPE ERROR
LINT ERROR
BUILD ERROR

report it accurately.

Do not:

delete failing tests
weaken assertions
disable type checking
skip unrelated tests without reason
suppress errors merely to obtain green output
90. Do Not Disable Security Controls to Make Tests Pass

Never solve a failing runtime/security test by weakening the actual security boundary.

For example, do not add:

--privileged

or Docker socket access just to make a runtime feature work.

Fix the architecture instead.

91. No Production Shortcuts

Do not implement:

fake database
fake terminal
fake runtime
fake GitHub
fake preview
fake test runner
fake AI
fake persistence

when the feature is presented as implemented.

If the feature is intentionally mocked for development, clearly label it as such.

92. No Generic Replacement UI

Never respond to a frontend implementation task by creating an unrelated:

DashboardLayout
Sidebar
CardGrid
StatsCards

system simply because it is easy.

Use the actual Stitch screen.

93. Preserve Existing Work

Before modifying an existing implementation:

Inspect it.
Understand what it does.
Identify dependencies.
Make the smallest safe change.

Do not overwrite large portions of working code unnecessarily.

94. Avoid Unnecessary Refactors

Do not combine:

feature implementation
+
large architectural refactor
+
dependency migration
+
formatting rewrite

unless explicitly requested.

Keep changes focused.

95. Security-Critical Principle

Treat every user-controlled value as untrusted.

Examples:

file path
file contents
project name
Git URL
repository contents
terminal input
command arguments
environment variables
preview port
template parameters
AI instructions
Git branch name
commit message

Validate and constrain appropriately.

96. User Command Execution

A command submitted by the user follows:

Browser
   ↓
Authenticated WebSocket/API
   ↓
Project authorization
   ↓
Runtime authorization
   ↓
Runtime Manager
   ↓
Isolated container
   ↓
PTY/process

Never:

Browser
   ↓
os.system(...)

Never:

Browser
   ↓
subprocess.run(user_input)

on the control-plane host.

97. AI Command Execution

AI-generated commands use the same runtime security boundary as human commands.

The AI does not receive a special privileged execution path.

Correct:

AI
 ↓
RUNIX tool layer
 ↓
runtime command service
 ↓
isolated runtime

Incorrect:

AI
 ↓
host shell
98. Frontend Secrets

The browser is an untrusted environment.

Never put:

database credentials
Docker credentials
GitHub private keys
server API secrets
AI provider secrets
internal service credentials

in client-side bundles.

99. External Integrations

Every external integration must have:

timeout
error handling
retry policy where appropriate
credential protection
auditability
graceful degradation

External services must not become hidden single points of failure.

100. Graceful Degradation

If a non-core dependency is unavailable:

show the affected capability as unavailable
preserve unrelated functionality
provide actionable information

Example:

If GitHub is unavailable:

Local editing and runtime remain available.
GitHub synchronization is temporarily unavailable.

Do not make the entire application appear broken if only one integration failed.

101. Production Readiness

Before calling RUNIX production-ready, verify:

Authentication
Authorization
Persistence
Workspace security
Runtime isolation
Terminal
Preview
Git
GitHub
Tests
Error handling
Observability
Backups
Rollback
Security controls
E2E flows
Performance
Accessibility
CI/CD

Use:

21-DEFINITION-OF-DONE.md

as the final acceptance authority.

102. Definition of Done

A feature is not done merely because:

the code compiles

or:

the page renders

A feature is done when:

Implementation
+
Integration
+
Error handling
+
Security
+
Tests
+
Observability where relevant
+
Documentation
+
Visual validation where relevant

are complete.

103. Final RUNIX Acceptance

RUNIX should eventually allow a real developer to:

Sign in
   ↓
Create/import project
   ↓
Choose template
   ↓
Create workspace
   ↓
Open cloud IDE
   ↓
Edit code
   ↓
Save code
   ↓
Start isolated runtime
   ↓
Open terminal
   ↓
Execute code
   ↓
Run development server
   ↓
Open live preview
   ↓
Run tests
   ↓
Inspect Git
   ↓
Commit
   ↓
Push to GitHub
   ↓
Deploy

while maintaining:

security
isolation
persistence
authorization
observability
reliability
responsive UX
accessibility
104. Absolute Non-Negotiable Rules

The following rules must never be violated for convenience.

Rule 1

Never execute user code on the API host.

Rule 2

Never expose the Docker socket to user runtimes.

Rule 3

Never use privileged user containers.

Rule 4

Never bypass authentication or authorization.

Rule 5

Never allow workspace path traversal.

Rule 6

Never expose secrets to the browser unnecessarily.

Rule 7

Never treat imported repositories as trusted.

Rule 8

Never fake functionality that is presented as implemented.

Rule 9

Never silently overwrite user changes.

Rule 10

Never silently swallow important failures.

Rule 11

Never replace the approved Stitch UI with a generic design.

Rule 12

Never weaken security to make a feature easier.

Rule 13

Never claim tests pass when they do not.

Rule 14

Never implement unrelated future phases without instruction.

Rule 15

Never make production behavior depend on an undocumented assumption.

105. Final Agent Instruction

When working on RUNIX:

Read the specification.
Inspect the existing implementation.
Inspect Stitch for frontend work.
Understand the architecture.
Implement the smallest correct change.
Keep security boundaries intact.
Connect real functionality.
Add tests.
Validate the implementation.
Compare frontend work against Stitch.
Update documentation when necessary.
Report actual results.

The objective is not to generate the largest amount of code.

The objective is to build RUNIX as a coherent, secure, real cloud development platform.

Build. Run. Ship. Anywhere.