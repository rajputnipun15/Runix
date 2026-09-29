# RUNIX

Cloud-native development environment and execution runtime engine.

## Directory Structure

```text
RUNIX/
│
├── docs/                      # Architectural & engineering specifications
│   ├── 00-PROJECT-OVERVIEW.md
│   ├── 01-PRD.md
│   ├── 02-FUNCTIONAL-REQUIREMENTS.md
│   ├── 03-SYSTEM-ARCHITECTURE.md
│   ├── 04-TECHNICAL-STACK.md
│   ├── 05-DATABASE-SCHEMA.md
│   ├── 06-API-SPECIFICATION.md
│   ├── 07-WEBSOCKET-SPECIFICATION.md
│   ├── 08-RUNTIME-ENGINE.md
│   ├── 09-WORKSPACE-FILESYSTEM.md
│   ├── 10-GITHUB-INTEGRATION.md
│   ├── 11-AI-AGENT-SPECIFICATION.md
│   ├── 12-SECURITY-ARCHITECTURE.md
│   ├── 13-FRONTEND-SPECIFICATION.md
│   ├── 14-DESIGN-SYSTEM.md
│   ├── 15-PROJECT-TEMPLATES.md
│   ├── 16-TESTING-STRATEGY.md
│   ├── 17-OBSERVABILITY.md
│   ├── 18-ERROR-HANDLING.md
│   ├── 19-DEPLOYMENT.md
│   ├── 20-ROADMAP.md
│   └── 21-DEFINITION-OF-DONE.md
│
├── frontend/                  # Web IDE and client user interface
├── backend/                   # Core API services and business logic
├── worker/                    # Asynchronous background jobs and task processing
├── runtime/                   # Sandboxed execution engine and container runtimes
├── infrastructure/            # Terraform, Kubernetes, and deployment configs
├── scripts/                   # Development, setup, and maintenance scripts
├── tests/                     # Integration, E2E, and benchmark suites
│
├── docker-compose.yml         # Local development orchestration
├── .env.example               # Environment variables template
└── README.md                  # Project overview and quickstart guide
```

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose
- [Node.js](https://nodejs.org/) (v20+)
- [Go](https://go.dev/) (v1.22+) or runtime dependencies depending on service

### Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Start dependencies and local development stack:
   ```bash
   docker-compose up -d
   ```

3. Refer to the documentation in [docs/](docs/00-PROJECT-OVERVIEW.md) for full system specifications.
