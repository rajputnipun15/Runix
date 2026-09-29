# RUNIX WebSocket Specification

## 1. Purpose

This document defines the WebSocket communication layer used by RUNIX for real-time developer interactions.

The primary V1 WebSocket feature is the interactive terminal.

WebSockets may later support:

- terminal sessions
- runtime status updates
- command output
- build logs
- test output
- deployment logs
- AI agent progress
- collaborative editing
- live preview status

The V1 implementation must prioritize a reliable interactive terminal.

---

# 2. Architecture

RUNIX terminal communication follows this architecture:

```text
Browser
   │
   │ WebSocket
   ▼
RUNIX API
   │
   │ authenticated connection
   ▼
Terminal Service
   │
   │ runtime command
   ▼
Runtime Manager
   │
   ▼
Isolated Runtime Container
   │
   ▼
PTY / Shell

The browser must NEVER connect directly to Docker.

The browser must NEVER receive Docker socket access.

The browser must NEVER communicate directly with the host operating system.

3. WebSocket Endpoint

Primary endpoint:

/ws/projects/{project_id}/terminal

Example:

ws://localhost:8000/ws/projects/PROJECT_ID/terminal

Production:

wss://api.RUNIX_DOMAIN/ws/projects/PROJECT_ID/terminal

The production domain must be configurable.

Never hard-code the production domain inside the frontend.

4. Connection Requirements

A WebSocket connection requires:

authenticated user
valid project ID
project access authorization
active or startable runtime
valid WebSocket handshake

Connection sequence:

Browser
   │
   ├── authenticate
   │
   ├── connect WebSocket
   │
   ▼
RUNIX API
   │
   ├── validate session
   ├── validate project
   ├── validate permissions
   ├── validate runtime
   │
   ▼
Terminal Session
   │
   ▼
PTY

If authorization fails:

403 Forbidden

If authentication is missing:

401 Unauthorized

If the runtime is unavailable:

RUNTIME_NOT_AVAILABLE
5. Authentication

WebSocket authentication must use the same authenticated session mechanism as the REST API.

Preferred browser architecture:

Browser
   │
   │ secure authenticated session
   ▼
RUNIX WebSocket

Do not put long-lived secrets directly into WebSocket URLs.

Avoid:

/ws/projects/123/terminal?token=VERY_LONG_SECRET

Query-string authentication can expose credentials through logs, browser history, proxies, or monitoring systems.

Use secure authenticated session mechanisms instead.

6. Authorization

After establishing the connection, the server must verify:

current_user
     ↓
project_id
     ↓
project exists
     ↓
user owns project OR has membership
     ↓
role allows terminal access

Recommended V1 terminal permissions:

owner  → allowed
admin  → allowed
member → allowed
viewer → denied

Authorization must be performed on every new WebSocket connection.

Do not assume that an authenticated user can access every project.

7. Terminal Session

Every WebSocket terminal connection maps to a RUNIX terminal session.

Database entity:

terminal_sessions

Example:

TerminalSession
├── id
├── runtime_id
├── user_id
├── status
├── shell
├── created_at
└── closed_at

The WebSocket connection ID and database terminal session ID should be correlated in logs.

8. PTY Requirement

RUNIX should use a pseudo-terminal (PTY) rather than a simple command-execution API for interactive terminals.

A PTY provides:

interactive shell behavior
stdin
stdout
stderr
terminal resizing
shell prompts
interactive programs
signal handling
Ctrl+C
Ctrl+D
terminal color sequences

The terminal should behave similarly to a normal developer terminal.

9. Shell

The runtime image should provide an approved shell.

Preferred:

/bin/bash

Fallback:

/bin/sh

The actual shell must be determined by the runtime image.

The browser must not be allowed to specify an arbitrary host shell.

Do not accept:

{
  "shell": "/host/custom/shell"
}

The runtime manager chooses the shell.

10. Client → Server Messages

The browser may send the following message types:

input
resize
ping
close

Message format:

{
  "type": "input",
  "data": "npm run dev\n"
}
11. Input Message

Used for keyboard input.

Example:

{
  "type": "input",
  "data": "ls -la\n"
}

The server forwards the input to the PTY attached to the isolated runtime.

The server must NOT execute the string on the API host.

Flow:

xterm.js
   ↓
WebSocket
   ↓
RUNIX Terminal Service
   ↓
PTY
   ↓
Container
12. Special Keyboard Input

Terminal control characters must be preserved.

Examples:

Ctrl+C → interrupt
Ctrl+D → EOF
Ctrl+L → clear
Arrow keys → terminal escape sequences
Tab → shell completion
Backspace → terminal input

The frontend should send the terminal's raw input sequence.

Do not implement custom command parsing in the browser.

13. Resize Message

When the terminal panel changes size:

{
  "type": "resize",
  "cols": 120,
  "rows": 32
}

The server forwards the resize operation to the PTY.

Example:

Browser
   │
   ├── cols=120
   ├── rows=32
   ▼
WebSocket
   ▼
PTY.resize(120, 32)

Both values must be validated.

Recommended constraints:

minimum columns: 20
maximum columns: 500

minimum rows: 5
maximum rows: 200
14. Ping Message

Client:

{
  "type": "ping"
}

Server:

{
  "type": "pong",
  "timestamp": "2026-09-28T10:00:00Z"
}

WebSocket infrastructure may also use protocol-level ping/pong frames.

Application-level ping is optional.

15. Close Message

Client:

{
  "type": "close"
}

The server should:

close the PTY session
update terminal session status
release session resources
close WebSocket

The runtime itself should NOT automatically stop merely because one terminal closes.

A runtime can remain active for the project's development server.

16. Server → Client Messages

The server may send:

connected
output
status
error
exit
pong
runtime_status
17. Connected Message

Immediately after successful connection:

{
  "type": "connected",
  "terminal_session_id": "uuid",
  "runtime_id": "uuid",
  "shell": "/bin/bash"
}

Example:

{
  "type": "connected",
  "terminal_session_id": "0dbf...",
  "runtime_id": "9ca2...",
  "shell": "/bin/bash"
}
18. Output Message

Terminal output:

{
  "type": "output",
  "data": "hello world\r\n"
}

Output must preserve terminal escape sequences where required.

For example:

ANSI colors
cursor movement
clear-screen commands
progress bars

The frontend terminal renderer is responsible for interpreting these sequences.

xterm.js should be used for rendering.

19. Large Output

Terminal output can become extremely large.

RUNIX must NOT buffer unlimited terminal output in memory.

Implement output backpressure.

Recommended flow:

PTY
 ↓
Output Buffer
 ↓
WebSocket
 ↓
Browser

If the browser cannot consume output fast enough:

apply backpressure
limit buffered data
optionally truncate old buffered output
keep the terminal connection alive when possible

Never allow terminal output to cause unbounded memory growth.

20. Output Chunk Size

The server should send terminal output in reasonable chunks.

Example configuration:

WEBSOCKET_OUTPUT_CHUNK_SIZE=16384

16 KB is a reasonable initial value.

This is configurable.

Do not create one WebSocket message for every individual byte.

21. Runtime Status Message

The server may push runtime state changes:

{
  "type": "runtime_status",
  "status": "running"
}

Possible states:

creating
starting
running
stopping
stopped
failed
terminating
terminated

This allows the frontend to update runtime indicators without polling continuously.

22. Error Message

Example:

{
  "type": "error",
  "code": "RUNTIME_NOT_AVAILABLE",
  "message": "The project runtime is not available."
}

Common errors:

AUTHENTICATION_REQUIRED
PROJECT_NOT_FOUND
PROJECT_ACCESS_DENIED
RUNTIME_NOT_AVAILABLE
RUNTIME_STARTING
TERMINAL_CREATION_FAILED
PTY_ERROR
WEBSOCKET_RATE_LIMITED
WEBSOCKET_MESSAGE_INVALID
WEBSOCKET_MESSAGE_TOO_LARGE
INTERNAL_ERROR

Do not expose internal stack traces to the browser.

23. Exit Message

When the shell process exits:

{
  "type": "exit",
  "exit_code": 0
}

Example failure:

{
  "type": "exit",
  "exit_code": 1
}

The server should then close or transition the terminal session appropriately.

The runtime itself may remain running.

24. Message Validation

Every incoming message must be validated.

Invalid:

{
  "type": "unknown",
  "something": "malicious"
}

Response:

{
  "type": "error",
  "code": "WEBSOCKET_MESSAGE_INVALID",
  "message": "Unsupported message type."
}

Never pass arbitrary JSON fields to the runtime.

25. Message Size Limits

Recommended initial limits:

maximum WebSocket message: 64 KB
maximum terminal input message: 16 KB
maximum resize message: 1 KB

These values must be configurable.

Very large terminal input should be rejected.

Example:

WEBSOCKET_MAX_MESSAGE_BYTES=65536
TERMINAL_MAX_INPUT_BYTES=16384
26. Connection Limits

Limit the number of simultaneous terminal connections per user/project.

Initial policy:

per user:
    maximum terminal connections = 5

per project:
    maximum active terminal connections = 3

These are configurable.

When exceeded:

429 Too Many Connections

or WebSocket close code:

1008
27. Idle Connections

Idle WebSocket connections should be monitored.

Example configuration:

TERMINAL_IDLE_TIMEOUT_SECONDS=1800

After the configured period:

notify the client
close the terminal session
release PTY resources

Closing an idle terminal does NOT necessarily stop the runtime.

28. Runtime Disconnect Handling

If the runtime crashes:

Runtime
   X
   ↓
Terminal Service
   ↓
WebSocket
   ↓
Browser

Send:

{
  "type": "runtime_status",
  "status": "failed"
}

Then:

{
  "type": "error",
  "code": "RUNTIME_DISCONNECTED",
  "message": "The development runtime has stopped."
}

Finally:

{
  "type": "exit",
  "exit_code": 1
}

The frontend should display an actionable runtime state.

29. Reconnection

The frontend should automatically attempt reconnection when a temporary network interruption occurs.

Recommended strategy:

attempt 1 → 1 second
attempt 2 → 2 seconds
attempt 3 → 4 seconds
attempt 4 → 8 seconds
attempt 5 → 16 seconds

Maximum retry delay:

30 seconds

Use exponential backoff with jitter.

Do not reconnect infinitely without informing the user.

30. Reconnection Behavior

After reconnecting:

Browser
   ↓
Authenticate
   ↓
Reconnect WebSocket
   ↓
Validate project
   ↓
Validate runtime
   ↓
Create new terminal session

A terminal PTY should not be assumed to survive a disconnected browser session unless the backend explicitly implements persistent PTY sessions.

V1 may create a new PTY after reconnection.

31. Terminal State Model
CONNECTING
    ↓
CONNECTED
    ↓
ACTIVE
    ↓
CLOSING
    ↓
CLOSED

Failure:

CONNECTING
    ↓
FAILED

Runtime failure:

ACTIVE
    ↓
RUNTIME_DISCONNECTED
    ↓
CLOSED
32. Server Implementation

Recommended backend structure:

backend/app/
├── websocket/
│   ├── __init__.py
│   ├── terminal.py
│   ├── messages.py
│   ├── connection_manager.py
│   └── authentication.py
│
├── services/
│   └── terminal_service.py
│
└── runtime/
    └── pty.py
33. Terminal Connection Manager

The connection manager tracks active WebSocket sessions.

Conceptual structure:

class TerminalConnectionManager:

    async def connect(
        self,
        websocket,
        terminal_session_id,
    ):
        ...

    async def disconnect(
        self,
        terminal_session_id,
    ):
        ...

    async def send_output(
        self,
        terminal_session_id,
        data,
    ):
        ...

    async def send_message(
        self,
        terminal_session_id,
        message,
    ):
        ...

The connection manager should not contain Docker-specific logic.

34. Terminal Service

The terminal service coordinates:

WebSocket
PTY
Runtime Manager
Database

Responsibilities:

create terminal session
validate runtime
create PTY
attach PTY to container
forward input
forward output
handle resize
handle disconnect
close PTY
update database state
35. PTY Service

The PTY service is responsible only for terminal process interaction.

Conceptual interface:

class PTYSession:

    async def start(self):
        ...

    async def write(self, data: bytes):
        ...

    async def resize(
        self,
        cols: int,
        rows: int,
    ):
        ...

    async def read(self):
        ...

    async def close(self):
        ...

The PTY implementation must operate against the isolated runtime.

It must not spawn arbitrary processes on the API host.

36. Runtime Manager Boundary

The terminal service must communicate with the Runtime Manager.

Preferred:

Terminal Service
       │
       ▼
Runtime Manager
       │
       ▼
Container

Not:

Terminal Service
       │
       ▼
Docker SDK everywhere

Only the Runtime Manager should own container lifecycle operations.

This prevents Docker logic from spreading throughout the backend.

37. Terminal Environment

The runtime should provide a controlled environment.

Example:

HOME=/home/runix
WORKSPACE=/workspace
TERM=xterm-256color
LANG=C.UTF-8

Environment values should be controlled by RUNIX.

Never expose server secrets through environment variables inside user containers.

Do not automatically pass:

DATABASE_URL
AWS_SECRET_ACCESS_KEY
GITHUB_TOKEN
RUNIX_INTERNAL_SECRET
POSTGRES_PASSWORD
REDIS_URL

into user runtimes.

38. Working Directory

The default terminal working directory should be:

/workspace

Example:

runix@runtime:/workspace$

The workspace directory must map to the project's isolated workspace storage.

39. Terminal Environment Isolation

User runtime environment variables should be project-scoped.

Example:

NODE_ENV=development
PORT=5173

Project environment variables may be supported later.

Sensitive project secrets must use a dedicated secret mechanism.

Do not place production credentials into .env files automatically.

40. Terminal Security

The terminal must not allow users to access:

host filesystem
Docker socket
host process namespace
host network namespace
cloud provider credentials
RUNIX internal credentials
other users' workspaces
RUNIX PostgreSQL directly
RUNIX Redis directly

The runtime is an isolated development environment.

41. WebSocket Security

Production WebSocket connections must use:

WSS

Never:

ws://

over an insecure production network.

The reverse proxy must correctly forward:

Upgrade: websocket
Connection: Upgrade

headers.

42. Origin Validation

The server should validate WebSocket origins.

Allowed origins must come from configuration.

Example:

RUNIX_ALLOWED_ORIGINS=https://runix.example.com

Do not use:

Access-Control-Allow-Origin: *

for authenticated production WebSocket connections.

43. Rate Limiting

Apply rate limits to:

connection creation
terminal input
reconnect attempts
WebSocket message frequency

Recommended initial input limit:

TERMINAL_INPUT_RATE_LIMIT=100 messages/second

This should be configurable.

The limit must be high enough for normal keyboard usage but prevent abusive automated input.

44. Backpressure

The system must handle:

fast producer
      ↓
slow consumer

Example:

npm build
   ↓
thousands of output lines
   ↓
PTY
   ↓
WebSocket
   ↓
slow browser

The server must not allocate unlimited memory.

Use:

bounded queues
output chunking
backpressure
queue size limits
connection termination for abusive streams
45. Logging

Log connection lifecycle events.

Example:

terminal.websocket.connected
terminal.websocket.disconnected
terminal.websocket.error
terminal.session.created
terminal.session.closed
terminal.runtime.disconnected

Log metadata:

request_id
user_id
project_id
runtime_id
terminal_session_id
timestamp
event

Do NOT log:

terminal input
terminal output
passwords
tokens
secrets
private keys

Terminal contents can contain sensitive information.

46. Metrics

Recommended metrics:

runix_websocket_connections_active
runix_websocket_connections_total
runix_websocket_connection_errors_total
runix_terminal_sessions_active
runix_terminal_sessions_total
runix_terminal_input_bytes_total
runix_terminal_output_bytes_total
runix_terminal_errors_total
runix_terminal_session_duration_seconds

These metrics should not contain user source code.

47. Frontend Integration

Use xterm.js.

Recommended frontend structure:

frontend/
└── components/
    └── terminal/
        ├── TerminalPanel.tsx
        ├── TerminalConnection.ts
        ├── TerminalToolbar.tsx
        ├── TerminalStatus.tsx
        └── useTerminal.ts
48. xterm.js Lifecycle
Component Mount
      ↓
Create xterm instance
      ↓
Open WebSocket
      ↓
Receive connected
      ↓
Attach output stream
      ↓
Forward keyboard input
      ↓
Forward resize
      ↓
Unmount
      ↓
Close WebSocket
      ↓
Dispose xterm

The terminal must clean up all listeners.

49. Frontend Terminal States

The UI should display:

Connecting...
Connected
Runtime starting...
Runtime stopped
Disconnected
Reconnecting...
Connection failed

Example toolbar:

Terminal                     ● Connected
────────────────────────────────────────
$ npm run dev
50. Runtime Starting

If the user opens the terminal while the runtime is starting:

Runtime starting...

The frontend should wait for the runtime status.

Do not create a terminal against a nonexistent runtime.

51. Runtime Stopped

If the runtime is stopped:

Runtime stopped

Start the runtime to open a terminal.

Provide:

[ Start Runtime ]

The button triggers:

POST /projects/{project_id}/runtime/start

Then the frontend waits for runtime readiness.

52. Terminal Reconnection UI

Example:

Connection lost.

Reconnecting in 4 seconds...

[ Reconnect Now ]

After maximum retry attempts:

Terminal disconnected.

[ Reconnect ]
53. WebSocket Error Codes

Application-level error codes:

AUTHENTICATION_REQUIRED
PROJECT_NOT_FOUND
PROJECT_ACCESS_DENIED
RUNTIME_NOT_FOUND
RUNTIME_NOT_READY
TERMINAL_LIMIT_REACHED
TERMINAL_CREATION_FAILED
PTY_CREATION_FAILED
MESSAGE_INVALID
MESSAGE_TOO_LARGE
RATE_LIMITED
RUNTIME_DISCONNECTED
INTERNAL_ERROR
54. WebSocket Close Codes

Use standard WebSocket close codes where possible.

Examples:

1000 Normal Closure
1001 Going Away
1008 Policy Violation
1011 Internal Error

RUNIX-specific application errors should be communicated through structured error messages before closing where appropriate.

55. Protocol Example

Complete interaction:

Browser
   │
   │ CONNECT /ws/projects/abc/terminal
   ▼
RUNIX API
   │
   ├── authenticate user
   ├── authorize project
   ├── verify runtime
   ├── create terminal session
   ├── create PTY
   │
   ▼
Browser
   │
   │ ← connected
   │
   │ input: "pwd\n"
   ▼
RUNIX
   │
   ▼
PTY
   │
   ▼
Container
   │
   │ output: "/workspace\n"
   ▼
RUNIX
   │
   ▼
Browser
   │
   ▼
xterm.js
56. Complete Message Examples
Client → Server
{
  "type": "input",
  "data": "npm install\n"
}
{
  "type": "resize",
  "cols": 140,
  "rows": 40
}
{
  "type": "ping"
}
Server → Client
{
  "type": "connected",
  "terminal_session_id": "8f0...",
  "runtime_id": "2ab...",
  "shell": "/bin/bash"
}
{
  "type": "output",
  "data": "\u001b[32mRUNIX\u001b[0m\n"
}
{
  "type": "runtime_status",
  "status": "running"
}
{
  "type": "exit",
  "exit_code": 0
}
57. V1 Scope

V1 WebSocket functionality must support:

authenticated terminal connections
project authorization
isolated runtime terminal
interactive PTY
keyboard input
terminal output
terminal resize
Ctrl+C
Ctrl+D
runtime disconnect handling
reconnection
connection limits
output backpressure
structured errors
terminal session tracking
WebSocket logging
xterm.js integration
58. V1 Non-Goals

Do not implement initially:

collaborative terminal sharing
terminal recording
terminal playback
public terminal URLs
terminal sharing with anonymous users
arbitrary host command execution
persistent terminal sessions across runtime destruction
unrestricted port forwarding
peer-to-peer WebSocket connections

These can be evaluated later.

59. Acceptance Criteria

The implementation is complete when:

An authenticated user can open a RUNIX project.
The project runtime can be started.
The user can open the terminal.
A PTY is created inside the isolated runtime.
The terminal displays a shell prompt.
pwd executes inside /workspace.
ls displays project files.
echo hello returns output.
Ctrl+C interrupts a running command.
terminal resize works.
npm run dev can start a development server inside the runtime.
terminal output streams without refreshing the page.
runtime failure is reflected in the terminal UI.
unauthorized users cannot connect.
terminal connections cannot access the host filesystem.
terminal input is never executed on the API host.
large output does not cause unbounded server memory usage.
disconnect/reconnect works.
terminal sessions are recorded in PostgreSQL.
secrets are not written to terminal logs.
60. Core Security Rule

The most important rule in this specification is:

A RUNIX WebSocket terminal is an interface to an isolated development runtime, never an interface to the RUNIX host.

Architecture must always remain:

Browser
   ↓
Authenticated WebSocket
   ↓
RUNIX Terminal Service
   ↓
Runtime Manager
   ↓
Isolated Container
   ↓
PTY

Never:

Browser
   ↓
WebSocket
   ↓
Host Shell

### After this

Your documentation sequence is now:

```text
05-DATABASE-SCHEMA.md       ✅
06-API-SPECIFICATION.md     ✅
07-WEBSOCKET-SPECIFICATION.md  ← current
08-RUNTIME-ENGINE.md         ← next
09-WORKSPACE-FILESYSTEM.md
10-GITHUB-INTEGRATION.md
11-AI-AGENT-SPECIFICATION.md
12-SECURITY-ARCHITECTURE.md
...