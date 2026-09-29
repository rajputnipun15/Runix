RUNIX — Definition of Done

Document: 21-DEFINITION-OF-DONE.md
Product: RUNIX
Tagline: Build. Run. Ship. Anywhere.
Status: Engineering Acceptance Specification
Version: 1.0
Audience: Engineering, QA, DevOps, Security, Product, Antigravity
Primary Visual Source: Approved RUNIX Stitch Project

1. Purpose

This document defines when RUNIX work is considered complete.

A feature is not done merely because:

code exists
the UI renders
an API returns a response
a Docker container starts
a button appears
a test passes locally

A feature is done only when its implementation, integration, security, error handling, observability, testing, documentation, and user experience satisfy the applicable acceptance criteria.

2. Definition of Done Hierarchy

RUNIX uses four levels:

Feature DoD
    ↓
Subsystem DoD
    ↓
Release DoD
    ↓
Production DoD

A production release cannot be considered complete if critical lower-level requirements remain incomplete.

3. Core Definition

A RUNIX feature is complete when:

Requirements
    +
Implementation
    +
Integration
    +
Error Handling
    +
Security
    +
Observability
    +
Testing
    +
Accessibility
    +
Documentation
    +
Deployment Validation

have been completed to the required level.

4. Universal Feature Checklist

Every feature must satisfy:

Requirement is understood.

Relevant specification was reviewed.

Existing implementation was inspected.

Dependencies were identified.

Backend behavior implemented where required.

Frontend behavior implemented where required.

Database changes implemented where required.

API contract implemented where required.

Error handling implemented.

Authorization verified.

Security implications reviewed.

Logging implemented.

Metrics implemented where applicable.

Tests implemented.

Documentation updated.

Build passes.

No known critical regression remains.

5. Requirement Traceability

Every significant implementation should be traceable to a specification.

Example:

Requirement
    ↓
PRD
    ↓
Functional Requirement
    ↓
Technical Specification
    ↓
Implementation
    ↓
Test

A feature should not be implemented solely from an informal assumption when an existing RUNIX specification already defines the behavior.

6. Source of Truth Hierarchy

When documents conflict, use this priority:

1. Security constraints
2. Architecture constraints
3. API/data contracts
4. Product requirements
5. Frontend Stitch/design requirements
6. Implementation details

For frontend visual decisions specifically:

Approved Stitch design
        ↓
Frontend specification
        ↓
Design system
        ↓
Implementation

The frontend must not invent a competing visual system.

7. Stitch Definition of Done

The approved Stitch project is the primary visual source of truth for RUNIX frontend implementation.

Frontend work is complete only when:

Correct Stitch screen was identified.

Layout hierarchy matches.

Major regions match.

Navigation matches.

Component hierarchy matches.

Typography hierarchy matches.

Spacing is consistent.

Colors/surfaces match the approved design language.

Borders and states match.

Interactions match where defined.

Responsive behavior is preserved.

Animations are implemented where meaningful.

Reduced-motion behavior exists where necessary.

No generic replacement UI has been introduced.

8. Stitch Project Reference

Approved project:

RUNIX Cloud Development Platform UI

Project ID:

2390441801388154937

Approved screens include:

98d2d9499d9143c8b95657d91fb2d856
Developer avatar

ff9274589d334fffbba97dfdec1f63e2
Cloud IDE

7bd5aaf3cb4a4318867e64ddb7b17294
Interactive Cloud IDE

a42d31e3c79a48a8a72729fc41fe4160
Developer Dashboard

12b851a93c9a42deb264221401ed819b
New Workspace

984a073b74c94908b31407a4d4a88df7
Interactive New Workspace

9c89cd452097490cb97fbc6ffa35bb3f
Create Workspace

9df9ed75441941a79f618295d6ca10c0
Landing Page

e5837e279f004f5fa918ab1812f5f056
Developer Sign In
9. Functional Definition of Done

A functional feature must:

Perform the intended operation.
Persist required state.
Return accurate status.
Handle expected failures.
Handle unexpected failures safely.
Respect authorization.
Provide appropriate user feedback.
Be testable.
Avoid introducing unrelated behavior.
10. Authentication Definition of Done

Authentication is complete when:

Registration works.

Login works.

Logout works.

Session persistence works.

Session expiration works.

Refresh works.

Invalid credentials are rejected.

Disabled accounts are rejected.

Passwords are securely hashed.

Sensitive authentication data is not logged.

Authentication events are observable.

Authentication errors use stable error codes.

Rate limiting is active.

Protected routes require authentication.

Frontend handles expired sessions correctly.

11. Authorization Definition of Done

Authorization is complete when:

Project ownership is enforced.

Project membership is enforced.

Role permissions are enforced.

Backend checks permissions.

Frontend does not act as the security boundary.

Unauthorized resource access is rejected.

Cross-project access is prevented.

WebSocket authorization is enforced.

Preview authorization is enforced.

Runtime authorization is enforced.

GitHub operations are authorized.

12. Project Definition of Done

Project management is complete when:

Projects can be created.

Projects can be listed.

Projects can be viewed.

Projects can be updated.

Projects can be deleted.

Ownership is stored.

Membership is enforced.

Slugs are validated.

Templates are resolved.

Template versions are persisted.

Invalid project creation is rejected.

Deletion behavior is safe.

Audit events are generated for important operations.

13. Template Definition of Done

A template is complete when:

Template ID exists.

Template version exists.

Runtime image is approved.

Runtime image is immutable.

Manifest exists.

Required files exist.

Integrity hash is valid.

Template can be materialized.

No code executes on the control plane.

Dependencies install inside the runtime.

Startup command works.

Expected ports work.

Template acceptance tests pass.

Template documentation exists.

14. Workspace Definition of Done

Workspace functionality is complete when:

Workspace is created.

Workspace persists.

Files can be read.

Files can be written.

Files can be deleted.

Files can be renamed.

Directories can be created.

Directory traversal works.

Search works.

Hidden files are handled appropriately.

Workspace quota is enforced.

File size limits are enforced.

Path traversal is blocked.

Symlink escape is prevented.

Atomic writes are used.

File hashes are generated.

Optimistic concurrency works.

Sensitive content is not logged.

Workspace survives runtime shutdown.

15. Filesystem Security Definition of Done

The filesystem layer is not complete until all of the following are tested:

../
../../
absolute paths
Windows paths
encoded traversal
null bytes
symlink escapes
large files
large directory trees
quota exhaustion
concurrent writes

Every unsafe path must be rejected.

16. Editor Definition of Done

The Monaco editor is complete when:

Files open.

Tabs work.

Editing works.

Syntax highlighting works.

Line numbers work.

Minimap works where designed.

Breadcrumbs work.

Dirty state is visible.

Save works.

Save errors are visible.

File conflicts are handled.

Keyboard shortcuts work.

Large files are handled appropriately.

Editor state survives normal navigation where intended.

Accessibility is acceptable.

17. Editor Save Definition of Done

A save operation is complete only when:

Editor content
    ↓
Hash validation
    ↓
API request
    ↓
Workspace write
    ↓
Persistent storage
    ↓
Successful response
    ↓
Editor marked saved

The frontend must never mark a file as saved before backend confirmation.

18. Runtime Definition of Done

The runtime system is complete when:

Runtime can be created.

Runtime can be started.

Runtime can be stopped.

Runtime can be restarted.

Runtime can be terminated.

Runtime state is persisted.

Runtime state transitions are valid.

Runtime labels are applied.

Workspace is mounted.

Resource limits are applied.

Network restrictions are applied.

Runtime cleanup works.

Runtime reconciliation works.

Orphan containers are handled.

Runtime failures are visible.

Runtime recovery is bounded.

19. Runtime Security Definition of Done

Every user runtime must satisfy:

No --privileged.

No Docker socket.

No host root mount.

No arbitrary host mounts.

No host networking.

CPU limit enforced.

Memory limit enforced.

PID limit enforced.

Storage limit enforced.

Command timeout enforced.

Idle timeout enforced.

Image allowlist enforced.

User runtime is treated as untrusted.

Internal services are protected.

Container cleanup is reliable.

20. Runtime Isolation Test

The following must be tested before runtime production approval:

User container
    X → Docker socket
    X → host root
    X → arbitrary host filesystem
    X → Docker daemon API
    X → internal database
    X → Redis
    X → metadata services
    X → other user runtime

Any unexpected access is a release blocker.

21. Terminal Definition of Done

Terminal functionality is complete when:

xterm.js renders.

WebSocket authentication works.

PTY is created.

Input works.

Output streams.

Resize works.

Ping/pong works.

Close works.

Runtime state is checked.

Connection limits work.

Message size limits work.

Idle timeout works.

Reconnection works.

Terminal output is not unnecessarily persisted.

Secrets are not logged.

22. Terminal Security Definition of Done

A terminal connection must never:

execute on the API host
bypass runtime isolation
access another project
access another user's runtime
bypass command limits
expose runtime credentials
expose host credentials
23. Preview Definition of Done

Preview is complete when:

Runtime exists.

Application port is detected.

Port belongs to the correct runtime.

Preview URL is generated.

Preview gateway authenticates requests.

Cross-project access is prevented.

Unauthorized ports cannot be exposed.

Runtime failures are reflected in preview state.

Preview timeout works.

Preview recovery works.

HTTPS is used in production.

24. Git Definition of Done

Git functionality is complete when:

Repository status works.

Diff works.

Stage works.

Unstage works.

Commit works.

Push works.

Pull works.

Branch list works.

Branch creation works.

Checkout works.

Dirty working tree is detected.

Conflicts are surfaced.

User changes are protected.

Credentials are protected.

25. Git Conflict Definition of Done

Git conflict handling is complete when:

Conflict is detected.

User is informed.

Local changes are preserved.

Remote changes are preserved.

Conflict information is accessible.

Automatic destructive overwrite does not occur.

Resolution workflow is explicit.

26. GitHub Definition of Done

GitHub integration is complete when:

GitHub authentication works.

Installation state is checked.

Repository listing works.

Repository access is validated.

Repository import works.

Import is asynchronous.

Import state is persisted.

Import failures are recoverable.

GitHub credentials remain server-side.

OAuth state/CSRF protection exists where applicable.

Rate limiting is handled.

Provider failures are isolated.

27. GitHub Import Definition of Done

Import must perform:

Authenticate
    ↓
Verify repository access
    ↓
Create project
    ↓
Create workspace
    ↓
Clone repository
    ↓
Checkout target branch
    ↓
Index files
    ↓
Persist metadata
    ↓
Finalize project

Repository code must not execute on the control plane during import.

28. Test Platform Definition of Done

The test platform is complete when:

Tests execute inside runtime.

Test command is controlled.

Test run state is persisted.

Output is captured safely.

Exit code is recorded.

Duration is recorded.

Counts are recorded where supported.

Timeout works.

Cancellation works.

Failed assertions differ from runner failures.

Results appear in UI.

Rerun works.

29. AI Agent Definition of Done

AI is complete only when:

Provider abstraction exists.

Repository context can be inspected.

Files can be read.

Code can be searched.

Plans can be generated.

Plans can be reviewed.

Patches can be generated.

Diffs can be shown.

Approval gates work.

Patch conflicts are detected.

Tests can be executed.

AI tool activity is auditable.

AI cannot access the host directly.

AI cannot bypass runtime security.

AI cannot silently commit/push/deploy.

30. AI Approval Definition of Done

The following must require explicit approval unless configuration explicitly permits otherwise:

destructive file deletion

dependency installation/change

security configuration changes

environment configuration changes

side-effectful shell commands

Git commit

Git push

deployment

31. AI Safety Definition of Done

AI must not:

execute arbitrary host commands
read host filesystem
access Docker socket
read unrelated projects
access secrets unnecessarily
bypass project authorization
modify files without the configured approval policy
claim tests passed without actual test results
claim changes were applied without successful persistence
32. Deployment Definition of Done

Deployment is complete when:

Build is reproducible.

Images are immutable.

Image digests are tracked.

Security scans pass.

Database migrations are validated.

Secrets are securely injected.

Health checks pass.

Readiness checks pass.

Smoke tests pass.

Rollback is available.

Deployment is observable.

Release is traceable to source commit.

33. Database Definition of Done

Database implementation is complete when:

Schema matches specification.

Foreign keys exist.

Unique constraints exist.

Required indexes exist.

Migrations exist.

Migrations run from a clean database.

Migrations work on representative existing data.

Transactions are used appropriately.

Connection pooling is configured.

Backup is configured.

Restore has been tested.

34. API Definition of Done

Every API endpoint must have:

authentication requirements

authorization requirements

request schema

response schema

validation

error codes

correct HTTP status

request ID

logging

tests

documentation

35. API Security Definition of Done

API security is complete when:

authentication cannot be bypassed

authorization cannot be bypassed

request validation exists

rate limiting exists where appropriate

sensitive fields are protected

error leakage is prevented

CORS is configured

CSRF protection is applied where necessary

SSRF risks are controlled

path traversal is blocked

unsafe deserialization is avoided

36. Error Handling Definition of Done

Error handling is complete when:

Stable error codes exist.

HTTP mapping is correct.

WebSocket errors are normalized.

Domain exceptions exist.

Unexpected exceptions are sanitized.

Request IDs are returned.

Retryability is accurate.

Frontend states exist.

Recovery actions are safe.

Errors are logged.

Error metrics exist.

Security-sensitive errors are audited.

No secrets are leaked.

37. Observability Definition of Done

Observability is complete when:

Structured logs exist.

Request IDs exist.

Trace IDs exist.

Runtime metrics exist.

API metrics exist.

Worker metrics exist.

Workspace metrics exist.

WebSocket metrics exist.

Preview metrics exist.

Git/GitHub metrics exist.

AI metrics exist.

Database health exists.

Redis health exists.

Audit events exist.

Alerts exist.

Sensitive data is redacted.

38. Frontend Definition of Done

Frontend work is complete when:

Stitch design is respected.

TypeScript passes.

Lint passes.

Components are reusable.

API integration is real.

Loading states exist.

Empty states exist.

Error states exist.

Success states exist.

Offline states exist where applicable.

Keyboard navigation works.

Focus behavior works.

Responsive behavior works.

Reduced motion is supported.

Visual regression passes.

No fake functionality remains.

39. IDE Definition of Done

The cloud IDE is complete when:

Dashboard
    ↓
Open Project
    ↓
Workspace
    ↓
File Explorer
    ↓
Editor
    ↓
Runtime
    ↓
Terminal
    ↓
Preview
    ↓
Tests
    ↓
Git

works as a coherent workflow.

40. Responsive Definition of Done
Desktop

The full IDE is supported.

Expected:

Explorer
+
Editor
+
AI
+
Terminal
+
Preview
Laptop

Secondary panels may collapse or resize.

Tablet

Secondary panels should become collapsible.

Mobile

The goal is project management rather than full desktop IDE parity.

Support:

authentication
dashboard
project creation
project navigation
runtime status
basic project management

Do not force the complete desktop IDE into a small viewport.

41. Accessibility Definition of Done

Semantic HTML used.

Keyboard navigation works.

Focus states are visible.

Dialogs manage focus.

Error states are announced appropriately.

Contrast is sufficient.

Color is not the only status signal.

Reduced motion is supported.

Interactive elements have accessible names.

Forms expose labels and validation errors.

42. Performance Definition of Done

Initial targets:

Operation	Target
Health	<200 ms
Simple auth API	<500 ms
Project list	<500 ms
File metadata	<500 ms
WebSocket connection	<2 s
Runtime start	<30 s
Preview readiness	<45 s

Performance testing must use representative workloads.

43. Load Testing Definition of Done

Load tests must evaluate:

concurrent API requests

concurrent projects

runtime startup

terminal connections

WebSocket output

workspace operations

job queues

preview traffic

database connections

Redis operations

The system must degrade predictably under overload.

44. Security Testing Definition of Done

Required tests:

Authentication
Authorization
Path Traversal
SSRF
XSS
CSRF
Secret Leakage
Container Escape
Docker Access
Preview Isolation
GitHub Credential Handling
AI Tool Boundaries
Rate Limiting
Resource Exhaustion
45. Runtime Security Release Gate

Any release affecting:

Docker
runtime manager
runtime networking
workspace mounts
terminal
preview
command execution
resource limits

must pass the complete runtime security test suite.

Failure blocks release.

46. Data Integrity Definition of Done

The system must preserve:

project metadata

workspace files

Git state

runtime metadata

test results

job state

audit events

under expected failure conditions.

47. Failure Recovery Definition of Done

Test:

API restart
Worker restart
Redis restart
Database restart
Runtime crash
Runtime manager restart
WebSocket disconnect
Preview failure
GitHub outage
AI provider outage
Disk pressure
Network interruption

The expected recovery behavior must be documented and verified.

48. Backup Definition of Done

Backups are complete only when:

backup is created

retention exists

backup is protected

restore procedure exists

restore has been tested

restored data is validated

49. Disaster Recovery Definition of Done

A disaster recovery plan is complete when the team can restore:

PostgreSQL
Workspace Storage
RUNIX Application
Runtime Images
Secrets
Network Configuration

and return the platform to a usable state.

50. CI Definition of Done

CI must automatically run:

Lint
Typecheck
Unit Tests
Integration Tests
Security Tests
Build
Container Tests
Runtime Isolation Tests
E2E Tests

as applicable.

51. CD Definition of Done

Continuous delivery is complete when:

artifact builds are reproducible

artifacts are versioned

artifacts are scanned

deployment is automated

migrations are controlled

health checks exist

smoke tests exist

rollback exists

deployment telemetry exists

52. Documentation Definition of Done

Documentation is complete when:

feature behavior is documented

API behavior is documented

environment variables are documented

operational behavior is documented

security constraints are documented

failure behavior is documented

setup instructions are updated

implementation deviations are documented

53. No Fake Functionality Rule

RUNIX must never ship fake:

runtime status
terminal output
test results
Git status
GitHub repository data
AI results
deployment status
preview status
save confirmation

If a feature is not implemented, show:

Not available
Coming soon
Disabled
Configuration required

as appropriate.

Never simulate successful infrastructure operations.

54. No Silent Failure Rule

The following are prohibited:

catch exception and ignore
return success after partial failure
hide failed runtime
discard failed file save
swallow Git conflict
hide GitHub import failure
claim AI completion without applying patch
claim tests passed without executing tests
55. No Silent Data Loss Rule

RUNIX must never silently discard user work.

This applies to:

editor changes
workspace files
Git changes
imported repositories
AI patches
runtime-generated files

Potential destructive operations must be explicit.

56. Feature Flags Definition of Done

A feature behind a flag must:

Have a documented flag.

Have a default state.

Have truthful UI.

Not expose insecure partial functionality.

Be testable in enabled and disabled states.

57. Migration Definition of Done

A database migration is complete when:

Migration file exists.

Migration applies cleanly.

Migration is tested.

Existing data remains valid.

Rollout compatibility is verified.

Rollback strategy is understood.

Production impact is documented.

58. API Compatibility Definition of Done

API changes are complete when:

Existing clients remain compatible where required.

Error codes remain stable.

Response shape is intentional.

Deprecated fields have a migration plan.

Documentation is updated.

Tests cover compatibility.

59. Database Compatibility Definition of Done

During rolling deployments:

old application
+
new application
+
current schema

must remain compatible unless deployment architecture explicitly guarantees otherwise.

60. Production Readiness Definition of Done

RUNIX is production-ready only when:

Product

Core user journey works.

Error states work.

Recovery works.

UI matches approved Stitch design.

Backend

API stable.

Database stable.

Authentication secure.

Authorization secure.

Runtime

User code isolation validated.

Runtime lifecycle reliable.

Terminal reliable.

Preview isolated.

Integrations

Git works.

GitHub works.

External failures are handled.

Operations

CI/CD works.

Monitoring works.

Alerts work.

Backups work.

Restore tested.

Rollback tested.

Security

Security testing complete.

Secrets protected.

Runtime isolation tested.

Audit logging active.

61. MVP Definition of Done

RUNIX MVP is complete when the following real end-to-end flow works:

Sign In
   ↓
Dashboard
   ↓
Create Project
   ↓
Select Template
   ↓
Create Workspace
   ↓
Open IDE
   ↓
Edit File
   ↓
Save File
   ↓
Start Runtime
   ↓
Open Terminal
   ↓
Run Command
   ↓
Start Dev Server
   ↓
Detect Port
   ↓
Open Preview
   ↓
Run Tests
   ↓
View Git Status
   ↓
Commit

No stage may rely on mocked success behavior.

62. V1 Definition of Done

V1 additionally requires:

GitHub integration.

Repository import.

Template versioning.

Runtime reconciliation.

Structured observability.

Production error handling.

CI/CD.

Production security hardening.

Backup and recovery procedures.

63. AI Release Definition of Done

AI should not be considered production-ready until:

Repository context works.

Tool permissions are enforced.

Diff-first workflow works.

Approval gates work.

Patch conflicts work.

Runtime execution is isolated.

AI cannot access host resources.

Tests run after changes.

AI cannot falsely report success.

AI activity is auditable.

Provider failures are handled.

64. Deployment Release Definition of Done

Deployment is complete when:

Build
 ↓
Artifact
 ↓
Security Scan
 ↓
Migration
 ↓
Deploy
 ↓
Health
 ↓
Smoke Test
 ↓
Telemetry
 ↓
Verification

passes successfully.

65. Release Candidate Checklist

Before declaring a release candidate:

All P0 features complete.

Critical P1 features complete or explicitly excluded.

No critical security issues.

No known data-loss issue.

Runtime isolation tests pass.

E2E critical flow passes.

Stitch visual regression passes.

Accessibility checks pass.

Performance targets measured.

Production deployment tested.

Rollback tested.

66. Release Blockers

The following automatically block release:

Critical security vulnerability
Runtime escape vulnerability
Unauthorized project access
User data loss
Database corruption
Secret leakage
Host command execution by user code
Docker socket exposure
Broken authentication
Broken authorization
Unrecoverable workspace corruption
False successful runtime state
False successful test state
False successful deployment state
67. P0 Bug Definition

A P0 bug is a defect that:

compromises security
causes significant user data loss
allows unauthorized access
breaks core platform execution
prevents the core product flow
causes systemic production failure

P0 bugs must be resolved before release.

68. P1 Bug Definition

P1 bugs significantly affect functionality but do not compromise the core security or data-integrity boundary.

Examples:

major UI workflow failure
GitHub import failures
preview failures affecting common templates
repeated runtime startup failures

P1 resolution is required according to release policy.

69. P2 Bug Definition

P2 bugs are lower-impact issues such as:

visual inconsistencies
minor performance problems
uncommon edge cases
secondary UI issues

These may be deferred with explicit tracking.

70. Code Review Definition of Done

Every significant pull request should verify:

Architecture

Correct layer.

No unnecessary coupling.

Existing abstractions reused.

Security

Input validation.

Authorization.

Secret handling.

Runtime safety.

Reliability

Failure handling.

Retry behavior.

Cleanup.

Quality

Tests.

Type checking.

Lint.

Documentation.

Frontend

Stitch alignment.

Accessibility.

Responsive behavior.

71. Antigravity Definition of Done

When Antigravity implements a task, it must not report:

Done

merely because files were generated.

It should verify:

implemented
tested
integrated
validated

before reporting completion.

72. Antigravity Implementation Loop

Use:

Read specification
      ↓
Inspect repository
      ↓
Inspect relevant Stitch screen
      ↓
Identify existing abstractions
      ↓
Implement
      ↓
Run tests
      ↓
Run lint/typecheck
      ↓
Run integration checks
      ↓
Review security
      ↓
Review UI
      ↓
Fix failures
      ↓
Document result
73. Frontend Agent Rule

When implementing frontend:

Stitch
  ↓
Visual reference
  ↓
Existing component system
  ↓
RUNIX feature implementation

The agent must not replace an existing Stitch-derived screen with a generic dashboard, generic IDE, or generic AI chatbot.

74. Backend Agent Rule

Backend implementations must follow:

Route
 ↓
Service
 ↓
Domain
 ↓
Repository / Infrastructure

Business logic should not accumulate inside FastAPI route handlers.

75. Runtime Agent Rule

Runtime implementations must follow:

API
 ↓
Service
 ↓
Runtime Manager
 ↓
Docker
 ↓
User Runtime

The API must never directly execute arbitrary user commands.

76. Testing Agent Rule

Tests must validate behavior rather than implementation details whenever possible.

Prioritize:

user-visible behavior
API contracts
security boundaries
data integrity
runtime isolation
77. Security Agent Rule

Security review must assume:

user code = untrusted
repository = potentially untrusted
dependency = potentially untrusted
terminal command = untrusted
AI-generated command = untrusted
GitHub repository = untrusted

The system must remain secure under these assumptions.

78. Production Incident Definition of Done

An incident is resolved only when:

Immediate failure is mitigated.

User impact is understood.

Root cause is identified or bounded.

Recovery is verified.

Monitoring confirms stability.

Relevant data integrity is verified.

Required rollback is complete.

Follow-up actions are documented.

79. Post-Incident Definition of Done

For significant incidents:

Incident timeline created.

Root cause documented.

Contributing factors documented.

Detection gap identified.

Prevention action defined.

Tests added where appropriate.

Monitoring improved where appropriate.

Documentation updated.

80. Final End-to-End Acceptance Test

The final RUNIX acceptance test is:

1. Open RUNIX
2. Sign in
3. Open dashboard
4. Create a React + Vite + TypeScript project
5. Workspace is created
6. IDE opens
7. File explorer displays project files
8. Open source file
9. Modify code
10. Save
11. Verify persistence
12. Start runtime
13. Verify runtime status
14. Open terminal
15. Execute command
16. Verify command output
17. Start development server
18. Detect application port
19. Open preview
20. Verify application loads
21. Run tests
22. Verify real test result
23. Open Git status
24. View diff
25. Commit changes
26. Connect GitHub
27. Push changes
28. Stop runtime
29. Restart runtime
30. Reopen project
31. Verify workspace persists
32. Verify Git state
33. Verify observability
34. Verify audit events

The test passes only if every stage uses actual RUNIX functionality.

81. Final Security Acceptance Test

Attempt:

1. Access another user's project.
2. Access another project's files.
3. Traverse outside workspace.
4. Mount arbitrary host path.
5. Access Docker socket.
6. Execute host command.
7. Access PostgreSQL directly from runtime.
8. Access Redis directly from runtime.
9. Access another runtime.
10. Expose unauthorized port.
11. Reuse invalid preview token.
12. Forge GitHub callback.
13. bypass AI approval.
14. inject secrets into logs.

Every unauthorized action must fail.

82. Final Reliability Acceptance Test

Simulate:

API restart
Worker restart
Redis restart
Database interruption
Runtime crash
Runtime manager restart
Terminal disconnect
Preview failure
GitHub outage
AI provider outage
Disk pressure
Network interruption

RUNIX must:

fail predictably
preserve user data
expose accurate state
recover where designed
provide actionable errors
maintain security boundaries
83. Final Visual Acceptance Test

Every primary screen must be compared against the approved Stitch implementation.

Required screens:

Landing
Sign In
Dashboard
Create Workspace
Cloud IDE
Interactive Cloud IDE
Runtime states
Terminal
Preview
Source Control
AI Agent
Error states
Empty states
Loading states

The visual review must verify:

hierarchy
spacing
typography
component dimensions
alignment
surfaces
borders
status indicators
interactions
responsive behavior
84. Final Performance Acceptance Test

Measure:

page startup
dashboard loading
project creation
file tree loading
file opening
file saving
runtime startup
terminal connection
terminal latency
preview startup
test execution
Git status
GitHub import

Compare results with the targets defined in:

16-TESTING-STRATEGY.md
17-OBSERVABILITY.md
20-ROADMAP.md
85. Final Documentation Acceptance Test

Before production launch:

README is current.

Architecture docs are current.

API documentation is current.

Environment variables documented.

Local setup documented.

Deployment documented.

Runtime security documented.

Error codes documented.

Troubleshooting documented.

Recovery procedures documented.

Stitch integration documented.

Known limitations documented.

86. Final Production Acceptance Matrix
Area	Required
Authentication	PASS
Authorization	PASS
Projects	PASS
Templates	PASS
Workspace	PASS
Editor	PASS
Runtime	PASS
Terminal	PASS
Preview	PASS
Git	PASS
GitHub	PASS
Tests	PASS
Error Handling	PASS
Security	PASS
Observability	PASS
Deployment	PASS
Backup	PASS
Recovery	PASS
Accessibility	PASS
Performance	PASS
Stitch Visual Alignment	PASS
E2E Critical Flow	PASS

Any critical FAIL blocks production release.

87. Final RUNIX Product Acceptance

RUNIX is considered functionally complete when a developer can genuinely:

BUILD

a project,

RUN

the project inside an isolated cloud runtime,

TEST

the project,

PREVIEW

the running application,

COMMIT

their changes,

PUSH

them to GitHub,

and use the browser as the primary development environment throughout the workflow.

88. Final Engineering Principle

The standard for RUNIX is not:

"It works on my machine."

The standard is:

"It works through the complete system boundary,
with real persistence, real execution,
real security controls, real observability,
real failure handling, and verified tests."
89. Final Product Principle

RUNIX must feel like one coherent developer platform:

              RUNIX
                │
       ┌────────┼────────┐
       │        │        │
     BUILD     RUN      SHIP
       │        │        │
     Editor   Runtime   Git
     Files    Terminal  GitHub
     AI       Preview   Deploy
              Tests

The product should not feel like separate tools glued together.

90. Final Architecture Principle

The final RUNIX system must preserve:

                    BROWSER
                       │
                       ▼
                 CONTROL PLANE
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    PostgreSQL       Redis          Workers
        │                             │
        └──────────────┬──────────────┘
                       ▼
                RUNTIME MANAGER
                       │
                       ▼
                EXECUTION PLANE
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Runtime      Runtime      Runtime
          │            │            │
          └────────────┼────────────┘
                       ▼
                    PREVIEW

The control plane manages the platform.

The execution plane executes user workloads.

The browser provides the development interface.

No boundary may be bypassed for convenience.

91. Final Rule Set

The following are non-negotiable:

User code never executes on the API host.
User runtimes never receive Docker socket access.
User runtimes never receive arbitrary host mounts.
Authentication is enforced server-side.
Authorization is enforced server-side.
Workspace paths are validated.
User data is not silently discarded.
Git conflicts do not silently overwrite changes.
AI changes follow the approval policy.
Fake success states are prohibited.
Runtime status reflects real runtime state.
Test status reflects real test execution.
Preview status reflects actual application availability.
Git status reflects the actual repository.
Deployment status reflects actual deployment state.
Errors are observable and traceable.
Secrets are never exposed to the browser unnecessarily.
Production images are immutable.
Database changes use migrations.
Critical failures block release.
The Stitch project remains the frontend visual source of truth.
Security requirements override convenience.
Data integrity overrides feature speed.
Real functionality overrides visual simulation.
Every production capability must be testable.
92. Final Completion Statement

RUNIX is DONE only when the system can demonstrate:

REAL USER
    ↓
REAL AUTHENTICATION
    ↓
REAL PROJECT
    ↓
REAL WORKSPACE
    ↓
REAL EDITOR
    ↓
REAL RUNTIME
    ↓
REAL TERMINAL
    ↓
REAL APPLICATION
    ↓
REAL PREVIEW
    ↓
REAL TESTS
    ↓
REAL GIT
    ↓
REAL GITHUB
    ↓
REAL OBSERVABILITY
    ↓
REAL DEPLOYMENT

with:

Security
+
Reliability
+
Persistence
+
Error Handling
+
Testing
+
Observability
+
Accessibility
+
Stitch Visual Fidelity

verified.

93. Final Release Gate

The RUNIX production release may be declared complete only after all required acceptance checks have passed and the implementation team can reproduce the complete developer workflow from a clean environment.

The final question is not:

Does the application render?

The final question is:

Can a developer reliably build, run, test, preview, commit, and ship real software through RUNIX without crossing the platform's security and reliability boundaries?

If the answer is yes, and all required acceptance gates above pass, RUNIX has met its Definition of Done.