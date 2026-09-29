# RUNIX — Functional Requirements

## FR-001 Authentication

The system shall authenticate users before allowing access to private projects.

### Acceptance

Unauthenticated requests to protected resources return:

HTTP 401 Unauthorized

---

## FR-002 Authorization

The system shall verify that the authenticated user owns or has permission
to access the requested project.

Unauthorized access returns:

HTTP 403 Forbidden

The system must not reveal whether a private project exists when the requester
is not authorized.

---

## FR-003 Create Project

Input:

- name
- template
- visibility

Process:

1. validate request
2. create project
3. create workspace
4. initialize template
5. return project

---

## FR-004 File Read

Input:

- project ID
- relative workspace path

Validation:

- authenticated user
- project authorization
- path normalization
- workspace boundary

Reject:

- absolute paths
- `..`
- null bytes
- paths outside workspace

---

## FR-005 File Write

Before writing:

1. authenticate
2. authorize
3. normalize path
4. validate size
5. validate workspace boundary
6. write atomically where practical

---

## FR-006 Runtime Creation

A runtime may be created only for an existing authorized project.

Runtime creation must:

- select approved runtime image
- configure resource limits
- mount only the project workspace
- apply network policy
- generate runtime metadata
- return runtime status

---

## FR-007 Command Execution

A command request must contain:

- runtime ID
- command input

The command must execute inside the runtime.

The host must never execute the command directly.

---

## FR-008 Runtime Cleanup

A runtime must be stopped when:

- user explicitly stops it
- runtime fails
- timeout occurs
- project is deleted
- cleanup policy triggers

---

## FR-009 Preview

A preview is available only when:

- runtime is RUNNING
- application process is running
- port is detected/configured
- proxy health check succeeds

---

## FR-010 GitHub Import

Import is an asynchronous job.

The API returns a job ID.

Frontend polls or subscribes to job status.

---

## FR-011 Test Execution

Tests must execute in the project's runtime.

Test output must be persisted.

---

## FR-012 Audit

Audit events must be generated for:

- login
- logout
- project creation
- project deletion
- runtime start
- runtime stop
- GitHub connection
- repository import
- Git operations
- deployment operations
- security events