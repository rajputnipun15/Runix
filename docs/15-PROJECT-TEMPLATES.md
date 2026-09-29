1. Purpose

RUNIX allows developers to create new projects from predefined development templates.

A template provides:

initial project structure;
source files;
dependency configuration;
runtime configuration;
development commands;
default environment variables;
default ports;
package manager configuration;
README;
.gitignore;
runtime compatibility metadata.

Templates provide a predictable starting point for developers while allowing RUNIX to control runtime safety and reproducibility.

The template system must be:

deterministic;
versioned;
reproducible;
secure;
extensible;
compatible with the RUNIX runtime engine;
independent from the frontend;
independent from any specific AI provider.
2. Important Architecture Rule

RUNIX itself and a user-created project are different systems.

RUNIX's control plane uses:

FastAPI
PostgreSQL
Redis
Workers
Docker

A user project may use:

React
Node.js
Python
FastAPI
MERN
etc.

For example:

RUNIX
├── PostgreSQL
├── Redis
├── FastAPI
└── Docker runtime manager

is not the same thing as:

User MERN Project
├── React
├── Express
├── Node.js
└── MongoDB connection

The mern template does not change RUNIX's own database architecture.

3. Initial Template Catalog

V1 supports the following templates:

ID	Name	Language	Framework	Runtime	Default Port
react-vite-ts	React + Vite + TypeScript	TypeScript	React/Vite	Node.js 22	5173
node-typescript	Node.js + TypeScript	TypeScript	Node.js	Node.js 22	3000
python-fastapi	Python + FastAPI	Python	FastAPI	Python 3.12	8000
mern	MERN Stack	TypeScript/JavaScript	MongoDB/Express/React/Node	Node.js 22	5173 / 5000
blank-docker	Blank Development Environment	—	—	RUNIX Blank	None

These templates are the initial supported catalog.

Additional templates can be introduced later without changing the fundamental template architecture.

4. Template IDs

Template IDs are stable identifiers.

Example:

react-vite-ts
node-typescript
python-fastapi
mern
blank-docker

Do not use display names as identifiers.

Good:

{
  "template": "react-vite-ts"
}

Bad:

{
  "template": "React + Vite + TypeScript"
}

Display names may change without breaking stored project metadata.

5. Template Versioning

Templates are versioned independently from RUNIX.

Example:

react-vite-ts@1.0.0
react-vite-ts@1.1.0
react-vite-ts@2.0.0

A project created from:

react-vite-ts@1.0.0

must retain its original template metadata.

Creating a new project later may use:

react-vite-ts@1.1.0

unless the user explicitly selects another version.

6. Template Version Rules

Template versions follow semantic versioning:

MAJOR.MINOR.PATCH
MAJOR

Breaking project structure or runtime behavior.

Example:

1.x → 2.x

when the template changes its fundamental architecture.

MINOR

Backward-compatible additions.

Example:

1.0.0 → 1.1.0

adding a utility file.

PATCH

Bug fixes.

Example:

1.0.0 → 1.0.1

fixing an incorrect configuration.

7. Immutable Template Versions

Once published, a template version must be immutable.

Do not modify:

react-vite-ts@1.0.0

after publication.

Instead publish:

react-vite-ts@1.0.1

This guarantees reproducibility.

8. Template Registry

The backend must maintain a template registry.

Conceptually:

class TemplateRegistry:
    def list_templates(self):
        ...

    def get_template(self, template_id):
        ...

    def get_version(self, template_id, version):
        ...

    def validate_template(self, template_id, version):
        ...

The registry is responsible for:

template discovery;
validation;
version resolution;
runtime compatibility;
metadata;
template materialization.
9. Template Manifest

Every template must have a manifest.

Recommended filename:

runix-template.json

Example:

{
  "id": "react-vite-ts",
  "version": "1.0.0",
  "name": "React + Vite + TypeScript",
  "description": "Modern React application using Vite and TypeScript.",
  "language": "typescript",
  "framework": "react",
  "runtime_type": "node",
  "runtime_image": "runix/node:22",
  "package_manager": "npm",
  "default_ports": [5173],
  "entrypoint": "src/main.tsx",
  "commands": {
    "install": "npm install",
    "dev": "npm run dev",
    "build": "npm run build",
    "test": "npm test"
  },
  "environment": {},
  "healthcheck": {
    "path": "/",
    "port": 5173
  }
}
10. Complete Manifest Schema

The template manifest should support:

id
version
name
description
language
framework
runtime_type
runtime_image
package_manager
default_ports
entrypoint
commands
environment
healthcheck
files
capabilities
status
metadata

Example:

{
  "id": "python-fastapi",
  "version": "1.0.0",
  "name": "Python + FastAPI",
  "description": "FastAPI backend using Python.",
  "language": "python",
  "framework": "fastapi",
  "runtime_type": "python",
  "runtime_image": "runix/python:3.12",
  "package_manager": "pip",
  "default_ports": [8000],
  "entrypoint": "app/main.py",
  "commands": {
    "install": "pip install -r requirements.txt",
    "dev": "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload",
    "test": "pytest"
  },
  "environment": {
    "PORT": "8000"
  },
  "healthcheck": {
    "path": "/health",
    "port": 8000
  },
  "capabilities": [
    "terminal",
    "preview",
    "git",
    "tests"
  ],
  "status": "active"
}
11. Template Directory Structure

Recommended repository structure:

templates/
├── registry/
│   ├── react-vite-ts/
│   │   └── 1.0.0/
│   │       ├── runix-template.json
│   │       ├── package.json
│   │       ├── tsconfig.json
│   │       ├── vite.config.ts
│   │       ├── index.html
│   │       ├── src/
│   │       ├── public/
│   │       └── .gitignore
│   │
│   ├── node-typescript/
│   │   └── 1.0.0/
│   │
│   ├── python-fastapi/
│   │   └── 1.0.0/
│   │
│   ├── mern/
│   │   └── 1.0.0/
│   │
│   └── blank-docker/
│       └── 1.0.0/
│
└── README.md

The template directory is controlled by RUNIX.

Users must not be able to modify template source through normal project APIs.

12. Template Materialization

Template materialization means copying a template into a new project workspace.

Flow:

User selects template
        ↓
Backend validates template
        ↓
Create project
        ↓
Create workspace
        ↓
Resolve template version
        ↓
Materialize template files
        ↓
Generate project-specific metadata
        ↓
Initialize Git if requested
        ↓
Return project
13. Template Materialization Security

Template materialization must:

use trusted template sources;
validate template manifests;
prevent path traversal;
prevent writing outside workspace;
preserve file integrity;
reject invalid template metadata;
avoid executing template commands;
avoid executing package installation;
avoid executing postinstall scripts.

Most importantly:

Template creation must never execute user or template code on the RUNIX API host.

14. Dependency Installation

Creating a project should not automatically execute arbitrary dependency installation on the control plane.

For example, RUNIX must not perform:

npm install

on the API server.

Instead:

Create Project
      ↓
Materialize files
      ↓
Start isolated runtime
      ↓
Install dependencies inside runtime
15. Dependency Installation Policy

Dependencies are installed inside the user's runtime.

Examples:

npm install

or:

pip install -r requirements.txt

must execute inside the isolated runtime.

The runtime must enforce:

CPU limits;
memory limits;
PID limits;
storage limits;
command timeout;
network policy.
16. Runtime Image Mapping

Templates map to controlled runtime images.

Template	Runtime Image
react-vite-ts	runix/node:22
node-typescript	runix/node:22
python-fastapi	runix/python:3.12
mern	runix/mern:versioned
blank-docker	runix/blank:versioned

Production images should be pinned to immutable versions or digests.

Avoid:

runix/node:latest

for production runtime creation.

17. React + Vite + TypeScript
Template ID
react-vite-ts
Version
1.0.0
Stack
React
Vite
TypeScript
Node.js 22
npm
Default Port
5173
Development Command
npm run dev -- --host 0.0.0.0
Build Command
npm run build
Test Command
npm test
18. React Template Structure

Expected structure:

project/
├── public/
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   ├── index.css
│   └── vite-env.d.ts
├── .gitignore
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── vite.config.ts
└── README.md

The exact generated files must be defined by the immutable template version.

19. React Runtime Requirements

The development server must bind to:

0.0.0.0

not:

127.0.0.1

This allows the RUNIX preview gateway to reach the development server inside the runtime.

20. Node.js + TypeScript
Template ID
node-typescript
Stack
Node.js 22
TypeScript
tsx
npm
Default Port
3000
Development Command
npm run dev

Recommended development command:

tsx watch src/index.ts
21. Node Template Structure
project/
├── src/
│   └── index.ts
├── tests/
├── package.json
├── tsconfig.json
├── .gitignore
└── README.md

The starter server should listen on:

0.0.0.0:3000
22. Node Environment Variables

The default template may expose:

PORT=3000
NODE_ENV=development

The actual environment must be injected by the runtime environment rather than hard-coded secrets.

23. Python + FastAPI
Template ID
python-fastapi
Stack
Python 3.12
FastAPI
Uvicorn
pytest
pip
Default Port
8000
Development Command
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
24. Python Template Structure
project/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_health.py
├── requirements.txt
├── .gitignore
├── README.md
└── pyproject.toml
25. FastAPI Starter Application

The template should contain a minimal functional application.

Example:

from fastapi import FastAPI

app = FastAPI(title="RUNIX FastAPI Project")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Hello from RUNIX"}

This is starter code only.

Users can replace it immediately.

26. FastAPI Test

The initial template should include a basic test.

Example:

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

This gives RUNIX a deterministic template acceptance test.

27. MERN Template
Template ID
mern
Stack
MongoDB
Express
React
Node.js
TypeScript
Vite
Runtime
runix/mern:versioned
28. MERN Architecture

Initial RUNIX MERN projects use:

project/
├── client/
│   └── React + Vite
│
├── server/
│   └── Express + Node
│
├── package.json
└── README.md

Default ports:

Frontend → 5173
Backend  → 5000
29. MERN Runtime Model

The initial RUNIX runtime model uses a single project runtime.

Therefore the MERN template should not automatically launch a MongoDB server inside the same runtime.

MongoDB should be configured through:

MONGODB_URI

Example:

MONGODB_URI=mongodb://...

The actual connection string must be supplied by the user or a future RUNIX-managed database service.

30. MERN Environment Variables

Backend:

PORT=5000
MONGODB_URI=

Frontend may use:

VITE_API_URL=http://localhost:5000

When running through RUNIX preview, frontend/backend URLs should be generated according to the preview architecture rather than assuming localhost is externally reachable.

31. MERN Root Scripts

Recommended:

{
  "scripts": {
    "dev": "concurrently \"npm run dev:client\" \"npm run dev:server\"",
    "dev:client": "npm --prefix client run dev -- --host 0.0.0.0",
    "dev:server": "npm --prefix server run dev",
    "build": "npm run build:client && npm run build:server",
    "build:client": "npm --prefix client run build",
    "build:server": "npm --prefix server run build"
  }
}

The exact implementation can evolve with the immutable template version.

32. MERN Dependency Policy

MongoDB itself should not be automatically installed as an operating-system service.

Do not execute:

apt install mongodb

inside the runtime.

The template should use the MongoDB client/driver and an externally supplied MongoDB endpoint.

33. Blank Development Environment
Template ID
blank-docker

Purpose:

Provide an empty but functional development workspace.

Initial contents:

project/
├── README.md
└── .gitignore

Runtime:

runix/blank:versioned

No default application server is started.

34. Blank Template Use Cases

The blank environment is useful for:

custom projects;
experiments;
shell development;
importing existing repositories;
manually installing tools;
projects not represented by existing templates.

It should not imply that arbitrary Dockerfiles are automatically trusted or executed by the control plane.

35. Custom Dockerfiles

V1 does not support unrestricted custom runtime images.

A user-created:

Dockerfile

must not automatically cause RUNIX infrastructure to build or execute an arbitrary privileged container.

Future custom-runtime support must use:

controlled build infrastructure;
resource limits;
image scanning;
network restrictions;
provenance;
immutable image references;
approval policies.
36. Template Metadata

Each created project should retain metadata similar to:

{
  "template": "react-vite-ts",
  "template_version": "1.0.0"
}

This allows RUNIX to identify the origin of the project without requiring the project to remain permanently synchronized with the template.

37. Template and Project Independence

After project creation, the user owns the project workspace.

Changing the global template must not overwrite existing project files.

For example:

react-vite-ts@1.0.0

creates:

my-project/

Publishing:

react-vite-ts@1.1.0

must not modify:

my-project/
38. Template Updates

Template updates affect:

new projects

by default.

Existing projects can optionally receive an explicit upgrade workflow in a future version.

V1 should not automatically migrate existing repositories.

39. Template Integrity

Templates should have integrity metadata.

Example:

{
  "id": "react-vite-ts",
  "version": "1.0.0",
  "integrity": {
    "algorithm": "sha256",
    "digest": "..."
  }
}

The integrity value represents the published template contents.

40. Template Validation

Before publication, RUNIX should validate:

manifest
files
paths
runtime image
commands
ports
environment variables
dependency metadata
README
.gitignore

Reject:

absolute file paths;
parent traversal;
invalid manifest;
executable unexpected metadata;
missing required runtime configuration.
41. Template Path Security

Template paths must be workspace-relative.

Allowed:

src/main.ts
package.json
README.md

Rejected:

../file
../../secret
/etc/passwd
C:\Windows\file

Template materialization must use the same safe path validation principles defined in:

09-WORKSPACE-FILESYSTEM.md
42. Template File Permissions

Template files should use predictable permissions.

Normal source files:

0644

Directories:

0755

Executable scripts should be explicitly marked executable.

Do not make every generated file executable.

43. Generated Files

RUNIX may generate project-specific files such as:

.runix/

where required.

However, generated metadata should be minimal.

Do not inject RUNIX-specific files into user repositories unnecessarily.

44. .gitignore

Each template must provide an appropriate .gitignore.

React/Node example:

node_modules/
dist/
.env
.env.*
!.env.example
.DS_Store

Python example:

__pycache__/
*.py[cod]
.venv/
.env
.pytest_cache/

Secrets should never be committed by default.

45. Environment Variable Templates

Where configuration is required, provide:

.env.example

rather than:

.env

Example:

MONGODB_URI=
PORT=5000

Do not generate real credentials.

46. Secret Handling

Template files must never contain:

API keys;
passwords;
access tokens;
private keys;
GitHub credentials;
database production credentials.

This applies even to example templates.

Use placeholders.

47. README Generation

Every template must include a README explaining:

what the template is
how to run it
default port
environment variables
test command
build command

Example:

# React + Vite + TypeScript

## Development

npm install
npm run dev

## Build

npm run build

## Port

5173
48. Template Discovery API

The backend should expose:

GET /api/v1/templates

Response:

{
  "templates": [
    {
      "id": "react-vite-ts",
      "version": "1.0.0",
      "name": "React + Vite + TypeScript",
      "description": "Modern React application.",
      "language": "typescript",
      "framework": "react",
      "runtime_type": "node",
      "default_ports": [5173],
      "status": "active"
    }
  ]
}
49. Template Details API

Endpoint:

GET /api/v1/templates/{template_id}

Example:

GET /api/v1/templates/react-vite-ts

Response should contain the template metadata required by the frontend to display the template selection UI.

50. Project Creation API

Project creation should accept:

{
  "name": "My React App",
  "template": "react-vite-ts",
  "template_version": "1.0.0",
  "description": "My first RUNIX project",
  "visibility": "private"
}

If template_version is omitted, the backend selects the current active version.

The backend must perform version resolution.

The frontend must not determine the active version itself.

51. Template Selection UI

The frontend must use the existing RUNIX Stitch design.

The project creation experience must preserve the visual structure of the Stitch screens:

RUNIX — New Workspace Creation
RUNIX — New Workspace Creation (Interactive & Animated)
RUNIX — Create Workspace

The template picker should therefore be implemented as part of the existing Stitch-derived workspace creation interface.

Do not replace it with a generic SaaS template dashboard.

52. Template Card Data

Template cards should be generated from backend template metadata.

Conceptually:

Template API
     ↓
Frontend template registry
     ↓
Stitch-derived template cards

Do not hard-code a second independent template catalog in the frontend.

53. Template Card Information

Each template should expose enough metadata to display:

name
description
language
framework
runtime
default port
version
availability

Optional:

icon
category
tags
recommended_for

The visual treatment must follow the existing Stitch design system.

54. Template Creation Flow

Complete flow:

User opens Create Workspace
        ↓
Frontend loads templates
        ↓
User selects template
        ↓
User enters project name
        ↓
Frontend submits request
        ↓
Backend authenticates user
        ↓
Backend validates template
        ↓
Backend creates project
        ↓
Backend creates workspace
        ↓
Template materialized
        ↓
Metadata stored
        ↓
Optional Git initialization
        ↓
Optional runtime start
        ↓
Workspace opens
55. Failure During Template Creation

If template materialization fails:

Project creation
      ↓
Workspace creation
      ↓
Template failure

RUNIX must not leave an apparently healthy project with incomplete template files.

Use transactional or compensating behavior:

rollback
or
mark creation as failed
and clean temporary resources
56. Runtime Start After Creation

Runtime startup may be:

automatic

or:

manual

depending on the product UX and project creation settings.

If automatic startup is enabled:

create project
→ materialize template
→ start runtime
→ install dependencies
→ start development server

All code execution occurs inside the runtime.

57. Template Health Checks

Templates with development servers should define health checks.

Example:

{
  "healthcheck": {
    "path": "/",
    "port": 5173
  }
}

FastAPI:

{
  "healthcheck": {
    "path": "/health",
    "port": 8000
  }
}

RUNIX uses these values for preview readiness.

58. Port Discovery

Declared ports are defaults, not unconditional guarantees.

RUNIX may detect actual listening ports.

For example:

declared: 5173
detected: 5173

is expected.

If the application starts on another port, the runtime manager may detect it according to the port discovery specification.

59. Template Capabilities

Templates can declare capabilities.

Example:

{
  "capabilities": [
    "editor",
    "terminal",
    "preview",
    "git",
    "tests"
  ]
}

Future capabilities may include:

database
deployment
background_worker
multi_service
60. Template Status

Supported statuses:

draft
active
deprecated
disabled

Only:

active

templates should be selectable for normal project creation.

61. Deprecated Templates

A deprecated template:

remains available to existing projects;
should not be selected for new projects by default;
may display a migration recommendation;
must remain immutable.
62. Disabled Templates

A disabled template cannot be used for new projects.

Existing projects created from that template may continue running if their runtime image remains supported.

63. Template Testing

Every template must pass automated tests before becoming active.

Required flow:

load manifest
↓
validate manifest
↓
materialize
↓
validate files
↓
create runtime
↓
install dependencies
↓
start development server
↓
health check
↓
run tests
↓
build
↓
cleanup
64. React Template Acceptance Test

Expected:

npm install
npm run build
npm run dev

Then:

GET /

must return successfully.

The runtime must expose port:

5173
65. Node Template Acceptance Test

Expected:

npm install
npm run build
npm run dev

The application must listen on:

0.0.0.0:3000

A health endpoint should respond successfully.

66. FastAPI Template Acceptance Test

Expected:

pip install -r requirements.txt
pytest
uvicorn app.main:app --host 0.0.0.0 --port 8000

Expected:

GET /health

returns:

{
  "status": "ok"
}
67. MERN Template Acceptance Test

Expected:

npm install
npm run build

Then:

frontend → 5173
backend → 5000

The backend should start without requiring MongoDB for basic health testing if the template is designed to support a disconnected startup mode.

The exact database integration test may use a dedicated MongoDB test service.

68. Blank Template Acceptance Test

Expected:

workspace created
runtime starts
terminal available

No application server is required.

The runtime must remain usable through the terminal.

69. Template Build Reproducibility

Template acceptance tests should run against a clean runtime.

Example:

new runtime
↓
fresh workspace
↓
materialize template
↓
install dependencies
↓
build

Do not rely on dependencies installed by a previous test.

70. Dependency Lockfiles

Templates should use lockfiles where practical.

Examples:

package-lock.json

for npm templates.

Python templates should use pinned or appropriately constrained dependencies.

The exact dependency strategy must be defined per immutable template version.

71. Dependency Updates

RUNIX must not silently modify template dependencies during project creation.

The generated project should represent the published template version.

Users can update dependencies themselves after creation.

72. Template Security Review

Before activation, review:

dependency sources
scripts
startup commands
filesystem paths
network requirements
runtime permissions
environment variables

No template should require:

--privileged
host networking
Docker socket
host filesystem mounts
root-only access

unless explicitly approved by a future architecture change.

73. Template Supply Chain

Template sources should be version-controlled.

Recommended:

Git
    ↓
review
    ↓
CI validation
    ↓
security scan
    ↓
template package
    ↓
integrity hash
    ↓
publish

Never modify published template artifacts manually in production.

74. Template Publishing

A template release should follow:

Developer changes template
        ↓
Pull request
        ↓
Tests
        ↓
Security checks
        ↓
Template acceptance tests
        ↓
Review
        ↓
Version bump
        ↓
Publish
        ↓
Registry activation
75. Template Rollback

If a newly published template version is defective:

react-vite-ts@1.1.0

can be marked:

disabled

and:

react-vite-ts@1.0.0

can remain active.

Existing projects are unaffected.

76. Template Cache

RUNIX may cache template artifacts for faster creation.

Cache must be:

immutable by version;
integrity checked;
safe to invalidate;
independent from user workspace storage.

Example:

template cache
react-vite-ts/1.0.0

must never be writable by user project processes.

77. Template Storage

Template storage must be separate from user workspaces.

Do not store templates under:

/var/lib/runix/workspaces/

Use a separate controlled location such as:

/var/lib/runix/templates/

or an object/artifact store.

78. User Workspace Isolation

A user's runtime receives:

/var/lib/runix/workspaces/<project-id>

mounted as:

/workspace

It must not receive access to:

/var/lib/runix/templates

unless a future architecture explicitly requires a read-only template mount.

Preferred behavior is to materialize files before runtime startup.

79. Template Logging

Template creation logs should include:

template_id
template_version
project_id
user_id
duration
status
error_code

Do not log:

file contents
environment secrets
credentials
private keys
80. Template Metrics

Recommended metrics:

runix_template_creation_total
runix_template_creation_failed_total
runix_template_creation_duration_seconds
runix_template_materialization_duration_seconds
runix_template_runtime_start_duration_seconds
runix_template_healthcheck_failures_total

Labels should remain bounded.

Avoid high-cardinality labels such as arbitrary project names.

81. Template Error Codes

Recommended errors:

TEMPLATE_NOT_FOUND
TEMPLATE_VERSION_NOT_FOUND
TEMPLATE_DISABLED
TEMPLATE_INVALID
TEMPLATE_MATERIALIZATION_FAILED
TEMPLATE_INTEGRITY_FAILED
TEMPLATE_RUNTIME_INCOMPATIBLE
TEMPLATE_HEALTHCHECK_FAILED
82. API Error Example
{
  "error": {
    "code": "TEMPLATE_NOT_FOUND",
    "message": "The requested project template is not available.",
    "request_id": "req_123"
  }
}

Do not expose internal filesystem paths or stack traces.

83. Template Configuration

Recommended backend configuration:

RUNIX_TEMPLATE_ROOT=/var/lib/runix/templates
RUNIX_TEMPLATE_CACHE=/var/lib/runix/template-cache
RUNIX_DEFAULT_TEMPLATE_VERSION=latest

latest is a registry resolution concept only.

Projects must store the resolved immutable version.

84. Template Creation Data Model

The Project entity should store:

template
template_version

Example:

template = react-vite-ts
template_version = 1.0.0

This can be added to the existing project schema if not already present.

85. Frontend Template Types

The frontend should consume a typed model similar to:

export interface ProjectTemplate {
  id: string;
  version: string;
  name: string;
  description: string;
  language?: string;
  framework?: string;
  runtimeType: string;
  defaultPorts: number[];
  status: "active" | "deprecated" | "disabled";
}

The exact API client types should be generated or maintained from the backend contract.

86. Template Loading State

The Stitch-derived create-workspace UI must support:

loading
loaded
empty
error

Do not display fake template cards while the API is unavailable.

87. Template Error State

If template loading fails, display a clear error state consistent with the existing Stitch visual system.

Example behavior:

Unable to load project templates.

Retry

Do not silently fall back to hard-coded templates unless explicitly designed as an offline fallback.

88. Template Selection State

The UI must clearly represent:

unselected
selected
unavailable
deprecated

The selected template should be preserved while the user enters project configuration.

89. Template Creation Progress

For creation flows that take time, the UI should represent meaningful stages.

Example:

Creating workspace
      ↓
Preparing template
      ↓
Setting up files
      ↓
Starting runtime
      ↓
Workspace ready

These states should reflect real backend/runtime events.

Do not display fake progress percentages.

90. Template Creation Cancellation

If cancellation is supported, it must:

cancel only the current creation job;
clean temporary resources;
not affect unrelated projects;
report the final state accurately.

If cancellation is not implemented, the UI must not display a fake cancel action.

91. Template and Git Initialization

A new project may optionally initialize Git.

Flow:

template materialization
↓
git init
↓
initial files
↓
initial status

Git initialization occurs inside the appropriate project/runtime infrastructure, not through arbitrary host shell execution.

92. Initial Commit

V1 should not automatically create and push an external GitHub commit unless the user explicitly requests it.

If an initial local commit is automatically created, this behavior must be explicitly documented in the product flow.

Recommended default:

workspace created
Git repository initialized
No automatic external push
93. Imported Repositories

Templates are primarily for new projects.

GitHub imports are different:

Template project
≠
Imported repository

An imported repository should preserve its existing structure instead of being overwritten by a template.

94. Template Compatibility

Each template must declare compatible runtime information.

Example:

{
  "runtime_type": "node",
  "runtime_image": "runix/node:22"
}

The runtime manager validates compatibility before startup.

95. Template Runtime Contract

Every executable template must define:

runtime type
runtime image
start command
default ports
health check
environment requirements

Without these fields, the template cannot be marked active.

96. Template Non-Goals for V1

V1 does not include:

arbitrary user Docker images;
arbitrary Dockerfile execution on the control plane;
multi-container orchestration;
Kubernetes-based user runtimes;
automatic template migration;
template marketplace;
user-created public templates;
GitLab templates;
Bitbucket templates;
automatic dependency upgrades;
automatic deployment.

These may be introduced later.

97. Future Template Architecture

The architecture should eventually support:

Template Registry
        ↓
Template Versions
        ↓
Runtime Profiles
        ↓
Project Creation
        ↓
Workspace
        ↓
Runtime

Future templates may include:

Next.js
Django
Flask
Vue
Angular
Svelte
Go
Rust
Java
Spring Boot
PHP
Laravel
.NET

Adding a template should not require rewriting the project creation architecture.

98. Template Acceptance Checklist

Before a template becomes active:

Metadata

Valid ID

Valid version

Name

Description

Language

Framework

Runtime type

Runtime image

Default ports

Commands

Files

Required files exist

No unsafe paths

README exists

.gitignore exists

No secrets

No unnecessary binaries

Runtime

Runtime starts

Dependencies install

Development server starts

Port is reachable

Health check succeeds

Runtime shuts down correctly

Testing

Template tests pass

Build succeeds

Security checks pass

Dependency scan passes

Clean-runtime test passes

99. Project Creation Definition of Done

A project created from a template is considered ready when:

Project exists
        +
Workspace exists
        +
Template files are complete
        +
Template version is recorded
        +
File metadata is synchronized
        +
Git state is valid
        +
Runtime can start

If runtime auto-start is enabled:

Runtime running
        +
Development server healthy
        +
Preview available

must also be true before reporting the workspace as fully ready.

100. Final Architecture

The final template architecture is:

                         RUNIX
                           │
                           ▼
                 Template Registry
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    Template ID       Version          Manifest
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                 Template Validator
                           │
                           ▼
                  Project Creation
                           │
                           ▼
                    Workspace
                           │
                           ▼
                 Template Materializer
                           │
                           ▼
                    User Files
                           │
                           ▼
                  Runtime Manager
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
        Node Runtime   Python Runtime   MERN Runtime
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                    Terminal / Preview

The critical security boundary remains:

RUNIX Control Plane
        │
        │ metadata / lifecycle
        ▼
Runtime Manager
        │
        │ controlled execution
        ▼
Isolated User Runtime
        │
        ▼
User Project

User project code must never execute directly on the RUNIX control-plane host.

101. Final Rules

The implementation must follow these rules:

Templates are versioned.
Published template versions are immutable.
The backend owns template resolution.
The frontend consumes template metadata from the backend.
The existing Stitch project remains the visual source of truth for template selection and workspace creation UI.
No generic replacement UI should be introduced.
Template files are materialized safely into the workspace.
Template creation must not execute arbitrary code on the control plane.
Dependencies are installed only inside isolated runtimes.
Runtime images are controlled and versioned.
User projects remain independent from future template updates.
Imported repositories are not overwritten by templates.
Secrets are never included in templates.
Template paths are validated against traversal.
Every active template must pass automated acceptance tests.
Runtime ports must be declared and/or discoverable.
Template failures must produce explicit error states.
No fake progress or fake runtime state may be shown in the UI.
Production runtime images should be immutable/pinned.
New templates must extend the registry rather than introducing custom project-creation logic.