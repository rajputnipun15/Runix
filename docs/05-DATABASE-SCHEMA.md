# RUNIX Database Schema

## 1. Purpose

This document defines the PostgreSQL data model for RUNIX.

PostgreSQL stores RUNIX control-plane metadata:

- users
- authentication sessions
- projects
- project memberships
- workspaces
- runtime metadata
- terminal sessions
- command executions
- GitHub repositories
- Git branches
- background jobs
- test runs
- deployments
- audit logs

PostgreSQL is NOT the primary storage location for every project source file.

Project source files are stored in the workspace filesystem associated with a RUNIX project.

---

# 2. Database

## Engine

PostgreSQL 16+

## Required Extensions

RUNIX should initially use:

- pgcrypto

UUIDs should be generated using PostgreSQL-compatible UUID generation.

Example:

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;


Naming Conventions

Database:

runix

Schema:

public

Tables:

snake_case

Primary keys:

id UUID

Foreign keys:

<entity>_id UUID

Timestamps:

created_at TIMESTAMPTZ
updated_at TIMESTAMPTZ

All timestamps are stored in UTC.


Entity Relationships:

User
 │
 ├── Session
 │
 ├── Project
 │    │
 │    ├── ProjectMember
 │    │
 │    ├── Workspace
 │    │
 │    ├── Runtime
 │    │     │
 │    │     ├── TerminalSession
 │    │     └── CommandExecution
 │    │
 │    ├── GitRepository
 │    │     └── GitBranch
 │    │
 │    ├── Job
 │    │
 │    ├── TestRun
 │    │
 │    ├── Deployment
 │    │
 │    └── AuditLog
 │
 └── AuditLog


 users

Stores RUNIX user accounts.

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    email VARCHAR(320) NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,

    display_name VARCHAR(100) NOT NULL,

    avatar_url TEXT,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    email_verified BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
Constraints
Email must be unique.
Email should be normalized to lowercase before persistence.
Passwords must never be stored in plaintext.
Password hashing must use Argon2id or an equivalent modern password hashing algorithm.
is_active=false prevents authentication.
Avatar URLs must not contain private authentication tokens.

sessions

Stores authenticated sessions.

CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    refresh_token_hash TEXT NOT NULL,

    user_agent TEXT,

    ip_address INET,

    expires_at TIMESTAMPTZ NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    revoked_at TIMESTAMPTZ
);
Indexes
CREATE INDEX idx_sessions_user_id
ON sessions(user_id);

CREATE INDEX idx_sessions_expires_at
ON sessions(expires_at);

Refresh tokens must be hashed before being stored.

RUNIX must never store raw refresh tokens in PostgreSQL.


projects

Represents a user-owned development project.

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    owner_id UUID NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    name VARCHAR(100) NOT NULL,

    slug VARCHAR(120) NOT NULL,

    description TEXT,

    template VARCHAR(50) NOT NULL,

    visibility VARCHAR(20) NOT NULL DEFAULT 'private',

    status VARCHAR(30) NOT NULL DEFAULT 'active',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT projects_owner_slug_unique
        UNIQUE(owner_id, slug),

    CONSTRAINT projects_visibility_check
        CHECK (visibility IN ('private', 'public')),

    CONSTRAINT projects_status_check
        CHECK (status IN ('active', 'archived', 'deleted'))
);
Supported templates

Initial values:

react-vite-ts
node-ts
python-fastapi
mern
blank-docker

The backend must validate template names.

Frontend-provided arbitrary template identifiers must not be trusted.

8. project_members

Allows future collaboration without changing the core project model.

CREATE TABLE project_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL
        REFERENCES projects(id)
        ON DELETE CASCADE,

    user_id UUID NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    role VARCHAR(30) NOT NULL DEFAULT 'member',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE(project_id, user_id),

    CONSTRAINT project_member_role_check
        CHECK (role IN ('owner', 'admin', 'member', 'viewer'))
);

For V1, projects may remain single-user while this schema is retained for future collaboration.

9. workspaces

Represents the persistent filesystem associated with a project.

CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL UNIQUE
        REFERENCES projects(id)
        ON DELETE CASCADE,

    storage_path TEXT NOT NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'ready',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT workspace_status_check
        CHECK (
            status IN (
                'creating',
                'ready',
                'locked',
                'error',
                'deleted'
            )
        )
);

storage_path must be controlled by the backend.

The client must never provide an arbitrary host filesystem path.

10. project_file_metadata

Optional metadata for files stored in the workspace filesystem.

CREATE TABLE project_file_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL
        REFERENCES projects(id)
        ON DELETE CASCADE,

    path TEXT NOT NULL,

    size_bytes BIGINT NOT NULL DEFAULT 0,

    content_hash VARCHAR(128),

    mime_type VARCHAR(255),

    is_directory BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE(project_id, path)
);

This table is metadata only.

The actual file content remains in workspace storage.

11. runtimes

Stores metadata for isolated execution environments.

CREATE TABLE runtimes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL
        REFERENCES projects(id)
        ON DELETE CASCADE,

    container_id VARCHAR(255),

    runtime_type VARCHAR(50) NOT NULL,

    image VARCHAR(255) NOT NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'creating',

    cpu_limit DECIMAL(5,2) NOT NULL DEFAULT 1.00,

    memory_limit_mb INTEGER NOT NULL DEFAULT 1024,

    storage_limit_mb INTEGER NOT NULL DEFAULT 2048,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    started_at TIMESTAMPTZ,

    stopped_at TIMESTAMPTZ,

    terminated_at TIMESTAMPTZ,

    last_health_check_at TIMESTAMPTZ,

    failure_reason TEXT,

    CONSTRAINT runtime_status_check
        CHECK (
            status IN (
                'creating',
                'starting',
                'running',
                'stopping',
                'stopped',
                'failed',
                'terminating',
                'terminated'
            )
        )
);
Runtime rules

A runtime belongs to exactly one project.

A project may have:

zero runtimes
one active runtime
historical terminated runtimes

The runtime manager is responsible for synchronizing database state with actual container state.

12. terminal_sessions

Tracks interactive terminal connections.

CREATE TABLE terminal_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    runtime_id UUID NOT NULL
        REFERENCES runtimes(id)
        ON DELETE CASCADE,

    user_id UUID NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    status VARCHAR(30) NOT NULL DEFAULT 'active',

    shell VARCHAR(100) NOT NULL DEFAULT '/bin/bash',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    closed_at TIMESTAMPTZ,

    CONSTRAINT terminal_session_status_check
        CHECK (
            status IN (
                'active',
                'closed',
                'failed'
            )
        )
);

Terminal output should NOT be stored permanently in PostgreSQL by default.

Large terminal streams should remain transient.

13. command_executions

Tracks commands executed through RUNIX.

CREATE TABLE command_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    runtime_id UUID NOT NULL
        REFERENCES runtimes(id)
        ON DELETE CASCADE,

    user_id UUID NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    command TEXT NOT NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'queued',

    exit_code INTEGER,

    started_at TIMESTAMPTZ,

    finished_at TIMESTAMPTZ,

    timeout_seconds INTEGER,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT command_execution_status_check
        CHECK (
            status IN (
                'queued',
                'running',
                'completed',
                'failed',
                'timeout',
                'cancelled'
            )
        )
);

Command output should be streamed to the client.

Large output must not be stored indefinitely.

14. git_repositories

Stores Git provider metadata.

CREATE TABLE git_repositories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL UNIQUE
        REFERENCES projects(id)
        ON DELETE CASCADE,

    provider VARCHAR(30) NOT NULL,

    repository_id VARCHAR(255) NOT NULL,

    repository_url TEXT NOT NULL,

    owner_name VARCHAR(255),

    repository_name VARCHAR(255),

    default_branch VARCHAR(255) NOT NULL DEFAULT 'main',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT git_provider_check
        CHECK (provider IN ('github'))
);

The actual Git repository exists inside the workspace.

This table stores provider metadata.

15. git_branches

Stores known Git branch metadata.

CREATE TABLE git_branches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    repository_id UUID NOT NULL
        REFERENCES git_repositories(id)
        ON DELETE CASCADE,

    name VARCHAR(255) NOT NULL,

    is_default BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE(repository_id, name)
);

Git itself remains the source of truth for repository history.

16. jobs

Stores asynchronous backend jobs.

CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID
        REFERENCES projects(id)
        ON DELETE CASCADE,

    user_id UUID
        REFERENCES users(id)
        ON DELETE SET NULL,

    type VARCHAR(100) NOT NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'queued',

    payload JSONB NOT NULL DEFAULT '{}'::jsonb,

    result JSONB,

    error TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    started_at TIMESTAMPTZ,

    completed_at TIMESTAMPTZ,

    CONSTRAINT job_status_check
        CHECK (
            status IN (
                'queued',
                'running',
                'completed',
                'failed',
                'cancelled'
            )
        )
);

Examples:

workspace.create
github.import
runtime.start
runtime.stop
tests.run
deployment.build
ai.agent_task

Redis may be used for queue coordination.

PostgreSQL remains the persistent source of truth for job state.

17. test_runs

Stores test execution metadata.

CREATE TABLE test_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL
        REFERENCES projects(id)
        ON DELETE CASCADE,

    runtime_id UUID
        REFERENCES runtimes(id)
        ON DELETE SET NULL,

    user_id UUID
        REFERENCES users(id)
        ON DELETE SET NULL,

    command TEXT NOT NULL,

    framework VARCHAR(100),

    status VARCHAR(30) NOT NULL DEFAULT 'queued',

    total_tests INTEGER DEFAULT 0,

    passed_tests INTEGER DEFAULT 0,

    failed_tests INTEGER DEFAULT 0,

    skipped_tests INTEGER DEFAULT 0,

    exit_code INTEGER,

    duration_ms BIGINT,

    output TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    started_at TIMESTAMPTZ,

    completed_at TIMESTAMPTZ,

    CONSTRAINT test_run_status_check
        CHECK (
            status IN (
                'queued',
                'running',
                'passed',
                'failed',
                'cancelled'
            )
        )
);

Output retention must be limited.

18. deployments

Reserved for deployment functionality.

CREATE TABLE deployments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL
        REFERENCES projects(id)
        ON DELETE CASCADE,

    user_id UUID
        REFERENCES users(id)
        ON DELETE SET NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'queued',

    provider VARCHAR(50),

    environment VARCHAR(30) NOT NULL DEFAULT 'production',

    deployment_url TEXT,

    commit_sha VARCHAR(64),

    build_log TEXT,

    error TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    started_at TIMESTAMPTZ,

    completed_at TIMESTAMPTZ,

    CONSTRAINT deployment_status_check
        CHECK (
            status IN (
                'queued',
                'building',
                'deploying',
                'ready',
                'failed',
                'cancelled'
            )
        ),

    CONSTRAINT deployment_environment_check
        CHECK (
            environment IN (
                'preview',
                'staging',
                'production'
            )
        )
);

Deployment functionality is not required for the initial V1 runtime milestone.

19. audit_logs

Stores security and important product events.

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID
        REFERENCES users(id)
        ON DELETE SET NULL,

    project_id UUID
        REFERENCES projects(id)
        ON DELETE SET NULL,

    action VARCHAR(100) NOT NULL,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    ip_address INET,

    user_agent TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

Examples:

user.login
user.logout
project.created
project.deleted
runtime.started
runtime.stopped
github.connected
github.imported
git.push
git.pull
test.started
test.completed
deployment.created
ai.change.approved

Do not store:

passwords
access tokens
refresh tokens
GitHub tokens
API keys
private source code unnecessarily
terminal secrets
20. Indexes

Create indexes for common access patterns.

CREATE INDEX idx_projects_owner_id
ON projects(owner_id);

CREATE INDEX idx_projects_updated_at
ON projects(updated_at DESC);

CREATE INDEX idx_project_members_user_id
ON project_members(user_id);

CREATE INDEX idx_runtimes_project_id
ON runtimes(project_id);

CREATE INDEX idx_runtimes_status
ON runtimes(status);

CREATE INDEX idx_command_executions_runtime_id
ON command_executions(runtime_id);

CREATE INDEX idx_command_executions_user_id
ON command_executions(user_id);

CREATE INDEX idx_jobs_status
ON jobs(status);

CREATE INDEX idx_jobs_project_id
ON jobs(project_id);

CREATE INDEX idx_jobs_created_at
ON jobs(created_at DESC);

CREATE INDEX idx_test_runs_project_id
ON test_runs(project_id);

CREATE INDEX idx_test_runs_created_at
ON test_runs(created_at DESC);

CREATE INDEX idx_audit_logs_user_id
ON audit_logs(user_id);

CREATE INDEX idx_audit_logs_project_id
ON audit_logs(project_id);

CREATE INDEX idx_audit_logs_created_at
ON audit_logs(created_at DESC);
21. Updated-at Trigger

RUNIX should automatically update updated_at.

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

Apply to tables containing updated_at:

CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at
BEFORE UPDATE ON projects
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workspaces_updated_at
BEFORE UPDATE ON workspaces
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_git_repositories_updated_at
BEFORE UPDATE ON git_repositories
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_git_branches_updated_at
BEFORE UPDATE ON git_branches
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
22. Data Ownership Rules

Every project-owned resource must ultimately resolve to a project.

Example:

User
  ↓
Project
  ↓
Workspace
  ↓
Runtime
  ↓
Terminal

A user must not be able to access a resource merely by knowing its UUID.

Every request must perform authorization.

Example:

project = await get_project(project_id)

if not await user_can_access_project(
    user=current_user,
    project=project
):
    raise HTTPException(
        status_code=403,
        detail="Project access denied"
    )
23. Deletion Rules

Deleting a user:

User
 ├── Sessions        → CASCADE
 ├── Projects        → CASCADE
 └── Audit Logs      → SET NULL

Deleting a project:

Project
 ├── Members         → CASCADE
 ├── Workspace       → CASCADE
 ├── Runtime records → CASCADE
 ├── Git metadata    → CASCADE
 ├── Jobs            → CASCADE
 ├── Test runs       → CASCADE
 └── Deployments     → CASCADE

Before deleting a project, RUNIX must first:

stop active runtimes
terminate runtime containers
close terminal sessions
release runtime resources
remove workspace storage according to retention policy
delete database records

Database deletion must not be treated as sufficient cleanup of runtime resources.

24. Secrets

Secrets must NOT be stored in ordinary database fields.

Examples:

GitHub access tokens
AI provider API keys
deployment credentials
cloud provider credentials
user secrets

If persistent secrets are required:

encrypt them at rest
restrict access to the backend service
never return them through normal API responses
never log them
never expose them to the browser
rotate them when supported

A dedicated secret-management service can replace this implementation in a later infrastructure phase.

25. SQLAlchemy Model Organization

Recommended backend structure:

backend/
└── app/
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   ├── session.py
    │   ├── project.py
    │   ├── project_member.py
    │   ├── workspace.py
    │   ├── project_file_metadata.py
    │   ├── runtime.py
    │   ├── terminal_session.py
    │   ├── command_execution.py
    │   ├── git_repository.py
    │   ├── git_branch.py
    │   ├── job.py
    │   ├── test_run.py
    │   ├── deployment.py
    │   └── audit_log.py
    │
    └── db/
        ├── session.py
        ├── base.py
        └── migrations/

Use SQLAlchemy 2.x style models.

26. Migration Strategy

Use Alembic.

Never manually modify an already-applied production migration.

Development workflow:

alembic revision --autogenerate -m "create initial schema"
alembic upgrade head

Check migration:

alembic current

Upgrade:

alembic upgrade head

Rollback one migration:

alembic downgrade -1

Production migrations must be reviewed before execution.

27. Transaction Rules

Use database transactions for related state changes.

Example:

Create Project
    ↓
Create Workspace
    ↓
Commit

If workspace creation fails before the transaction is committed, the database transaction should be rolled back.

Runtime state requires additional care because Docker state exists outside PostgreSQL.

Therefore:

Database transaction
        +
Runtime reconciliation

must be treated as separate systems.

RUNIX must never assume that a successful database transaction automatically means a Docker operation succeeded.

28. Runtime Reconciliation

On backend startup and periodically:

query active runtime records
query actual managed containers
compare database and runtime state
identify abandoned containers
terminate unauthorized/orphaned containers
mark missing runtimes as failed/stopped
update health timestamps

This prevents stale runtime records.

29. Database Security

Production PostgreSQL requirements:

private network access
TLS where applicable
strong database credentials
least-privilege database user
no public database exposure unless explicitly required
automated backups
tested restore procedure
connection pooling
migration control
database monitoring

The frontend must never connect directly to PostgreSQL.

Architecture:

Browser
   │
   ▼
RUNIX API
   │
   ▼
PostgreSQL

Never:

Browser
   │
   ▼
PostgreSQL
30. V1 Required Tables

V1 implementation must include:

users
sessions
projects
project_members
workspaces
runtimes
terminal_sessions
command_executions
jobs
test_runs
audit_logs

Git tables are required when GitHub integration is implemented.

Deployment tables may be created during initial schema setup but deployment functionality is not required for the first V1 milestone.

31. Database Source-of-Truth Rules

PostgreSQL is the source of truth for:

users
authentication sessions
projects
project ownership
workspace metadata
runtime metadata
job state
test metadata
Git provider metadata
audit records

Workspace storage is the source of truth for:

source files
project directories
package files
Git repository contents

Git is the source of truth for:

commit history
branches
Git objects
repository history

Redis is NOT the source of truth.

Docker container state is NOT the source of truth.

The RUNIX API reconciles external runtime state with PostgreSQL.


---
