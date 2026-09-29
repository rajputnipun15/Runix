# RUNIX — Project Overview

## 1. Product Identity

**Product Name:** RUNIX

**Tagline:** Build. Run. Ship. Anywhere.

**Product Type:** Browser-based Cloud Development Platform / Cloud IDE

**Status:** Active Development

**Primary Goal:**

RUNIX provides developers with a complete software development environment
accessible through a web browser.

Users should be able to create or import a software project, edit source code,
execute commands, run tests, preview the application, interact with GitHub,
and manage the development environment without manually configuring a local
development environment.

---

# 2. Product Vision

RUNIX aims to make software development environment-independent.

A developer should be able to open a browser, sign into RUNIX, open a project,
and continue development from any supported device without reinstalling the
project's runtime, dependencies, editor, or command-line tools.

RUNIX separates the development interface from the execution environment.

The browser provides the development interface.

The cloud runtime provides the execution environment.

---

# 3. Core Principle

The system consists of two major planes:

## Control Plane

The control plane manages:

- users
- authentication
- projects
- workspaces
- runtime lifecycle
- GitHub integration
- jobs
- configuration
- permissions

## Execution Plane

The execution plane runs:

- user source code
- development servers
- build commands
- test commands
- terminal processes

User code MUST execute inside an isolated runtime environment.

User code MUST NOT execute directly on the API server host.

---

# 4. Core Product Modules

## 4.1 RUNIX Dashboard

The dashboard is the user's project management area.

Responsibilities:

- display projects
- create projects
- import GitHub repositories
- show recent activity
- show active runtimes
- display project status

---

## 4.2 RUNIX Workspace

The workspace is the primary development interface.

Responsibilities:

- file explorer
- code editor
- source control
- terminal
- preview
- test results
- logs
- AI coding agent

---

## 4.3 RUNIX Runtime

The runtime is an isolated execution environment associated with a project.

Responsibilities:

- execute commands
- run development servers
- execute tests
- provide filesystem access to the project
- expose application ports
- enforce resource limits

---

## 4.4 RUNIX Terminal

The terminal provides interactive shell access to the project's runtime.

The terminal communicates with the runtime through a WebSocket connection.

---

## 4.5 RUNIX Preview

The preview system allows users to access a running development server from
the browser.

Example:

Project runtime:

http://localhost:5173

RUNIX preview:

https://preview.runix.example/project-id/

The exact production domain is configurable.

---

## 4.6 RUNIX Git

RUNIX Git provides source-control functionality.

Initial functionality:

- repository import
- branch listing
- status
- commit
- push
- pull
- checkout

GitHub integration is implemented separately from generic Git operations.

---

## 4.7 RUNIX Agent

RUNIX Agent is the AI coding assistant.

The agent can:

- understand repository structure
- inspect source files
- search code
- explain code
- propose changes
- generate patches
- run tests
- inspect test failures

The agent does not receive unrestricted host access.

---

## 4.8 RUNIX Tests

The testing subsystem executes project tests inside the project's runtime.

It records:

- command
- status
- output
- exit code
- duration
- test results

---

## 4.9 RUNIX Deploy

Deployment is a later-stage feature.

The deployment system will eventually:

- build applications
- execute tests
- create deployment artifacts
- deploy applications
- provide deployment status
- provide deployment URLs

Deployment is NOT part of the initial V1 implementation.

---

# 5. Initial Supported Project Types

V1 templates:

1. React + Vite + TypeScript
2. Node.js + TypeScript
3. Python + FastAPI
4. MERN
5. Blank Docker environment

The RUNIX platform itself uses PostgreSQL.

The MERN template is only a user-project template and does not mean that RUNIX
uses MongoDB internally.

---

# 6. Target Users

Primary users:

- individual software developers
- students
- developers learning new technologies
- full-stack developers
- frontend developers
- backend developers
- developers working from multiple machines

V1 is optimized for individual users.

Team collaboration is a future capability.

---

# 7. V1 Scope

V1 MUST include:

- authentication
- dashboard
- project creation
- project listing
- project deletion
- project rename
- project templates
- workspace
- file explorer
- file creation
- file editing
- file deletion
- file rename
- directory creation
- Monaco editor
- file persistence
- Docker runtime
- runtime lifecycle
- terminal
- WebSocket terminal streaming
- live preview
- runtime status
- GitHub repository import
- basic Git operations
- tests
- logging
- health checks

---

# 8. V2 Scope

V2 includes:

- AI coding agent
- repository context
- code explanation
- code generation
- code modification
- diff review
- test generation
- AI debugging
- AI-assisted code review

---

# 9. V3 Scope

V3 includes:

- deployment
- collaborative editing
- teams
- role-based access
- usage limits
- billing
- advanced observability
- advanced runtime orchestration

---

# 10. Non-Goals

The initial implementation MUST NOT attempt to build:

- a complete replacement for GitHub
- a complete replacement for VS Code
- a general-purpose public cloud provider
- unrestricted server access
- unrestricted container networking
- a cryptocurrency/mining environment
- arbitrary host command execution
- Kubernetes-based multi-region orchestration in V1

The first objective is a reliable single-user cloud development environment.

---

# 11. Product Quality Standard

RUNIX must behave like a real production software product.

The system must not contain:

- fake production APIs
- hardcoded user data
- fake runtime states
- buttons without functionality
- placeholder backend responses presented as real functionality
- unprotected project endpoints
- direct host execution of user commands

Development mocks must be explicitly separated from production code.

---

# 12. Architecture Principle

The fundamental architecture is:

Browser
    |
    | HTTPS / WebSocket
    v
RUNIX API
    |
    +---- PostgreSQL
    |
    +---- Redis
    |
    +---- Runtime Manager
               |
               v
        Isolated Runtime
               |
               +---- Project Files
               +---- Processes
               +---- Development Server
               +---- Tests

This architecture must be preserved unless a documented architectural decision
changes it.