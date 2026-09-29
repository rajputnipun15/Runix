RUNIX — Product & Engineering Roadmap

Document: 20-ROADMAP.md
Product: RUNIX
Tagline: Build. Run. Ship. Anywhere.
Status: Implementation Roadmap
Version: 1.0
Audience: Product, Engineering, QA, DevOps, AI Coding Agent
Primary Visual Source: Approved RUNIX Stitch Project

1. Purpose

This document defines the implementation roadmap for RUNIX.

RUNIX is a browser-based cloud development platform where developers can:

create projects
import repositories
edit source code
use a browser terminal
execute code inside isolated cloud runtimes
view live previews
run tests
use Git/GitHub
use an AI coding agent
eventually deploy applications

The roadmap converts the RUNIX specifications into an ordered implementation sequence.

The implementation must follow dependencies.

Do not attempt to implement advanced features before the underlying infrastructure is stable.

2. Product Vision

RUNIX should provide a complete browser-based development environment:

Create
   ↓
Code
   ↓
Run
   ↓
Test
   ↓
Preview
   ↓
Commit
   ↓
Push
   ↓
AI-assisted development
   ↓
Deploy

The browser is the development interface.

The cloud runtime is the execution environment.

The control plane coordinates the system.

3. Core Architecture

RUNIX is divided into:

Frontend
Backend / Control Plane
Worker System
Runtime Engine
Workspace Storage
PostgreSQL
Redis
Git/GitHub Integration
Preview Gateway
AI Agent
Observability
Deployment Infrastructure

The implementation roadmap must preserve these boundaries.

4. Roadmap Principles
4.1 Build foundations first

The following must exist before advanced functionality:

authentication
database
project model
workspace
API
frontend shell
runtime manager
4.2 Build vertical slices

Where possible, complete an end-to-end slice instead of building isolated infrastructure indefinitely.

Example:

Create project
→ create workspace
→ start runtime
→ open terminal
→ execute command

is more valuable than implementing five disconnected subsystems.

4.3 Real functionality over mock interfaces

Do not create fake functionality merely to make the UI look complete.

Bad:

Run
→ animation
→ "Running"

without a runtime.

Correct:

Run
→ backend request
→ runtime manager
→ Docker runtime
→ actual process
→ actual status
5. Implementation Phases

RUNIX should be implemented in the following phases:

Phase 0  Foundation
Phase 1  Control Plane
Phase 2  Frontend / Stitch Integration
Phase 3  Workspace + Editor
Phase 4  Runtime Engine
Phase 5  Terminal + Preview
Phase 6  Git + GitHub
Phase 7  Testing Platform
Phase 8  AI Coding Agent
Phase 9  Deployment
Phase 10 Observability + Reliability
Phase 11 Collaboration
Phase 12 Production Hardening
6. Phase 0 — Foundation
Objective

Create the repository, development environment, documentation, coding standards, and CI foundation.

6.1 Deliverables

Create:

RUNIX/
├── docs/
├── frontend/
├── backend/
├── worker/
├── runtime/
├── infrastructure/
├── scripts/
├── tests/
├── docker-compose.yml
├── .env.example
├── README.md
└── AGENTS.md
6.2 Documentation

The following documents define the implementation:

00-PROJECT-OVERVIEW.md
01-PRD.md
02-FUNCTIONAL-REQUIREMENTS.md
03-SYSTEM-ARCHITECTURE.md
04-TECHNICAL-STACK.md
05-DATABASE-SCHEMA.md
06-API-SPECIFICATION.md
07-WEBSOCKET-SPECIFICATION.md
08-RUNTIME-ENGINE.md
09-WORKSPACE-FILESYSTEM.md
10-GITHUB-INTEGRATION.md
11-AI-AGENT-SPECIFICATION.md
12-SECURITY-ARCHITECTURE.md
13-FRONTEND-SPECIFICATION.md
14-DESIGN-SYSTEM.md
15-PROJECT-TEMPLATES.md
16-TESTING-STRATEGY.md
17-OBSERVABILITY.md
18-ERROR-HANDLING.md
19-DEPLOYMENT.md
20-ROADMAP.md
21-DEFINITION-OF-DONE.md
7. Phase 0 — Repository Setup

Implement:

Git repository
directory structure
.gitignore
.env.example
README
AGENTS.md
Docker Compose
CI configuration
development scripts
8. Phase 0 — Development Standards

Configure:

Frontend
TypeScript
ESLint
Prettier
Vitest
Playwright
Backend
Python 3.11+
Ruff
mypy
pytest
pytest-asyncio
Infrastructure
Docker
Docker Compose
9. Phase 0 — Success Criteria

Phase 0 is complete when:

repository structure exists
frontend starts
backend starts
PostgreSQL starts
Redis starts
tests execute
lint executes
type checking executes
Docker Compose starts successfully
CI executes successfully
documentation is present
10. Phase 1 — Control Plane
Objective

Implement the RUNIX backend foundation.

11. Phase 1 — Backend Foundation

Implement:

FastAPI
configuration
logging
request IDs
error handling
database connection
SQLAlchemy
Alembic
Pydantic models
authentication foundation
12. Phase 1 — Database

Create migrations and models for:

User
Session
Project
ProjectMember
Workspace
Runtime
ProjectFileMetadata
TerminalSession
CommandExecution
GitRepository
GitBranch
Job
TestRun
Deployment
AuditLog
13. Phase 1 — Authentication

Implement:

POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
POST /api/v1/auth/forgot-password
POST /api/v1/auth/reset-password
GET  /api/v1/auth/me

Requirements:

secure password hashing
session management
authentication middleware
session expiration
logout
authorization foundation
rate limiting
audit events
14. Phase 1 — Project Management

Implement:

GET    /api/v1/projects
POST   /api/v1/projects
GET    /api/v1/projects/{project_id}
PATCH  /api/v1/projects/{project_id}
DELETE /api/v1/projects/{project_id}

Project creation must support:

name
template
template_version
description
visibility
15. Phase 1 — Project Authorization

Every project endpoint must verify:

authenticated user
        ↓
project exists
        ↓
membership/ownership
        ↓
permission

No frontend-only authorization.

16. Phase 1 — Template Registry

Implement:

GET /api/v1/templates
GET /api/v1/templates/{template_id}

Initial templates:

react-vite-ts
node-typescript
python-fastapi
mern
blank-docker

Template versions must be immutable.

17. Phase 1 — Workspace Service

Implement:

workspace creation
workspace lookup
workspace deletion
file tree
file metadata
file read
file write
file delete
directory creation
rename
search
quota enforcement
hashing
path validation

Workspace storage must remain separate from PostgreSQL.

18. Phase 1 — Error Handling

Implement the rules in:

18-ERROR-HANDLING.md

Required:

domain exceptions
error codes
API error envelope
request IDs
centralized exception handling
validation errors
safe production errors
19. Phase 1 — Control Plane Success Criteria

Phase 1 is complete when:

Register
   ↓
Login
   ↓
Create project
   ↓
Create workspace
   ↓
Read files
   ↓
Write files
   ↓
Delete files
   ↓
Delete project

works through real APIs and PostgreSQL.

20. Phase 2 — Frontend / Stitch Integration
Objective

Implement the actual RUNIX frontend using the approved Stitch project as the visual source of truth.

21. Stitch Source of Truth

The existing Stitch project is authoritative for:

layout
hierarchy
spacing
typography
component appearance
navigation
responsive behavior
interactions
visual language

Do not redesign the interface independently.

Stitch project:

Project:
RUNIX Cloud Development Platform UI

Project ID:
2390441801388154937
22. Stitch Screens

The frontend implementation must account for these approved screens:

98d2d9499d9143c8b95657d91fb2d856
Developer Avatar

ff9274589d334fffbba97dfdec1f63e2
RUNIX Cloud IDE - Browser Workspace

7bd5aaf3cb4a4318867e64ddb7b17294
RUNIX Cloud IDE - Interactive Animated Workspace

a42d31e3c79a48a8a72729fc41fe4160
RUNIX Developer Dashboard

12b851a93c9a42deb264221401ed819b
RUNIX New Workspace Creation

984a073b74c94908b31407a4d4a88df7
RUNIX New Workspace Creation - Interactive

9c89cd452097490cb97fbc6ffa35bb3f
RUNIX Create Workspace

9df9ed75441941a79f618295d6ca10c0
RUNIX Cloud Platform Landing

e5837e279f004f5fa918ab1812f5f056
RUNIX Developer Sign In
23. Phase 2 — Frontend Architecture

Implement:

frontend/
├── app/
├── components/
├── features/
├── hooks/
├── lib/
├── services/
├── stores/
├── types/
├── styles/
└── tests/

Recommended architecture:

app
 ↓
feature pages
 ↓
reusable RUNIX components
 ↓
API/services
 ↓
backend
24. Phase 2 — Public Pages

Implement:

/
 /login
 /register

Landing page should match the Stitch screen.

Authentication pages should match Stitch.

25. Phase 2 — Dashboard

Implement:

/dashboard

Features:

projects
project cards
recent work
create project
import GitHub repository
runtime/project status
user menu

Do not create a generic SaaS dashboard.

26. Phase 2 — Create Workspace

Implement the Stitch workspace creation flow.

Features:

template selection
project name
description
visibility
GitHub import where available
create action
validation
loading
failure
success

Template data comes from:

GET /api/v1/templates

Do not duplicate template definitions manually in the frontend.

27. Phase 2 — Frontend Success Criteria

Phase 2 is complete when:

Landing
 ↓
Login
 ↓
Dashboard
 ↓
Create Project
 ↓
Project Created

works through real backend APIs.

28. Phase 3 — Workspace + Editor
Objective

Turn the workspace into a real cloud IDE.

29. Phase 3 — IDE Shell

Implement the Stitch-approved IDE layout:

┌───────────────────────────────────────────────┐
│ RUNIX / Project / Branch / Runtime / Actions │
├────────────┬─────────────────────┬────────────┤
│ Explorer   │ Monaco Editor       │ AI Agent   │
│ Search     │                     │            │
│ Source     │                     │            │
│ Control    │                     │            │
├────────────┴─────────────────────┴────────────┤
│ Terminal / Problems / Output / Tests / Preview│
└───────────────────────────────────────────────┘

Actual dimensions and visual treatment come from Stitch.

30. Phase 3 — Monaco

Implement:

Monaco editor
syntax highlighting
tabs
line numbers
minimap
breadcrumbs
diagnostics
dirty state
save
keyboard shortcuts
31. Phase 3 — File Explorer

Implement:

directories
files
expand/collapse
create file
create folder
rename
delete
search
refresh

All operations use the workspace API.

32. Phase 3 — File Persistence

Implement:

editor
 ↓
content hash
 ↓
PUT file
 ↓
workspace service
 ↓
persistent storage

Handle:

FILE_CHANGED
FILE_TOO_LARGE
WORKSPACE_QUOTA_EXCEEDED
PATH_TRAVERSAL
33. Phase 3 — Unsaved Changes

The editor must show:

saved
saving
unsaved
save failed
conflict

Never report successful save without backend confirmation.

34. Phase 3 — Command Palette

Implement:

Ctrl/Cmd + K

Commands:

Create project
Open project
Start runtime
Stop runtime
Restart runtime
Run tests
Open terminal
Open preview
Toggle AI
Import GitHub
Commit
Push
Pull
Deploy
Settings

Unavailable features must be truthful.

35. Phase 3 — Workspace Success Criteria

Phase 3 is complete when:

Open project
 ↓
Load file tree
 ↓
Open file
 ↓
Edit file
 ↓
Save file
 ↓
Refresh
 ↓
Changes remain persisted
36. Phase 4 — Runtime Engine
Objective

Execute user code safely.

37. Phase 4 — Runtime Manager

Implement:

create runtime
start runtime
stop runtime
restart runtime
terminate runtime
inspect runtime
reconcile runtime
cleanup runtime
38. Phase 4 — Runtime State Machine

Implement:

creating
starting
running
stopping
stopped
failed
terminating
terminated

Persist state in PostgreSQL.

39. Phase 4 — Docker Isolation

Every user runtime must enforce:

CPU limit
memory limit
PID limit
storage quota
network isolation
non-root user
no privileged mode
no Docker socket
no arbitrary host mounts
40. Phase 4 — Runtime Templates

Implement runtime support for:

Node.js
Python
MERN
Blank

Use approved images only.

41. Phase 4 — Runtime Success Criteria

Phase 4 is complete when:

Project
 ↓
Start runtime
 ↓
Docker container created
 ↓
Workspace mounted
 ↓
Runtime running
 ↓
Runtime status persisted
 ↓
Stop runtime
 ↓
Container removed safely

works reliably.

42. Phase 5 — Terminal + Preview
Objective

Connect developers to the running runtime.

43. Phase 5 — Terminal

Implement:

xterm.js
WebSocket
PTY
input
output
resize
ping/pong
disconnect
reconnect
44. Phase 5 — Terminal Flow
Browser
 ↓
WebSocket
 ↓
Terminal Service
 ↓
Runtime Manager
 ↓
PTY
 ↓
Container
45. Phase 5 — Terminal Security

Enforce:

authentication
project authorization
connection limits
message size limits
idle timeout
runtime validation
46. Phase 5 — Terminal Success Criteria

Developer can:

open terminal
run pwd
run ls
create a file
run npm/python command
see output
resize terminal
close terminal
reconnect

All commands execute inside the runtime.

47. Phase 5 — Preview

Implement:

port discovery
preview gateway
preview authorization
preview URL
runtime-to-preview routing

Initial ports:

3000
4173
5173
8000
8080
48. Phase 5 — Preview Flow
User application
 ↓
Runtime port
 ↓
Port detection
 ↓
Preview Gateway
 ↓
Authorization
 ↓
Browser Preview
49. Phase 5 — Preview Success Criteria

For React:

Create React project
 ↓
Start runtime
 ↓
npm install
 ↓
npm run dev -- --host 0.0.0.0
 ↓
detect 5173
 ↓
preview available

For FastAPI:

uvicorn
 ↓
detect 8000
 ↓
preview available
50. Phase 6 — Git + GitHub
Objective

Give developers a real Git workflow.

51. Phase 6 — Local Git

Implement:

status
diff
stage
unstage
commit
push
pull
branches
checkout

Git commands execute inside the runtime/workspace boundary.

52. Phase 6 — Git UI

Implement:

Source Control panel
changed files
staged files
unstaged files
diff viewer
commit message
branch selector
push
pull
conflict state

Visual design must follow Stitch.

53. Phase 6 — GitHub Authentication

Production:

GitHub App

Development may support OAuth where necessary.

54. Phase 6 — GitHub Repository Import

Flow:

GitHub
 ↓
Repository selection
 ↓
Project creation
 ↓
Workspace
 ↓
Clone
 ↓
Checkout
 ↓
Index
 ↓
Runtime

Import must be asynchronous.

55. Phase 6 — GitHub Success Criteria

Developer can:

connect GitHub
 ↓
view repositories
 ↓
import repository
 ↓
open workspace
 ↓
edit
 ↓
commit
 ↓
push
56. Phase 7 — Testing Platform
Objective

Make tests a first-class RUNIX feature.

57. Phase 7 — Test Runner

Implement:

POST /projects/{project_id}/tests/run
GET /projects/{project_id}/tests
GET /projects/{project_id}/tests/{test_run_id}
58. Phase 7 — Test Execution

Tests execute inside the runtime.

Never execute project test commands on the API host.

59. Phase 7 — Test UI

Implement:

Tests panel
run button
running state
passed state
failed state
test counts
duration
output
exit code
60. Phase 7 — Test States
queued
running
passed
failed
timed_out
cancelled
error
61. Phase 7 — Testing Success Criteria

Developer can:

open project
 ↓
run tests
 ↓
see live state
 ↓
see results
 ↓
inspect output
 ↓
rerun
62. Phase 8 — AI Coding Agent
Objective

Add a controlled repository-aware AI development agent.

AI is a V2 feature.

It must not compromise the runtime/security architecture.

63. Phase 8 — AI Architecture
User Request
    ↓
AI Agent
    ↓
Repository Context
    ↓
Plan
    ↓
Approval
    ↓
Patch
    ↓
Validation
    ↓
Apply
    ↓
Tests
    ↓
Result
64. Phase 8 — AI Tools

Implement:

list_files
read_file
search_code
create_file
update_file
delete_file
inspect_terminal
run_tests
inspect_git
65. Phase 8 — AI UI

The AI panel must look like a coding agent.

It should show:

repository context
selected files
task
plan
tool activity
diff
test results
approval state

Do not create a generic chatbot.

66. Phase 8 — AI Approval

Approval required for:

destructive changes
dependency changes
security/config changes
side-effectful commands
Git commit
Git push
deployment
67. Phase 8 — AI Success Criteria

Developer can:

Ask AI to implement a feature
 ↓
AI inspects repository
 ↓
AI generates plan
 ↓
User reviews
 ↓
AI generates patch
 ↓
User approves
 ↓
Patch applied
 ↓
Tests run
 ↓
Results shown
68. Phase 9 — Deployment
Objective

Allow users to deploy projects.

Deployment is a later milestone and must not compromise the core IDE.

69. Phase 9 — Deployment Architecture

Implement a deployment abstraction:

Project
 ↓
Build
 ↓
Artifact
 ↓
Deployment
 ↓
Platform
 ↓
URL
70. Phase 9 — Deployment Model

Initial implementation may integrate with one controlled deployment target.

Do not build a large multi-cloud deployment system in V1.

71. Phase 9 — Deployment UI

Add:

Deploy
Deployments
Deployment status
Build logs
Deployment logs
URL
Rollback
72. Phase 9 — Deployment States
queued
building
deploying
running
failed
cancelled
rolled_back
73. Phase 9 — Deployment Success Criteria

Developer can:

project
 ↓
deploy
 ↓
build
 ↓
deployment
 ↓
public URL
 ↓
inspect logs
 ↓
rollback
74. Phase 10 — Observability + Reliability
Objective

Make RUNIX operationally reliable.

75. Phase 10 — Logging

Implement structured JSON logging.

Every important operation should include:

request_id
trace_id
service
operation
timestamp
status
76. Phase 10 — Metrics

Implement:

API latency
API errors
runtime starts
runtime failures
terminal connections
workspace operations
jobs
tests
preview
GitHub
AI
database
Redis
77. Phase 10 — Tracing

Implement OpenTelemetry where practical.

Trace:

project creation
workspace creation
runtime start
command execution
GitHub import
Git push/pull
tests
AI tasks
preview
deployment
78. Phase 10 — Alerts

Initial alerts:

high API error rate
high runtime failure rate
database unavailable
Redis unavailable
disk nearly full
runtime capacity exhausted
worker queue backlog
preview failure rate
GitHub integration failures
79. Phase 10 — Reliability

Implement:

retries
backoff
job retry
dead-letter handling
runtime reconciliation
orphan cleanup
health checks
graceful shutdown
capacity monitoring
80. Phase 11 — Collaboration
Objective

Add multi-user development capabilities after the core single-user workflow is stable.

81. Phase 11 — Project Members

Implement:

invite member
remove member
role
permissions

Roles may include:

owner
admin
developer
viewer
82. Phase 11 — Collaboration

Potential future features:

presence
shared editor
comments
activity feed
real-time collaboration
shared terminal

These are not prerequisites for the first functional RUNIX release.

83. Phase 12 — Production Hardening
Objective

Prepare RUNIX for real users and sustained workloads.

84. Phase 12 — Security Hardening

Review:

authentication
authorization
CSRF
XSS
SSRF
path traversal
container escape
Docker permissions
preview isolation
GitHub credentials
AI tools
rate limits
secrets
audit logging
85. Phase 12 — Performance

Measure:

API latency
workspace operations
file loading
editor startup
runtime startup
terminal latency
preview startup
Git operations
test execution
AI response latency
86. Initial Performance Targets

Target values from the testing specification:

Operation	Target
Health	<200 ms
Simple auth API	<500 ms
Project list	<500 ms
File metadata	<500 ms
WebSocket connection	<2 s
Runtime start	<30 s
Preview readiness	<45 s

These are initial engineering targets rather than guarantees.

87. Phase Dependencies

The phases depend on each other:

Phase 0
   ↓
Phase 1
   ↓
Phase 2
   ↓
Phase 3
   ↓
Phase 4
   ↓
Phase 5
   ↓
Phase 6
   ↓
Phase 7
   ↓
Phase 8
   ↓
Phase 9
   ↓
Phase 10
   ↓
Phase 11
   ↓
Phase 12

Some Phase 10 work begins earlier.

Some infrastructure work can happen in parallel.

88. Parallel Workstreams

The following can progress in parallel after Phase 0:

Backend
Frontend
Runtime
Infrastructure
Testing
Documentation

But integration must follow dependency boundaries.

89. Recommended Team Workstreams

If multiple developers are available:

Track A — Backend
auth
projects
workspace
Git
GitHub
jobs
AI APIs
Track B — Frontend
Stitch implementation
dashboard
workspace
editor
terminal
preview
Git
AI
Track C — Runtime
Docker
runtime manager
PTY
resource limits
port detection
reconciliation
Track D — Platform
PostgreSQL
Redis
CI/CD
deployment
observability
security
90. Solo Developer Strategy

If RUNIX is implemented by one developer, use this order:

1. Backend foundation
2. Authentication
3. Project CRUD
4. Workspace
5. Stitch frontend
6. Monaco
7. Runtime
8. Terminal
9. Preview
10. Git
11. GitHub
12. Tests
13. Observability
14. AI
15. Deployment
16. Hardening

Do not start AI before the core IDE works.

91. MVP Definition

The RUNIX MVP is:

Authentication
+
Dashboard
+
Project creation
+
Templates
+
Workspace filesystem
+
Monaco editor
+
Docker runtime
+
Terminal
+
Live preview
+
Tests
+
Git
+
Basic GitHub integration
92. MVP Exclusions

The MVP does not require:

advanced collaboration
billing
marketplace
multi-cloud deployment
advanced AI autonomy
enterprise SSO
advanced analytics
complex team administration
multi-region runtime scheduling
93. MVP End-to-End Flow

The primary MVP flow is:

Landing
 ↓
Sign in
 ↓
Dashboard
 ↓
Create project
 ↓
Select template
 ↓
Create workspace
 ↓
Start runtime
 ↓
Open IDE
 ↓
Edit source
 ↓
Save
 ↓
Open terminal
 ↓
Run command
 ↓
Start development server
 ↓
Preview application
 ↓
Run tests
 ↓
Git status
 ↓
Commit
 ↓
Push

This flow should work before calling the MVP complete.

94. V1 Release

V1 should add:

strong error handling
observability
GitHub integration
template versioning
runtime reconciliation
security hardening
deployment foundation
production CI/CD
95. V2 Release

V2 can add:

AI coding agent
deployment workflows
collaboration
advanced GitHub features
improved runtime scheduling
team features
96. V3 / Scale

Future scale features may include:

multi-region runtimes
Kubernetes-based runtime scheduling
persistent volumes at scale
autoscaling
enterprise identity
organization management
billing
usage metering
advanced collaboration
marketplace
deployment providers
97. Feature Priority

Use these priorities:

P0 — Required
authentication
projects
workspace
editor
runtime
terminal
preview
tests
Git
security
P1 — Important
GitHub
observability
runtime reconciliation
deployment
AI agent
P2 — Expansion
collaboration
teams
billing
advanced deployment
multi-region
98. Technical Debt Policy

Do not accumulate intentional technical debt around:

security
authentication
authorization
runtime isolation
workspace integrity
data persistence

Temporary shortcuts may be acceptable for:

visual polish
non-critical optimization
advanced deployment abstraction
secondary integrations

provided they are documented.

99. Architecture Change Policy

Before changing architecture:

Identify affected documents.
Identify API impact.
Identify database impact.
Identify runtime impact.
Identify security implications.
Update relevant specification.
Update implementation.
Update tests.

Do not silently diverge from the specifications.

100. Stitch Change Policy

If the Stitch design changes:

Stitch
 ↓
Frontend specification
 ↓
Design system
 ↓
Frontend implementation
 ↓
Visual regression

The frontend must follow the updated approved Stitch design.

Do not preserve an obsolete implementation merely because it was coded first.

101. Implementation Order Within a Feature

For every feature:

1. Read relevant specification
2. Inspect existing implementation
3. Identify dependencies
4. Define data/API changes
5. Implement backend
6. Implement frontend
7. Integrate
8. Add error handling
9. Add observability
10. Add tests
11. Validate security
12. Run build
13. Run E2E where applicable
14. Update documentation
102. Antigravity Implementation Rule

When implementing RUNIX, Antigravity must not blindly generate the entire application in one operation.

It should implement in controlled phases.

For each phase:

specification
 ↓
implementation
 ↓
validation
 ↓
fix
 ↓
tests
 ↓
next phase
103. Antigravity Frontend Rule

For every frontend task:

1. Inspect Stitch project.
2. Identify matching screen.
3. Retrieve/inspect Stitch-generated assets/code where available.
4. Reuse the visual structure.
5. Implement using RUNIX's approved frontend architecture.
6. Connect real APIs.
7. Preserve responsive behavior.
8. Validate against Stitch.

Do not create an unrelated UI.

104. Antigravity Backend Rule

For backend tasks:

API route
 ↓
service
 ↓
domain
 ↓
repository/infrastructure
 ↓
database/runtime/external system

Do not put business logic directly into route handlers.

105. Antigravity Runtime Rule

For runtime features:

API
 ↓
Runtime service
 ↓
Runtime Manager
 ↓
Docker
 ↓
User Runtime

Never:

API
 ↓
subprocess(user_command)
106. Antigravity Security Rule

Before considering runtime functionality complete, verify:

no privileged container
no Docker socket
no host root mount
no arbitrary host path
no host command execution
no unrestricted image selection
no missing authorization
no exposed secrets
107. Definition of Phase Completion

A phase is not complete merely because the code exists.

A phase is complete when:

implementation
+
integration
+
tests
+
error handling
+
security validation
+
observability
+
documentation

are complete for that phase.

108. Release Gates

Before every release:

Functional

Required features work.

Primary user flow works.

Error states work.

Recovery actions work.

Security

Authorization tested.

Runtime isolation tested.

Secrets reviewed.

Input validation tested.

Path traversal tested.

Quality

Lint passes.

Typecheck passes.

Unit tests pass.

Integration tests pass.

E2E passes.

Build succeeds.

Operations

Logs available.

Metrics available.

Health checks pass.

Alerts configured.

Rollback path verified.

Frontend

Stitch visual alignment checked.

Responsive behavior checked.

Accessibility checked.

Loading states checked.

Error states checked.

109. Critical Path

The most important technical critical path is:

PostgreSQL
   ↓
Authentication
   ↓
Projects
   ↓
Workspace
   ↓
Frontend IDE
   ↓
Runtime Manager
   ↓
Docker Runtime
   ↓
WebSocket Terminal
   ↓
Port Detection
   ↓
Preview

If this path works reliably, RUNIX has its core identity.

110. Product Critical Path

The most important user journey is:

Sign In
   ↓
Create Project
   ↓
Choose Template
   ↓
Open Workspace
   ↓
Start Runtime
   ↓
Edit Code
   ↓
Run Code
   ↓
Preview
   ↓
Test
   ↓
Git Commit
   ↓
GitHub Push

Every major implementation decision should preserve this flow.

111. Risk Register
Risk 1 — Runtime Security

Risk: User code escapes the runtime.

Mitigation:

container isolation
no privileged mode
resource limits
network restrictions
no Docker socket
security tests
host isolation
Risk 2 — Workspace Data Loss

Risk: User code is lost.

Mitigation:

persistent storage
atomic writes
Git integration
backups
restore testing
quotas
Risk 3 — Runtime Scalability

Risk: Too many concurrent runtimes overwhelm infrastructure.

Mitigation:

resource limits
capacity monitoring
runtime scheduling
idle shutdown
future horizontal scaling
Risk 4 — GitHub Integration Failure

Risk: GitHub outages affect development.

Mitigation:

local Git remains functional
provider error isolation
bounded retries
clear UI states
Risk 5 — AI Misbehavior

Risk: AI makes unsafe or destructive changes.

Mitigation:

tool allowlist
runtime execution
diff-first workflow
approval gates
audit events
patch conflict detection
Risk 6 — Frontend Drift From Stitch

Risk: Implementation gradually becomes a different product.

Mitigation:

Stitch remains visual source of truth
visual regression
design-system rules
explicit review
112. Success Metrics

Engineering metrics:

runtime start success rate
runtime startup latency
preview startup latency
API error rate
workspace save success rate
terminal connection success rate
Git operation success rate
GitHub import success rate
test execution success rate
deployment success rate

Product metrics may later include:

project creation completion
active workspaces
runtime sessions
projects per user
GitHub imports
successful previews
successful deployments

Do not optimize metrics before the underlying system is reliable.

113. Initial Operational Targets

The initial platform should aim for:

API availability: 99.9%
Workspace API availability: 99.9%
Runtime start success: 99%
Preview availability: 99%

These are planning targets from the observability specification.

They should be measured before being treated as achieved.

114. Roadmap Completion Model

RUNIX should move through these maturity levels:

Level 0 — Documentation
Level 1 — Functional Prototype
Level 2 — Working Cloud IDE
Level 3 — Developer Platform
Level 4 — Production Platform
Level 5 — Scalable Cloud Infrastructure
115. Level 0 — Documentation

Complete when:

specifications exist
architecture is defined
design source is defined
implementation standards exist
116. Level 1 — Functional Prototype

Complete when:

auth
projects
workspace
basic editor

work end-to-end.

117. Level 2 — Working Cloud IDE

Complete when:

editor
runtime
terminal
preview
tests
Git

work reliably.

118. Level 3 — Developer Platform

Complete when:

GitHub
AI
deployment
observability

are integrated.

119. Level 4 — Production Platform

Complete when:

security
reliability
backups
rollback
monitoring
alerting
scaling

are operational.

120. Level 5 — Scalable Cloud Infrastructure

Future state:

multi-host runtimes
runtime scheduling
multi-region
autoscaling
organizations
billing
enterprise controls
121. Final Implementation Sequence

The recommended concrete build sequence is:

01. Repository foundation
02. Docker Compose
03. PostgreSQL
04. Redis
05. FastAPI foundation
06. Database models
07. Alembic migrations
08. Authentication
09. Project CRUD
10. Template registry
11. Workspace filesystem
12. Error handling
13. Frontend foundation
14. Stitch landing page
15. Stitch authentication
16. Stitch dashboard
17. Stitch project creation
18. IDE shell
19. File explorer
20. Monaco editor
21. File persistence
22. Runtime database/API
23. Runtime Manager
24. Docker runtimes
25. Runtime lifecycle
26. xterm.js
27. WebSocket terminal
28. PTY
29. Port detection
30. Preview gateway
31. Live preview
32. Git integration
33. Git UI
34. GitHub App
35. Repository import
36. Test runner
37. Test UI
38. Observability
39. Runtime reconciliation
40. AI agent
41. AI tools
42. AI approval/diff
43. Deployment
44. Production CI/CD
45. Security hardening
46. Performance testing
47. Disaster recovery
48. Production launch
122. What Must Not Be Done

Do not:

build AI before runtime
build deployment before workspace persistence
execute user commands on API host
use fake runtime states
use fake test results
use fake AI completion
use fake Git status
use arbitrary Docker images
give user containers Docker socket access
overwrite user files during conflicts
silently overwrite Git changes
store secrets in frontend
skip authorization
skip path validation
skip runtime isolation tests
replace Stitch UI with a generic dashboard
123. Final Roadmap Principle

RUNIX should not be built as:

Dashboard
+
Chatbot
+
Code Editor

It should be built as:

Cloud Development Infrastructure
            +
Browser IDE
            +
Isolated Execution
            +
Developer Workflow

The fundamental product loop is:

BUILD
  ↓
RUN
  ↓
TEST
  ↓
PREVIEW
  ↓
SHIP

with AI acting as an optional controlled development layer around that workflow.

124. Final Roadmap Definition of Done

The roadmap is considered successfully executed when RUNIX can perform the following complete flow using real infrastructure:

User
 ↓
Sign In
 ↓
Dashboard
 ↓
Create Project
 ↓
Select Template
 ↓
Workspace Created
 ↓
IDE Opens
 ↓
Files Loaded
 ↓
Code Edited
 ↓
Code Saved
 ↓
Runtime Started
 ↓
Terminal Connected
 ↓
Command Executed
 ↓
Development Server Started
 ↓
Port Detected
 ↓
Preview Opened
 ↓
Tests Executed
 ↓
Git Status Retrieved
 ↓
Commit Created
 ↓
GitHub Push Completed
 ↓
Optional AI Assistance
 ↓
Optional Deployment

Every stage must use real backend state, real execution infrastructure, real persistence, and real error handling.

No stage may depend on a fake success state.