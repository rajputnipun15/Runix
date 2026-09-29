# RUNIX — Product Requirements Document

## 1. Product Objective

RUNIX provides a browser-based software development environment.

The product must allow an authenticated developer to:

1. create a project
2. select a development template
3. open a workspace
4. edit source code
5. save source code
6. start an isolated runtime
7. execute terminal commands
8. start a development server
9. preview the application
10. execute tests
11. inspect logs
12. connect/import GitHub repositories

---

# 2. Primary User Flow

Landing Page
    |
    v
Register / Login
    |
    v
Dashboard
    |
    +---- Create Project
    |
    +---- Import GitHub
    |
    v
Project Workspace
    |
    v
Start Runtime
    |
    +---- File Editor
    |
    +---- Terminal
    |
    +---- Preview
    |
    +---- Tests
    |
    +---- Git
    |
    v
Stop Runtime

---

# 3. Authentication Requirements

Users must be able to:

- register
- login
- logout
- retrieve current user
- maintain an authenticated session
- reset password

Authenticated users must only access resources they own or are authorized
to access.

Authentication failures must return appropriate HTTP status codes.

---

# 4. Dashboard Requirements

The dashboard must display:

- user's projects
- project names
- project templates
- runtime state
- last modified timestamp
- Git branch when available
- recent activity
- active runtime information

Dashboard actions:

- Create Project
- Import GitHub Repository
- Open Project
- Rename Project
- Delete Project

---

# 5. Project Requirements

A project contains:

- project metadata
- workspace
- runtime configuration
- optional Git repository
- test history
- jobs
- audit information

Project names must:

- be non-empty
- have a configurable maximum length
- reject unsupported control characters

Project IDs must be UUIDs.

---

# 6. Workspace Requirements

The workspace must provide:

- file tree
- code editor
- file tabs
- save functionality
- file creation
- directory creation
- rename
- delete
- search

The frontend must not assume that a file exists.

The filesystem returned by the backend is the source of truth.

---

# 7. Runtime Requirements

A runtime belongs to exactly one project.

A runtime has a lifecycle:

CREATING
STARTING
RUNNING
STOPPING
STOPPED
FAILED
TERMINATING
TERMINATED

Only valid state transitions may be performed.

Example:

STOPPED -> STARTING -> RUNNING

Invalid transitions must be rejected.

---

# 8. Terminal Requirements

The terminal must:

- connect to the project runtime
- stream input
- stream output
- support terminal resize
- support process termination
- handle runtime disconnects
- reconnect when appropriate

The terminal must not execute commands on the API host.

---

# 9. Preview Requirements

The preview system must:

1. identify the project's running application
2. identify an exposed development port
3. verify the service is reachable
4. generate a preview route
5. display the application in the workspace

If preview is unavailable, the UI must show:

- status
- reason where known
- retry action
- runtime logs action

---

# 10. GitHub Requirements

Users must be able to:

1. connect GitHub
2. view repositories they have authorized
3. select a repository
4. select a branch
5. import the repository
6. create a RUNIX project from the repository

Import must be asynchronous.

The UI must show:

IMPORTING
    |
    v
CLONING
    |
    v
INSTALLING
    |
    v
READY

or:

FAILED

with an actionable error.

---

# 11. Testing Requirements

Users can request a test run.

The test operation executes inside the project runtime.

A test run stores:

- test command
- start time
- finish time
- status
- exit code
- output

Possible states:

QUEUED
RUNNING
PASSED
FAILED
CANCELLED
TIMEOUT

---

# 12. Error Requirements

Every major operation must have:

- loading state
- success state
- failure state
- retry action where appropriate

The backend must return structured errors.

The frontend must not expose raw stack traces to normal users.

---

# 13. Performance Requirements

The frontend must not block while:

- runtime starts
- GitHub repository imports
- tests execute
- dependencies install
- builds execute

Long-running operations must use asynchronous jobs.

---

# 14. Security Requirements

The system must:

- authenticate requests
- authorize project access
- isolate user execution
- enforce runtime resource limits
- validate filesystem paths
- protect secrets
- protect GitHub credentials
- rate-limit sensitive endpoints
- audit sensitive operations

---

# 15. V1 Acceptance Criteria

V1 is considered functional when a new user can:

1. register
2. login
3. create a React project
4. open the project
5. see the file tree
6. edit a file
7. save it
8. start the runtime
9. open the terminal
10. execute a command
11. start the development server
12. view the live preview
13. stop the runtime
14. logout
15. return later
16. reopen the project
17. repeat the workflow successfully