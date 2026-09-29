# RUNIX — Agent & Contributor Guidelines

This document provides essential context and instructions for AI agents and human contributors developing the **RUNIX** platform.

Product tagline:
> **Build. Run. Ship. Anywhere.**

## Core Architecture Principles

1. **Security Isolation**:
   - Never execute arbitrary untrusted code directly on the control plane or API server host.
   - Workspaces must always be scoped strictly to designated tenant sandboxes/containers.
   - Prevent all path traversal vulnerabilities (`..`, symlinks escaping workspace bounds).

2. **Full-Stack Separation**:
   - **Frontend**: Next.js 16 (Turbopack, TypeScript, Tailwind CSS). Connects to API base via `src/lib/api.ts`.
   - **Backend**: FastAPI (Python 3.12+), SQLAlchemy (async), SQLite (local dev) / PostgreSQL (production).
   - **Terminal & Execution**: Dual-mode terminal supporting streaming WebSockets (`/ws/projects/{project_id}/terminal`) with REST command fallback (`POST /api/v1/projects/{project_id}/commands`).

3. **Database & Migrations**:
   - SQLite (`runix_dev.db`) is used for local zero-dependency development.
   - PostgreSQL is used in staging/production via Docker Compose.
   - All migrations must be compatible with SQLAlchemy async sessions.

4. **Testing Standards**:
   - Backend: `pytest` with `pytest-asyncio`. Run `pytest` inside `backend/`.
   - Frontend: TypeScript typechecking (`npx tsc --noEmit`) and component tests.
   - All tests must pass before merging or pushing changes.

5. **Secrets & Configurations**:
   - Secrets must never be committed to source control.
   - Always reference `.env.example` for environment variable templates.
