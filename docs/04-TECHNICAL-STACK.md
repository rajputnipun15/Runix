# RUNIX — Technical Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Monaco Editor
- xterm.js
- Playwright
- Vitest

## Backend

- Python 3.11+
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- pytest

## Database

PostgreSQL 16+ compatible deployment.

The exact managed PostgreSQL provider is environment-specific.

## Queue

Redis 7+ compatible deployment.

## Runtime

Docker Engine / Docker-compatible runtime.

## Git

Git CLI inside controlled worker/runtime environments.

## GitHub

GitHub OAuth or GitHub App.

Prefer GitHub App architecture for production because permissions can be
restricted more precisely.

## AI

Create an internal provider abstraction:

AIProvider
    |
    +-- ProviderImplementationA
    +-- ProviderImplementationB

Do not hard-code the application architecture around one model provider.

## API Documentation

FastAPI OpenAPI.

## Container Images

Initial approved runtime images:

- runix/node:22
- runix/python:3.12
- runix/mern:versioned

Do not use mutable `latest` tags in production.

## Local Development

Docker Compose should provide:

- PostgreSQL
- Redis
- API
- worker
- runtime manager
- frontend

The Docker daemon itself may remain host-provided during development.

---

# Version Policy

Dependencies must use lockfiles.

Do not blindly install the latest package version.

Dependency upgrades must be intentional and tested.