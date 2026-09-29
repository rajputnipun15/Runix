RUNIX Runtime Engine Specification

## 1. Purpose

The RUNIX Runtime Engine provides isolated cloud development environments in which user projects can be:

- installed
- executed
- tested
- built
- served
- debugged
- accessed through a terminal
- accessed through a live preview

The Runtime Engine is responsible for managing isolated execution environments.

The API server must never execute arbitrary user code directly.

---

# 2. Core Principle

RUNIX separates the control plane from the execution plane.

```text
CONTROL PLANE
────────────────────────────────────────

Browser
   │
   ▼
RUNIX API
   │
   ├── PostgreSQL
   ├── Redis
   └── Runtime Manager
                │
                ▼

EXECUTION PLANE
────────────────────────────────────────

      Isolated Runtime
      ┌───────────────────────┐
      │ /workspace            │
      │ Node / Python / etc.  │
      │ npm / pip / git       │
      │ dev server            │
      │ terminal              │
      └───────────────────────┘

User code executes only inside the execution plane.

3. Runtime Responsibilities

The Runtime Engine must provide:

runtime creation
runtime startup
runtime stopping
runtime restarting
runtime termination
runtime health checks
workspace mounting
environment configuration
resource limits
process limits
network restrictions
port discovery
preview integration
terminal integration
cleanup
abandoned runtime detection
runtime state reconciliation
4. Runtime Lifecycle

A runtime follows this lifecycle:

CREATING
    │
    ▼
STARTING
    │
    ▼
RUNNING
    │
    ├───────────────┐
    │               │
    ▼               ▼
STOPPING          FAILED
    │
    ▼
STOPPED
    │
    ▼
STARTING

Permanent termination:

RUNNING
   ↓
STOPPING
   ↓
STOPPED
   ↓
TERMINATING
   ↓
TERMINATED
5. Runtime States

Supported states:

CREATING
STARTING
RUNNING
STOPPING
STOPPED
FAILED
TERMINATING
TERMINATED

Database values must use lowercase equivalents:

creating
starting
running
stopping
stopped
failed
terminating
terminated
6. Runtime State Definitions
CREATING

The runtime record exists but the container has not been successfully created.

STARTING

The container exists and RUNIX is preparing the environment.

Tasks may include:

mounting workspace
starting container
initializing shell
checking filesystem
installing required runtime bootstrap dependencies
detecting project configuration
checking health
RUNNING

The runtime is available.

The user can:

open terminal
execute commands
run tests
start development servers
access previews
STOPPING

RUNIX is shutting down the runtime.

STOPPED

The container is no longer running but runtime metadata remains.

The workspace remains persistent.

FAILED

The runtime could not start or became unhealthy.

A failure reason must be recorded.

TERMINATING

The runtime is being permanently removed.

TERMINATED

The runtime container has been removed.

Historical metadata may remain in PostgreSQL.

7. Runtime Types

Initial runtime types:

node
python
mern
blank

Future types may include:

java
cpp
go
rust
php
ruby

Do not implement additional runtime types merely because they are listed here.

They must have corresponding:

runtime images
security configuration
templates
tests
resource policy
documentation
8. Runtime Images

Initial images:

runix/node:22
runix/python:3.12
runix/mern:<version>
runix/blank:<version>

Production deployments must use immutable image references.

Prefer:

image digest

over mutable tags.

Example:

runix/node@sha256:abcdef...

Tags may be used during development.

Production must not depend on a mutable latest tag.

9. Node Runtime

Initial Node runtime:

Node.js 22

Expected tools:

node
npm
npx
git
bash

The runtime should provide:

/workspace

as the project directory.

10. Python Runtime

Initial Python runtime:

Python 3.12

Expected tools:

python
pip
git
bash

The runtime should provide:

/workspace

as the project directory.

11. MERN Runtime

The MERN runtime supports projects containing:

MongoDB client libraries
Express
React
Node.js

RUNIX itself uses PostgreSQL.

MongoDB is only part of the user-project development environment.

RUNIX must not automatically expose RUNIX's internal PostgreSQL or Redis services to user containers.

12. Blank Runtime

The blank runtime provides a minimal development environment.

It is useful for:

experiments
custom projects
imported repositories
future language support

The blank runtime must still comply with all runtime security policies.

13. Runtime Resource Limits

Every runtime must have resource limits.

Initial configurable defaults:

CPU:
1 vCPU

Memory:
1024 MB

Workspace storage:
2048 MB

Process limit:
256 processes

Command timeout:
120 seconds

Runtime idle timeout:
30 minutes

These are initial defaults, not immutable values.

14. Resource Configuration

Environment configuration:

RUNIX_RUNTIME_CPU_LIMIT=1
RUNIX_RUNTIME_MEMORY_MB=1024
RUNIX_RUNTIME_STORAGE_MB=2048
RUNIX_RUNTIME_PIDS_LIMIT=256
RUNIX_COMMAND_TIMEOUT_SECONDS=120
RUNIX_RUNTIME_IDLE_TIMEOUT_SECONDS=1800

Production infrastructure may override these values.

The frontend must not be allowed to arbitrarily increase them.

15. CPU Limits

A runtime must not consume unlimited CPU.

Example Docker configuration concept:

CPU quota / CPU period

or an equivalent container runtime mechanism.

The exact implementation must be encapsulated inside the Runtime Manager.

Do not expose Docker-specific resource configuration directly through the frontend.

16. Memory Limits

Every runtime must have a hard memory limit.

Example:

1 GB

When the runtime exceeds the configured limit, the container runtime may terminate processes or the container.

RUNIX must detect this and report:

RUNTIME_OUT_OF_MEMORY

where possible.

17. Process Limits

Each runtime must have a process limit.

Example:

256 processes

This reduces the risk of process-fork abuse.

The limit must be configured through the container runtime.

18. Storage Limits

Each workspace must have a storage quota.

Initial default:

2 GB

RUNIX must monitor:

workspace size

If the limit is exceeded:

WORKSPACE_STORAGE_LIMIT_EXCEEDED

The API should prevent operations that would cause uncontrolled storage growth where practical.

19. Container Security

User containers must not run with unnecessary privileges.

Do NOT use:

--privileged

for normal RUNIX runtimes.

Avoid unnecessary Linux capabilities.

Prefer:

drop unnecessary capabilities

Use the default container security profile unless a specific runtime requirement has been reviewed.

20. Root User

User processes should run as a non-root user whenever practical.

Example:

runix

rather than:

root

The runtime image should define an appropriate development user.

Some development operations may require additional permissions.

Those permissions must be granted inside the container only.

Never solve permission problems by giving the container host-level privileges.

21. Docker Socket

The Docker socket must NEVER be mounted into user containers.

Never:

-v /var/run/docker.sock:/var/run/docker.sock

User code must not be able to control the host Docker daemon.

This is a critical security requirement.

22. Host Filesystem

Never mount arbitrary host directories into a user runtime.

Forbidden:

/
 /etc
 /home
 /root
 /var
 /proc
 /sys

Do not expose:

host SSH keys
cloud credentials
RUNIX configuration
database credentials
Docker configuration
system secrets
23. Workspace Mount

Only the project's dedicated workspace may be mounted into the runtime.

Example conceptual mapping:

RUNIX Workspace Storage
        │
        ▼
/workspace

The mapping must be generated by RUNIX.

The client cannot choose:

/mnt/private

or:

/home/server

as a workspace path.

24. Workspace Isolation

Project A:

/workspaces/project-A

Project B:

/workspaces/project-B

A runtime for Project A must never access Project B.

The application must enforce:

project ID
    ↓
workspace ID
    ↓
workspace path

Do not construct workspace paths directly from arbitrary user input.

25. Runtime Network

User runtimes must not receive unrestricted access to the RUNIX internal network.

Avoid exposing:

PostgreSQL
Redis
RUNIX API internal services
Docker daemon
host services

by default.

The runtime network should be isolated.

26. Internet Access

Internet access may be required for development.

Examples:

npm install
pip install
git clone
API requests
package downloads

However, unrestricted network access increases security risk.

The Runtime Engine should support configurable network policies.

Initial policy:

development:
    outbound internet = allowed

production:
    outbound internet = controlled/configurable

Internal RUNIX services must remain inaccessible.

27. DNS

User containers require DNS for normal development.

DNS must resolve public internet domains where network access is enabled.

Internal service names should not automatically expose RUNIX infrastructure.

28. Network Isolation

Never use host networking:

--network host

for normal user runtimes.

Use an isolated container network.

29. Port Management

Development servers commonly listen on ports such as:

3000
4173
5173
8000
8080

RUNIX must detect application ports.

The user should not need to expose host ports manually.

30. Port Discovery

RUNIX may discover ports using:

process inspection
container listening socket information
configured project metadata
runtime logs
development-server output

Example:

npm run dev

Local:
http://localhost:5173

RUNIX detects:

5173

and registers it with the Preview system.

31. Allowed Port Range

Use a configurable port range.

Example:

RUNIX_PREVIEW_PORT_MIN=3000
RUNIX_PREVIEW_PORT_MAX=9999

The internal runtime may listen on any supported development port within policy.

RUNIX's proxy determines how the port becomes accessible to the browser.

32. Port Collision

Multiple projects may use the same internal port.

Example:

Project A → 5173
Project B → 5173

This is acceptable because each runtime has an isolated network namespace.

The external preview layer maps them separately.

Example:

Project A
https://preview.RUNIX_DOMAIN/project/A/port/5173

Project B
https://preview.RUNIX_DOMAIN/project/B/port/5173

The production URL format must be configurable.

33. Preview Security

A preview must not automatically become publicly accessible.

The preview gateway should validate:

authenticated user
project access
runtime status
requested port
preview authorization

Possible mechanisms:

authenticated preview session
signed preview token
short-lived preview URL
34. Preview Proxy

Architecture:

Browser
   │
   ▼
Preview Gateway
   │
   ├── authenticate
   ├── authorize
   ├── validate project
   ├── validate port
   │
   ▼
Runtime Network
   │
   ▼
Container Port

The browser must not directly access arbitrary container IP addresses.

35. Runtime Environment Variables

RUNIX controls system environment variables.

Example:

HOME=/home/runix
WORKSPACE=/workspace
TERM=xterm-256color

Runtime-specific variables may include:

NODE_ENV=development
PORT=5173

Do not automatically inject RUNIX server environment variables.

36. User Environment Variables

Future project configuration may allow:

DATABASE_URL
API_URL
PUBLIC_API_URL

These should be stored separately from general project metadata.

Sensitive values require encryption and restricted access.

They must not appear in:

logs
Git commits
API responses
frontend JavaScript
terminal history where avoidable
37. Runtime Startup Sequence

When the user clicks:

Start Runtime

the following process occurs:

1. Authenticate user
       ↓
2. Authorize project
       ↓
3. Load project metadata
       ↓
4. Load workspace metadata
       ↓
5. Select runtime type
       ↓
6. Select immutable runtime image
       ↓
7. Create runtime database record
       ↓
8. Create isolated container
       ↓
9. Mount workspace
       ↓
10. Apply resource limits
       ↓
11. Apply security configuration
       ↓
12. Configure network
       ↓
13. Start container
       ↓
14. Run health check
       ↓
15. Detect runtime readiness
       ↓
16. Mark runtime RUNNING
       ↓
17. Notify frontend
38. Runtime Startup Failure

If startup fails:

STARTING
    ↓
FAILED

Record:

failure_reason

Example:

ImagePullFailed
WorkspaceMountFailed
ContainerStartFailed
HealthCheckFailed
ResourceUnavailable

Do not expose raw infrastructure details to the user unless useful.

User-facing error:

The development runtime could not be started.
Please try again.

Technical logs contain the detailed reason.

39. Runtime Health Check

A runtime must be considered healthy only after the container is actually usable.

Possible checks:

container running
shell available
/workspace available
runtime executable available

For Node:

node --version

For Python:

python --version

A container being in Docker's running state does not automatically mean the development environment is ready.

40. Runtime Heartbeat

RUNIX should periodically check active runtimes.

Example:

every 15 seconds

The interval must be configurable.

Health data:

runtime_id
container_id
status
cpu_usage
memory_usage
storage_usage
last_health_check
41. Runtime Monitoring

Runtime metrics should include:

CPU usage
memory usage
memory limit
storage usage
process count
runtime age
last activity

Example frontend data:

{
  "cpu_percent": 32,
  "memory_used_mb": 418,
  "memory_limit_mb": 1024,
  "storage_used_mb": 842,
  "storage_limit_mb": 2048,
  "process_count": 18
}
42. Runtime Activity

Track runtime activity such as:

terminal input
command execution
file save
test execution
preview request
Git operation

Activity can be used to determine idle runtime state.

Do not store complete terminal contents simply to determine activity.

43. Idle Runtime

A runtime may be stopped automatically after a configurable idle period.

Initial default:

30 minutes

Before stopping, the frontend should display:

Your runtime has been idle.

It will stop automatically soon.

The user may continue activity to prevent shutdown where supported.

44. Runtime Stop Sequence
RUNNING
   ↓
STOPPING
   ↓
terminate user processes
   ↓
stop container
   ↓
release runtime resources
   ↓
update database
   ↓
STOPPED

Workspace data must remain persistent.

45. Runtime Restart

Restart:

RUNNING
   ↓
STOPPING
   ↓
STOPPED
   ↓
STARTING
   ↓
RUNNING

The workspace must remain intact.

The runtime container itself may be replaced.

RUNIX should not depend on container identity for project persistence.

46. Runtime Termination

Termination permanently removes the runtime container.

TERMINATING
    ↓
container removed
    ↓
network resources released
    ↓
temporary resources released
    ↓
TERMINATED

The workspace must remain unless the project itself is being deleted.

47. Runtime Cleanup

RUNIX must clean up:

stopped containers
orphaned containers
temporary networks
temporary volumes
abandoned terminal sessions
stale runtime records

Cleanup must be idempotent.

Running cleanup twice must not corrupt the system.

48. Orphaned Container Detection

Each RUNIX-managed container must contain identifying metadata.

Example labels:

runix.managed=true
runix.project_id=<uuid>
runix.runtime_id=<uuid>
runix.user_id=<uuid>

The Runtime Manager can use these labels to identify RUNIX containers.

49. Orphan Cleanup

On startup:

1. list RUNIX-managed containers
2. read runtime labels
3. compare with PostgreSQL
4. identify unknown containers
5. terminate unauthorized orphan containers
6. record cleanup event

Do not delete arbitrary Docker containers belonging to other applications.

Only containers carrying the RUNIX management label should be considered.

50. Runtime Reconciliation

The database and Docker are separate systems.

Therefore:

PostgreSQL state
       +
Docker state
       ↓
Reconciliation

Example:

Database:

runtime.status = running

Docker:

container = missing

RUNIX should transition:

running
   ↓
failed

or another explicitly defined recovery state.

51. Container Naming

Container names should be generated by RUNIX.

Example:

runix-runtime-<runtime_id>

Do not use arbitrary user project names directly as Docker container names.

Project names can contain characters unsuitable for infrastructure identifiers.

52. Container Labels

Every runtime container should have:

runix.managed=true
runix.runtime_id=<runtime UUID>
runix.project_id=<project UUID>
runix.user_id=<user UUID>
runix.runtime_type=node
runix.version=1

These labels support:

cleanup
debugging
monitoring
reconciliation
auditing
53. Runtime Manager API

The Runtime Manager should expose an internal abstraction.

Example:

class RuntimeManager:

    async def create_runtime(
        self,
        project_id,
        runtime_type,
    ):
        ...

    async def start_runtime(
        self,
        runtime_id,
    ):
        ...

    async def stop_runtime(
        self,
        runtime_id,
    ):
        ...

    async def restart_runtime(
        self,
        runtime_id,
    ):
        ...

    async def terminate_runtime(
        self,
        runtime_id,
    ):
        ...

    async def get_status(
        self,
        runtime_id,
    ):
        ...

    async def execute(
        self,
        runtime_id,
        command,
    ):
        ...

    async def create_terminal(
        self,
        runtime_id,
    ):
        ...

    async def get_metrics(
        self,
        runtime_id,
    ):
        ...
54. Docker Adapter

Docker-specific code should be isolated.

Recommended structure:

backend/app/runtime/
├── manager.py
├── models.py
├── policies.py
├── lifecycle.py
├── health.py
├── metrics.py
├── ports.py
└── docker/
    ├── client.py
    ├── containers.py
    ├── networks.py
    └── volumes.py

The rest of the application should depend on RuntimeManager, not directly on Docker SDK calls.

55. Runtime Policy

Every runtime creation request should be evaluated against a policy.

Example:

RuntimePolicy(
    cpu_limit=1,
    memory_limit_mb=1024,
    storage_limit_mb=2048,
    pids_limit=256,
    network_access=True,
    privileged=False,
    host_network=False,
    docker_socket=False,
)

The policy is server-controlled.

The browser cannot override it.

56. Runtime Creation Request

The frontend may request:

{
  "runtime_type": "node"
}

It must NOT be able to request:

{
  "runtime_type": "node",
  "memory": "64GB",
  "privileged": true,
  "host_network": true,
  "docker_socket": true
}

Infrastructure policy always wins.

57. Command Execution

Commands must execute only inside an active runtime.

Flow:

POST /commands
      ↓
authorize project
      ↓
find runtime
      ↓
verify RUNNING
      ↓
Runtime Manager
      ↓
container
      ↓
command

Never:

API endpoint
   ↓
subprocess.run(command)

on the RUNIX host.

58. Command Timeout

Every non-interactive command must have a timeout.

Initial default:

120 seconds

Examples:

npm test
npm run build
pytest
npm install

Long-running development servers should use a dedicated terminal/process mechanism rather than normal request-response execution.

59. Long-Running Processes

Examples:

npm run dev
uvicorn app:app --reload
npm start

These should not run through a normal HTTP request.

They should be attached to:

terminal
process manager
runtime session

The user should be able to:

start process
inspect output
stop process
restart process
60. Process Tracking

RUNIX should track important development processes.

Example:

{
  "pid": 42,
  "command": "npm run dev",
  "status": "running",
  "port": 5173
}

The process ID is valid only inside the runtime.

Do not expose host process IDs as if they were user-runtime process IDs.

61. Development Server Detection

RUNIX should detect common development server patterns.

Examples:

Vite
Next.js
React development server
Express
FastAPI
Flask

Detection sources:

stdout
stderr
listening sockets
configured ports
process metadata

Detection must not depend solely on parsing logs.

62. Preview Registration

When a port is detected:

runtime_id
project_id
port
protocol
process

is registered with the Preview subsystem.

Example:

{
  "project_id": "uuid",
  "runtime_id": "uuid",
  "port": 5173,
  "protocol": "http",
  "status": "ready"
}
63. Preview Protocol

Initial supported protocols:

http
https

WebSocket upgrade requests should be supported for development servers that require them.

Example:

Browser
   ↓
Preview Gateway
   ↓
HTTP/WebSocket
   ↓
Container Port
64. Runtime Logs

Runtime infrastructure logs should contain:

runtime_id
project_id
container_id
event
status
timestamp
error

Examples:

runtime.created
runtime.started
runtime.health_check
runtime.port_detected
runtime.stopped
runtime.failed
runtime.terminated

Never log:

password
token
API key
private key
secret environment variable
65. Runtime Failure Recovery

If a runtime unexpectedly exits:

RUNNING
   ↓
container exited
   ↓
health check detects failure
   ↓
runtime = FAILED

The frontend receives:

Runtime stopped unexpectedly.

The user can choose:

[ Restart Runtime ]

Automatic restart should not be enabled by default because repeated crashes may create resource loops.

66. Crash Loop Protection

If a runtime repeatedly fails:

start
 ↓
fail
 ↓
start
 ↓
fail
 ↓
start
 ↓
fail

RUNIX should stop automatic recovery attempts.

Example policy:

maximum automatic recovery attempts = 3

After the limit:

FAILED

and require user action.

67. Runtime Quotas

Future account-level quotas may include:

maximum concurrent runtimes
maximum runtime hours
maximum workspace storage
maximum terminal sessions
maximum deployments
maximum build time

The Runtime Engine should expose a policy layer so quotas can be added without redesigning container management.

68. Runtime Scheduling

V1 may use immediate runtime creation.

Future infrastructure may introduce:

queued
scheduled
starting
running

This allows RUNIX to support:

multiple runtime nodes
capacity management
autoscaling
regional execution
workload scheduling

Do not implement distributed orchestration until required.

69. V1 Infrastructure Model

Initial deployment model:

RUNIX API
   │
   ├── PostgreSQL
   ├── Redis
   ├── Runtime Manager
   │
   ▼
Docker Host
   │
   ├── Runtime A
   ├── Runtime B
   ├── Runtime C
   └── Runtime N

A single-node Docker runtime architecture is acceptable for the initial V1 implementation.

70. Future Runtime Cluster

Future architecture may evolve into:

RUNIX Control Plane
        │
        ▼
Runtime Scheduler
        │
        ├── Runtime Node A
        ├── Runtime Node B
        ├── Runtime Node C
        └── Runtime Node N

This is outside the initial V1 implementation.

The Runtime Manager abstraction should make this future migration possible.

71. Runtime Security Checklist

Every runtime must satisfy:

[ ] privileged = false
[ ] host network = false
[ ] Docker socket = not mounted
[ ] host root filesystem = not mounted
[ ] dedicated workspace only
[ ] CPU limit applied
[ ] memory limit applied
[ ] process limit applied
[ ] storage limit applied
[ ] runtime image pinned
[ ] isolated network
[ ] internal RUNIX services inaccessible
[ ] non-root user where practical
[ ] runtime labels applied
[ ] health check configured
[ ] cleanup mechanism available
72. Runtime Creation Checklist

Before creating a runtime:

[ ] user authenticated
[ ] project exists
[ ] user authorized
[ ] workspace exists
[ ] runtime type is supported
[ ] runtime quota available
[ ] image exists
[ ] policy resolved
[ ] resource limits resolved
[ ] network policy resolved
73. Runtime Shutdown Checklist

Before stopping:

[ ] mark runtime STOPPING
[ ] stop active terminal processes where appropriate
[ ] stop development processes
[ ] stop container
[ ] release temporary resources
[ ] update database
[ ] emit runtime status event

Workspace files must remain intact.

74. Runtime Termination Checklist

Before permanent termination:

[ ] verify runtime ownership
[ ] mark TERMINATING
[ ] stop container
[ ] remove container
[ ] remove runtime-specific network resources
[ ] remove temporary volumes
[ ] close terminal sessions
[ ] update database
[ ] emit audit event

Do not delete workspace storage unless the project deletion workflow explicitly requests it.

75. Audit Events

Runtime actions should generate audit events:

runtime.created
runtime.started
runtime.stopped
runtime.restarted
runtime.failed
runtime.terminated
runtime.cleanup
runtime.orphan_removed

Audit metadata may include:

{
  "runtime_id": "uuid",
  "runtime_type": "node"
}

Never include secrets.

76. Testing Requirements

The Runtime Engine must have automated tests for:

Lifecycle
create
start
stop
restart
terminate
Security
no privileged container
no host network
no Docker socket
no arbitrary host mount
Resources
CPU limit
memory limit
process limit
storage limit
Workspace
workspace mounted
workspace persists
cross-project isolation
Failure
container crash
health-check failure
missing container
orphan cleanup
Networking
port detection
preview registration
network isolation
77. Runtime Integration Test

A complete integration test should perform:

1. Create user
2. Create project
3. Create workspace
4. Start runtime
5. Wait for RUNNING
6. Open terminal
7. Execute pwd
8. Verify /workspace
9. Create file
10. Execute runtime command
11. Start development server
12. Detect port
13. Open preview
14. Stop runtime
15. Verify workspace persists
16. Start runtime again
17. Verify file still exists
18. Terminate runtime
19. Verify container removed
78. Acceptance Criteria

The Runtime Engine is considered V1-ready when:

RUNIX can create an isolated runtime.
The runtime uses an approved immutable image.
The runtime has CPU limits.
The runtime has memory limits.
The runtime has process limits.
The runtime has storage limits.
The runtime does not use privileged mode.
The runtime does not use host networking.
The runtime does not receive Docker socket access.
The runtime cannot access another project's workspace.
The workspace persists after runtime shutdown.
The runtime can be started and stopped.
The runtime can be restarted.
Runtime health can be detected.
Runtime failures are recorded.
Orphan containers can be detected.
Orphan containers can be safely removed.
Development ports can be detected.
Preview services can route to approved runtime ports.
Runtime resources are cleaned up.
Runtime state remains synchronized with PostgreSQL.
User commands never execute on the API host.
79. Absolute Security Rules

These rules are non-negotiable.

Rule 1

Never execute user code on the RUNIX API host.

Rule 2

Never mount the Docker socket into a user runtime.

Rule 3

Never run user containers with --privileged.

Rule 4

Never use host networking for user runtimes.

Rule 5

Never mount arbitrary host directories.

Rule 6

Never expose RUNIX database credentials to user runtimes.

Rule 7

Never trust client-provided Docker configuration.

Rule 8

Never trust client-provided host filesystem paths.

Rule 9

Never expose another project's workspace.

Rule 10

Never allow runtime resources to be unlimited.

Rule 11

Never treat a client-side runtime status as authoritative.

Rule 12

Always reconcile PostgreSQL runtime state with actual container state.

80. Final Architecture

The final V1 execution architecture is:

                         RUNIX
                          │
             ┌────────────┴────────────┐
             │                         │
        CONTROL PLANE             EXECUTION PLANE
             │                         │
        ┌────┴─────┐             ┌────┴──────┐
        │          │             │           │
      FastAPI   PostgreSQL    Runtime     Preview
        │          │          Manager      Gateway
        │          │             │           │
        │        Redis           │           │
        │                        │           │
        └──────────────┬─────────┘           │
                       │                     │
                       ▼                     ▼
                 Docker Runtime       Runtime Network
                       │
          ┌────────────┼────────────┐
          │            │            │
       Node 22      Python 3.12    MERN
          │            │            │
          └────────────┼────────────┘
                       │
                  /workspace
                       │
                 User Project