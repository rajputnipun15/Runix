RUNIX GitHub Integration Specification

## 1. Purpose

RUNIX integrates with GitHub to allow users to:

- connect a GitHub account
- view accessible repositories
- import repositories into RUNIX
- create a RUNIX project from a repository
- clone repositories into a workspace
- inspect branches
- switch branches
- view Git status
- stage changes
- commit changes
- pull changes
- push changes
- create branches
- optionally create pull requests in a future phase

GitHub integration must preserve the separation between:

```text
RUNIX Control Plane
        │
        ├── Authentication
        ├── GitHub Integration
        ├── Project Metadata
        └── Runtime Management
                 │
                 ▼
RUNIX Execution Plane
        │
        └── Git repository inside workspace
2. Core Principle

GitHub is an external source-control provider.

RUNIX is not a replacement for GitHub.

Git remains the source of truth for repository history.

The RUNIX workspace contains a working copy of the repository.

GitHub Repository
       │
       │ clone / fetch
       ▼
RUNIX Workspace
       │
       ├── edit
       ├── test
       ├── build
       ├── commit
       └── push
       │
       ▼
GitHub Repository
3. GitHub Integration Architecture
                       Browser
                          │
                          ▼
                     RUNIX API
                          │
            ┌─────────────┴─────────────┐
            │                           │
            ▼                           ▼
     GitHub Integration             Git Service
            │                           │
            ▼                           ▼
       GitHub API                 Runtime Workspace
                                        │
                                        ▼
                                  .git directory

The browser must not directly manage GitHub access tokens.

4. Supported Provider

V1 provider:

GitHub

Future providers may include:

GitLab
Bitbucket
Azure DevOps

Do not implement additional providers until their requirements are defined.

5. Recommended Authentication Model

For production, RUNIX should prefer a:

GitHub App

over a broad OAuth token model.

Reasons:

granular permissions
repository-level access
better organization support
easier permission management
reduced token scope
installation-based access

OAuth may be used during development if necessary.

6. GitHub App Architecture

Conceptually:

User
 │
 ▼
RUNIX
 │
 │ GitHub App installation
 ▼
GitHub
 │
 ├── repository access
 ├── metadata access
 └── Git operations

RUNIX should request only permissions required by implemented features.

7. Required GitHub Permissions

Initial permissions should be minimal.

Potential repository permissions:

Contents:
Read and write

For metadata:

Metadata:
Read-only

Additional permissions must be requested only when a feature requires them.

Do not request:

organization administration
account administration
security administration
billing

unless a future feature explicitly requires them.

8. Environment Configuration

Example:

RUNIX_GITHUB_APP_ID=
RUNIX_GITHUB_PRIVATE_KEY=
RUNIX_GITHUB_CLIENT_ID=
RUNIX_GITHUB_CLIENT_SECRET=
RUNIX_GITHUB_WEBHOOK_SECRET=
RUNIX_GITHUB_CALLBACK_URL=

These are server-side secrets.

Never expose them to the browser.

Never include them in:

Git
logs
API responses
frontend bundles
runtime containers
audit metadata
9. GitHub Private Key

The GitHub App private key is highly sensitive.

It must:

remain server-side
be stored securely
never be sent to the browser
never be written to project workspaces
never be logged
never be committed to Git
be rotated when required

Production should use a dedicated secret-management mechanism where available.

10. User GitHub Connection

RUNIX should maintain GitHub integration metadata.

Example future table:

github_installations

Possible fields:

id
user_id
installation_id
account_id
account_login
account_type
created_at
updated_at

Do not store unnecessary GitHub account information.

11. Installation Flow

User selects:

Connect GitHub

Flow:

Browser
   │
   ▼
RUNIX
   │
   ▼
GitHub App Installation
   │
   ▼
GitHub
   │
   ▼
User approves repository access
   │
   ▼
GitHub
   │
   ▼
RUNIX Callback
   │
   ▼
Installation stored
12. GitHub Callback

Endpoint:

GET /api/v1/github/callback

The callback must validate:

state
authenticated session where applicable
installation information
signed parameters
expected provider flow

Never trust callback parameters without validation.

13. State Parameter

GitHub authorization flows must use a secure state value.

Purpose:

CSRF protection

The state should be:

cryptographically random
short-lived
tied to the initiating user/session
single-use

Invalid or expired state:

400 GITHUB_INVALID_STATE
14. Repository Listing

Endpoint:

GET /api/v1/github/repositories

Optional parameters:

?page=1
&page_size=30
&search=portfolio

Response:

{
  "data": {
    "items": [
      {
        "id": "123456",
        "name": "portfolio",
        "full_name": "username/portfolio",
        "private": true,
        "default_branch": "main",
        "html_url": "https://github.com/username/portfolio"
      }
    ],
    "page": 1,
    "page_size": 30,
    "total": 1
  },
  "error": null,
  "request_id": "req_001"
}
15. Repository Data

RUNIX should display:

repository name
owner
visibility
default branch
repository URL
last updated information where available

Do not expose:

GitHub installation tokens
private credentials
internal GitHub API responses
16. Repository Selection UI

Recommended UI:

Import from GitHub

Search repositories...

┌──────────────────────────────────────┐
│ portfolio                            │
│ username/portfolio                  │
│ Private • main                      │
│                         [Import]     │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ SkillForge                           │
│ username/SkillForge                 │
│ Private • main                      │
│                         [Import]     │
└──────────────────────────────────────┘

The actual RUNIX interface should follow the approved Stitch design.

17. Import Flow

User selects:

Import Repository

RUNIX performs:

1. authenticate user
2. authorize GitHub access
3. verify repository access
4. create RUNIX project
5. create workspace
6. queue import job
7. clone repository
8. verify repository
9. update Git metadata
10. mark project ready
18. Import Endpoint
POST /api/v1/projects/{project_id}/github/import

Request:

{
  "repository_id": "123456",
  "branch": "main"
}

Response:

202 Accepted
{
  "data": {
    "job_id": "uuid",
    "status": "queued"
  },
  "error": null,
  "request_id": "req_002"
}
19. Import Job

Repository import should be asynchronous.

Job:

github.import

Lifecycle:

queued
   ↓
running
   ↓
completed

Failure:

queued
   ↓
running
   ↓
failed
20. Import Process

Conceptual process:

GitHub
   │
   │ repository access
   ▼
Git Service
   │
   ▼
Workspace
   │
   ├── git init/clone
   ├── checkout branch
   └── verify repository

The Git operation must execute inside the controlled runtime or another isolated Git execution environment.

The API host should not execute arbitrary repository hooks or scripts.

21. Repository Trust Model

Imported repositories are untrusted.

A repository may contain:

package.json
requirements.txt
Makefile
Dockerfile
shell scripts
Git hooks
build scripts
postinstall scripts

RUNIX must NOT execute these automatically on the control-plane host.

22. Git Hooks

Repository Git hooks are untrusted.

Examples:

.git/hooks/pre-commit
.git/hooks/post-checkout
.git/hooks/post-merge

They must never execute on the RUNIX API host.

If Git operations occur inside the user runtime, hooks execute only inside that isolated runtime and remain subject to runtime resource and security policies.

23. Dependency Installation

Do not automatically execute:

npm install
pip install -r requirements.txt
pnpm install
yarn install
bundle install
make

during repository import unless explicitly configured.

If dependency installation is requested:

Browser
   ↓
RUNIX API
   ↓
Runtime Manager
   ↓
Isolated Runtime
   ↓
Dependency installation
24. Repository Initialization

For a new RUNIX project created from a template:

Create Workspace
      ↓
Create files
      ↓
git init
      ↓
initial branch

The initial branch should be configurable.

Default:

main
25. Git Repository Metadata

Table:

git_repositories

Example:

project_id
provider
repository_id
repository_url
owner_name
repository_name
default_branch
created_at
updated_at

The actual Git repository remains in:

/workspace/.git
26. Git Branch Metadata

Table:

git_branches

Stores known branch information.

Example:

main
feature/dashboard
feature/auth

Git itself remains the authoritative source for repository history and branch state.

27. Current Branch

RUNIX should obtain the actual current branch from Git.

Example:

git branch --show-current

Do not trust a database field as the sole source of truth for the current Git branch.

28. Git Status

Endpoint:

GET /api/v1/projects/{project_id}/git/status

Response:

{
  "data": {
    "branch": "main",
    "ahead": 1,
    "behind": 0,
    "staged": [
      "src/App.tsx"
    ],
    "modified": [
      "src/index.css"
    ],
    "untracked": [
      "src/components/Button.tsx"
    ],
    "deleted": []
  },
  "error": null,
  "request_id": "req_003"
}
29. Git Diff

Endpoint:

GET /api/v1/projects/{project_id}/git/diff

Optional:

?path=src/App.tsx

Response should contain structured diff information.

Example:

{
  "data": {
    "files": [
      {
        "path": "src/App.tsx",
        "status": "modified",
        "additions": 8,
        "deletions": 2
      }
    ]
  },
  "error": null,
  "request_id": "req_004"
}

The frontend may render a Monaco diff editor.

30. Git Staging

Endpoint:

POST /api/v1/projects/{project_id}/git/stage

Request:

{
  "paths": [
    "src/App.tsx",
    "src/index.css"
  ]
}

The backend must validate every path.

Never accept:

../../

or arbitrary filesystem paths.

31. Unstage

Endpoint:

POST /api/v1/projects/{project_id}/git/unstage

Request:

{
  "paths": [
    "src/App.tsx"
  ]
}
32. Commit

Endpoint:

POST /api/v1/projects/{project_id}/git/commit

Request:

{
  "message": "Add dashboard layout"
}

Validation:

message required
message length limited
repository must exist
user must have write permission
workspace must be available

Response:

{
  "data": {
    "commit_sha": "abc123..."
  },
  "error": null,
  "request_id": "req_005"
}
33. Commit Message Limits

Initial:

minimum: 1 character
maximum: 500 characters

The commit message must not contain control characters that could break logging or UI rendering.

34. Push

Endpoint:

POST /api/v1/projects/{project_id}/git/push

Response:

202 Accepted
{
  "data": {
    "job_id": "uuid",
    "status": "queued"
  },
  "error": null,
  "request_id": "req_006"
}

Push operations should be asynchronous.

35. Push Authentication

RUNIX must authenticate GitHub operations securely.

Possible mechanisms:

GitHub App installation token

or:

short-lived GitHub credential

The credential should be injected into the isolated runtime only for the duration required by the operation.

36. Credential Injection

Credentials must NOT be written permanently into:

.git/config

unless Git's credential mechanism is specifically configured securely.

Do not expose:

https://TOKEN@github.com/...

in logs or UI.

The credential mechanism must prevent accidental leakage.

37. Git Remote

Repository remote:

git remote -v

should not expose secrets.

Preferred remote form:

https://github.com/owner/repository.git

Credentials should be provided separately.

Never permanently store:

https://TOKEN@github.com/owner/repository.git

inside the repository configuration.

38. Pull

Endpoint:

POST /api/v1/projects/{project_id}/git/pull

Response:

202 Accepted

Pull should execute inside the runtime/workspace environment.

39. Pull Safety

A pull may cause conflicts.

RUNIX must detect:

merge conflicts
rebase conflicts
uncommitted changes

Do not automatically discard user changes.

If the workspace contains uncommitted changes:

409 WORKSPACE_HAS_UNCOMMITTED_CHANGES

unless the user explicitly requests a supported merge strategy.

40. Branch Listing

Endpoint:

GET /api/v1/projects/{project_id}/git/branches

Response:

{
  "data": {
    "current": "main",
    "branches": [
      {
        "name": "main",
        "remote": "origin/main",
        "is_current": true
      },
      {
        "name": "feature/dashboard",
        "remote": "origin/feature/dashboard",
        "is_current": false
      }
    ]
  },
  "error": null,
  "request_id": "req_007"
}
41. Create Branch

Endpoint:

POST /api/v1/projects/{project_id}/git/branches

Request:

{
  "name": "feature/dashboard"
}

Branch names must be validated.

42. Branch Name Validation

Reject unsafe or invalid branch names.

Do not accept:

../
refs/heads/
command injection
control characters

Git itself performs validation, but RUNIX should validate before invoking Git.

43. Checkout Branch

Endpoint:

POST /api/v1/projects/{project_id}/git/checkout

Request:

{
  "branch": "feature/dashboard"
}

Before checkout:

check workspace status
check uncommitted changes
confirm branch exists
lock workspace
perform checkout
refresh metadata
unlock workspace
44. Branch Checkout Conflicts

If uncommitted changes would be overwritten:

409 CHECKOUT_WOULD_OVERWRITE_CHANGES

The frontend should explain:

Your local changes would be overwritten by switching branches.
Commit or stash them first.

RUNIX must not silently delete changes.

45. Create Remote Branch

Future feature:

POST /projects/{project_id}/git/branches

with:

{
  "name": "feature/dashboard",
  "push": true
}

This should be implemented only after local branch management is stable.

46. Pull Request Support

Pull requests are V2+.

Future endpoint:

POST /api/v1/projects/{project_id}/github/pull-requests

Possible request:

{
  "title": "Add dashboard",
  "body": "Implements the RUNIX dashboard.",
  "head": "feature/dashboard",
  "base": "main"
}

Do not implement this as part of the initial Git integration milestone.

47. Repository Disconnect

User may disconnect GitHub.

Disconnecting GitHub should:

remove RUNIX GitHub connection metadata
invalidate applicable credentials

It should NOT automatically delete:

RUNIX projects
workspace files
local Git repository
commits
branches
48. Repository Unlink

A project can be unlinked from GitHub.

Result:

RUNIX project
   │
   └── local Git repository remains

The GitHub remote may be removed or disabled according to the user's explicit action.

Do not delete project source files.

49. GitHub Repository Deletion

RUNIX must not delete a GitHub repository as part of:

project deletion
GitHub disconnect
repository unlink

unless a separate future feature explicitly provides repository deletion and requires confirmation.

50. GitHub Repository Import Naming

When importing:

username/portfolio

default project name:

portfolio

If a project with that name already exists, RUNIX may suggest:

portfolio-1

or allow the user to choose another name.

Do not overwrite an existing project automatically.

51. Import Existing Project

User flow:

Dashboard
   ↓
New Project
   ↓
Import from GitHub
   ↓
Connect GitHub
   ↓
Select repository
   ↓
Select branch
   ↓
Choose project name
   ↓
Import
   ↓
Workspace created
   ↓
Repository cloned
   ↓
Project ready
52. Import Progress

The UI should display:

Importing repository...

✓ Connecting to GitHub
✓ Creating workspace
✓ Cloning repository
✓ Checking out main
✓ Indexing files
✓ Configuring project

Repository ready.

Progress should come from actual job state.

Never display fake progress.

53. Import Job Events

Future WebSocket or Server-Sent Events may provide:

{
  "type": "job_progress",
  "job_id": "uuid",
  "stage": "cloning",
  "message": "Cloning repository..."
}

Stages:

connecting
creating_workspace
cloning
checking_out
indexing
finalizing
completed
54. Import Failure

Possible failures:

GITHUB_ACCESS_DENIED
REPOSITORY_NOT_FOUND
REPOSITORY_IMPORT_FAILED
BRANCH_NOT_FOUND
WORKSPACE_CREATION_FAILED
GIT_CLONE_FAILED
STORAGE_LIMIT_EXCEEDED

User-facing message:

Repository import failed.

Your existing RUNIX projects were not modified.
55. Repository Size Limits

Very large repositories can consume significant resources.

Initial policy should enforce configurable limits:

maximum repository size
maximum file count
maximum single file size

Example:

RUNIX_MAX_IMPORT_SIZE_BYTES=2147483648
RUNIX_MAX_IMPORT_FILES=50000

If exceeded:

413 REPOSITORY_TOO_LARGE
56. Git LFS

Git LFS may be encountered in imported repositories.

V1 behavior:

detect Git LFS

If unsupported:

GIT_LFS_UNSUPPORTED

The UI should explain the limitation.

Do not silently create incomplete repositories.

Future versions may support Git LFS explicitly.

57. Submodules

Repositories may contain:

.gitmodules

V1 should detect submodules.

Do not automatically fetch arbitrary submodules unless supported.

Possible behavior:

Repository contains Git submodules.

Submodule initialization is not enabled for this project.

Future support can provide controlled submodule initialization.

58. Git Hooks Security

During import:

.git/hooks/

must not be executed on the control plane.

When Git operations run inside a runtime, hooks remain untrusted code.

They execute with:

runtime CPU limit
runtime memory limit
runtime process limit
runtime network policy
59. Git Config Security

Do not allow repository-level Git configuration to override RUNIX security settings.

Be careful with:

core.sshCommand
core.fsmonitor
credential.helper
protocol.*
url.*

RUNIX must control how credentials and network access are handled.

60. SSH Git URLs

Repositories may use:

git@github.com:owner/repository.git

V1 should prefer HTTPS-based Git operations through the GitHub integration.

SSH support can be added later with dedicated ephemeral credentials.

Never expose user SSH private keys to runtimes automatically.

61. GitHub API Rate Limits

GitHub APIs have rate limits.

RUNIX should:

cache repository metadata briefly
paginate repository lists
avoid unnecessary polling
handle 429 and rate-limit responses
surface actionable errors

Example:

GitHub API rate limit reached.
Please try again later.
62. GitHub API Errors

Map external errors to RUNIX errors.

Examples:

401 → GITHUB_AUTHENTICATION_FAILED
403 → GITHUB_ACCESS_DENIED
404 → GITHUB_REPOSITORY_NOT_FOUND
409 → GITHUB_CONFLICT
422 → GITHUB_VALIDATION_ERROR
429 → GITHUB_RATE_LIMITED
5xx → GITHUB_UNAVAILABLE

Do not expose raw GitHub internal response bodies to users.

63. Git Service Architecture

Recommended:

backend/app/git/
├── __init__.py
├── service.py
├── repository.py
├── commands.py
├── status.py
├── branches.py
├── diff.py
├── credentials.py
└── exceptions.py

Git commands should be encapsulated.

64. GitHub Service Architecture

Recommended:

backend/app/integrations/github/
├── __init__.py
├── client.py
├── auth.py
├── installations.py
├── repositories.py
├── imports.py
├── webhooks.py
├── models.py
└── exceptions.py

The GitHub service should handle GitHub API communication.

The Git service should handle repository operations.

Do not mix provider API logic with local Git command logic.

65. Git Command Execution

Local Git operations may be executed inside the runtime.

Example:

git status
git diff
git add
git commit
git branch
git checkout
git pull
git push

The Runtime Manager controls execution.

The API should never directly execute arbitrary Git commands on the host.

66. Command Construction

Never construct Git commands using raw string concatenation.

Bad:

command = f"git checkout {branch}"

Safer conceptual approach:

command = [
    "git",
    "checkout",
    "--",
    branch,
]

The actual implementation must use safe subprocess argument handling.

67. Git Output

Git output may contain:

file paths
branch names
commit messages
remote information
errors

Treat all output as untrusted text.

Do not render it as raw HTML.

68. Audit Events

GitHub-related audit events:

github.connected
github.disconnected
github.repository_import_started
github.repository_import_completed
github.repository_import_failed
github.push
github.pull
github.branch_created
github.branch_checkout

Git-related events:

git.commit
git.push
git.pull
git.checkout
git.branch_created
git.stage
git.unstage

Do not store:

tokens
private keys
credential values

in audit metadata.

69. GitHub Webhooks

Future webhook endpoint:

POST /api/v1/github/webhooks

Possible events:

push
pull_request
repository
installation
installation_repositories

Webhook signatures must be verified.

Never trust an unsigned GitHub webhook payload.

70. Webhook Security

GitHub webhook requests must be verified using the configured webhook secret.

Invalid signature:

401 GITHUB_WEBHOOK_INVALID

Webhook processing should be asynchronous.

Do not perform long-running operations directly inside the HTTP webhook request.

71. Push Synchronization

Future behavior:

GitHub push
   ↓
Webhook
   ↓
RUNIX
   ↓
Repository state notification

The UI may show:

Remote branch updated.

RUNIX must not automatically overwrite local changes.

72. Local vs Remote State

RUNIX must clearly distinguish:

local working tree
local branch
remote branch

Example:

main

Local:
1 commit ahead

Remote:
0 commits ahead

Do not represent this as a single ambiguous status.

73. Conflict Handling

If a pull results in conflicts:

MERGE_CONFLICT

The UI should show:

Merge conflicts detected.

Files:
- src/App.tsx
- package.json

[Open Conflict Editor]

Future conflict resolution can use Monaco's diff/merge editor.

74. Git Credentials Lifecycle

Credential lifecycle:

request credential
      ↓
generate/obtain short-lived credential
      ↓
use for Git operation
      ↓
credential expires
      ↓
remove temporary credential

Credentials should have the shortest practical lifetime.

75. Credential Revocation

When a GitHub integration is disconnected:

invalidate installation/session credentials

When a user loses repository permission:

GitHub operation fails
       ↓
RUNIX refreshes authorization
       ↓
user prompted if required
76. Browser Security

The browser should receive:

repository metadata
branch metadata
Git status
diff
job status

The browser should NOT receive:

GitHub App private key
GitHub installation private credentials
raw access tokens
credential helper secrets
77. V1 Scope

V1 GitHub integration must support:

GitHub connection
repository listing
repository search
repository import
branch selection
workspace clone
Git status
Git diff
staging
unstaging
commit
push
pull
branch listing
local branch creation
branch checkout
credential protection
GitHub error handling
audit logging
78. V1 Non-Goals

Do not implement initially:

GitLab
Bitbucket
GitHub repository deletion
full pull request management
GitHub Actions management
GitHub Issues management
GitHub Discussions
GitHub Codespaces integration
SSH credential management
Git LFS
automatic submodule management
advanced merge conflict automation

These are separate features.

79. Acceptance Criteria

GitHub integration is V1-ready when:

A user can connect GitHub.
RUNIX can list accessible repositories.
Repository search works.
A repository can be selected for import.
RUNIX creates a project and workspace.
The repository is cloned into the workspace.
The selected branch is checked out.
Git metadata is stored.
The repository appears in Source Control.
Git status works.
Git diff works.
Files can be staged.
Files can be unstaged.
Commits can be created.
Changes can be pushed.
Changes can be pulled.
Branches can be listed.
Branches can be created.
Branches can be checked out.
Uncommitted changes are protected from accidental overwrite.
GitHub credentials never appear in browser responses.
GitHub credentials never appear in logs.
Imported repositories never execute code on the API host.
Git operations execute inside the controlled runtime.
Repository import is asynchronous.
Large repositories are subject to resource limits.
GitHub API failures are handled gracefully.
Audit events are generated for important Git/GitHub operations.
80. Security Rules

These rules are mandatory.

Rule 1

Never expose GitHub credentials to the browser.

Rule 2

Never store raw GitHub tokens in PostgreSQL.

Rule 3

Never write GitHub credentials into project source files.

Rule 4

Never execute repository scripts on the RUNIX API host.

Rule 5

Never trust repository contents.

Rule 6

Never automatically execute dependency installation during import without explicit controlled execution.

Rule 7

Never automatically delete local changes during pull or checkout.

Rule 8

Never store credentials in Git remote URLs.

Rule 9

Never allow Git operations to bypass runtime security.

Rule 10

Never trust GitHub webhook payloads without signature verification.

81. Final Architecture
                         RUNIX
                           │
                           ▼
                    GitHub Integration
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
          GitHub API                Git Service
              │                         │
              │                         ▼
              │                   Runtime Manager
              │                         │
              │                         ▼
              │                    Isolated Runtime
              │                         │
              │                         ▼
              │                     Workspace
              │                         │
              │                        .git
              │
              ▼
       Repository Metadata
              │
              ▼
          PostgreSQL

GitHub provides remote repository access.

Git provides version control.

The RUNIX workspace provides the working tree.

The runtime provides isolated execution.

The RUNIX API coordinates the entire workflow.