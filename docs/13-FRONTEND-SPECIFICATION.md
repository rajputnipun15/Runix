# RUNIX — Frontend Specification

**Document:** 13-FRONTEND-SPECIFICATION.md  
**Product:** RUNIX  
**Status:** Implementation Specification  
**Version:** 1.0  
**Last Updated:** 2026-09-29

---

# 1. Purpose

This document defines the frontend architecture, application structure, UI behavior, component system, interaction model, responsive behavior, and implementation requirements for RUNIX.

The frontend implementation MUST be based on the existing **RUNIX Stitch project**.

The Stitch project is the primary visual reference for:

- Layout
- Page hierarchy
- Component placement
- Navigation
- Typography
- Spacing
- Colors
- Borders
- Radius
- Icons
- Buttons
- Panels
- Cards
- Tables
- Editor layout
- Terminal layout
- AI panel
- Runtime indicators
- Responsive behavior
- Interaction patterns
- Empty states
- Loading states
- Error states

The frontend implementation must not replace the Stitch design with a generic SaaS dashboard.

---

# 2. Frontend Source of Truth

The implementation priority is:

```text
RUNIX Product Requirements
        ↓
RUNIX Architecture
        ↓
RUNIX Functional Requirements
        ↓
RUNIX Stitch Project
        ↓
Frontend Implementation

For visual decisions:

Stitch
  ↓
Component implementation
  ↓
RUNIX design tokens

If the developer encounters a visual decision that is not explicitly defined in the technical documentation, the existing Stitch design should be inspected before inventing a new pattern.

3. Stitch Implementation Rule

The Stitch project represents the intended RUNIX product experience.

The developer MUST preserve:

Existing layout hierarchy.
Existing navigation structure.
Existing visual proportions.
Existing typography hierarchy.
Existing panel relationships.
Existing spacing rhythm.
Existing interaction patterns.
Existing visual density.
Existing responsive intent.

Do not redesign the interface during implementation unless explicitly requested.

4. Product Identity
Product
RUNIX
Tagline
Build. Run. Ship. Anywhere.
Product category
Browser-based cloud development platform
Cloud IDE
Developer infrastructure platform
5. Frontend Technology

The frontend uses:

Next.js
React
TypeScript
Tailwind CSS
Monaco Editor
xterm.js
Playwright
Vitest

Recommended supporting libraries:

React Query / TanStack Query
Zod
React Hook Form
Lucide React or approved icon system

Libraries should only be added when they solve a real implementation requirement.

Do not add dependencies merely to reproduce simple UI behavior.

6. Application Structure

Recommended frontend structure:

frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   │
│   ├── login/
│   │   └── page.tsx
│   │
│   ├── register/
│   │   └── page.tsx
│   │
│   ├── dashboard/
│   │   └── page.tsx
│   │
│   ├── projects/
│   │   ├── page.tsx
│   │   ├── new/
│   │   │   └── page.tsx
│   │   └── [projectId]/
│   │       ├── page.tsx
│   │       ├── settings/
│   │       │   └── page.tsx
│   │       └── source-control/
│   │           └── page.tsx
│   │
│   └── settings/
│       └── page.tsx
│
├── components/
│   ├── ui/
│   ├── layout/
│   ├── dashboard/
│   ├── project/
│   ├── editor/
│   ├── terminal/
│   ├── preview/
│   ├── runtime/
│   ├── git/
│   ├── ai/
│   └── feedback/
│
├── features/
│   ├── auth/
│   ├── projects/
│   ├── workspace/
│   ├── runtime/
│   ├── terminal/
│   ├── preview/
│   ├── git/
│   ├── github/
│   └── agent/
│
├── hooks/
├── lib/
├── services/
├── types/
├── stores/
├── styles/
└── tests/

The actual directory structure may be adapted to the implementation, but responsibilities must remain clearly separated.

7. Application Shell

RUNIX has two primary frontend environments.

Marketing / Public Environment
Landing
Login
Register
Authentication flows
Application Environment
Dashboard
Projects
Cloud IDE
Settings
Source Control
Runtime
AI
8. Public Landing Page

The landing page should communicate:

RUNIX

Build. Run. Ship. Anywhere.

A browser-based development environment
for building and running software in the cloud.

The landing page should follow the visual language established by Stitch.

Primary actions:

Get Started
Sign In

Secondary content may include:

Cloud development
Isolated runtimes
Integrated terminal
Live preview
GitHub integration
AI coding agent
9. Authentication Screens

Required screens:

Login
Register
Forgot Password
Reset Password

Authentication screens must follow the Stitch design.

They should not introduce a separate visual language.

10. Login Page

Required elements:

RUNIX branding
Email
Password
Show/hide password
Remember/session option if supported
Sign In
Forgot password
Register link

Optional:

Continue with GitHub

if GitHub authentication is configured.

11. Register Page

Required:

Name
Email
Password
Confirm password
Create account
Login link

Validation must be displayed inline.

Examples:

Invalid email address.
Password must contain at least 12 characters.
Passwords do not match.
Email already registered.
12. Dashboard

The dashboard is the main project-management environment.

It should contain:

Global navigation
User profile
Project list
Create project
Recent projects
Project status
Runtime status where appropriate

The dashboard must follow the hierarchy established in Stitch.

13. Dashboard Information Architecture

Conceptually:

RUNIX
│
├── Dashboard
├── Projects
├── GitHub
├── Settings
│
└── User

The exact visual navigation arrangement must follow the Stitch design.

14. Project Cards

A project card may display:

Project name
Description
Template
Runtime status
Last modified
Git branch
GitHub repository

Possible status:

Running
Stopped
Starting
Failed

Project cards must remain visually compact.

Avoid unnecessarily oversized cards.

15. Create Project

Create-project flow must support:

Blank project
React + Vite + TypeScript
Node.js + TypeScript
Python + FastAPI
MERN
Blank Docker environment

The user should be able to:

Choose template
Enter project name
Choose visibility
Create project
16. Create Project UX

Flow:

Create Project
      ↓
Select Template
      ↓
Project Details
      ↓
Create
      ↓
Workspace Initialization
      ↓
IDE

Loading state:

Creating workspace...
Preparing runtime...
Initializing project...

The frontend must not claim the project is ready until the API confirms creation.

17. Main Cloud IDE

The cloud IDE is the primary RUNIX experience.

The layout should be based directly on the Stitch project.

Conceptual structure:

┌─────────────────────────────────────────────────────────────┐
│ RUNIX / Project / Branch     Runtime   Run   Test   User   │
├────────────┬───────────────────────────────┬───────────────┤
│            │                               │               │
│ Explorer   │        Monaco Editor          │   RUNIX AI    │
│            │                               │               │
│ Search     │                               │               │
│ Source     │                               │               │
│ Control    │                               │               │
│ Extensions │                               │               │
│ Settings   │                               │               │
│            │                               │               │
├────────────┴───────────────────────────────┴───────────────┤
│ Terminal | Problems | Output | Tests | Logs | Preview       │
└─────────────────────────────────────────────────────────────┘

This is an architectural representation.

The actual dimensions, spacing, colors, typography, and component styling MUST follow Stitch.

18. IDE Top Bar

The top bar should provide access to:

RUNIX
Project name
Branch
Runtime status
Save state
Run
Stop
Restart
Test
Deploy
User profile

Not every action needs to be visible at all viewport sizes.

Secondary actions may move into menus.

19. Project Breadcrumb

The editor should provide project context.

Example:

RUNIX
/
my-project
/
src
/
components
/
Button.tsx

The breadcrumb must reflect the currently active file.

20. Runtime Indicator

The top bar should display runtime status.

Examples:

● Running
○ Stopped
◌ Starting
⚠ Failed

The status indicator should use the RUNIX design-system colors defined by Stitch.

Do not invent a new status color palette.

21. Runtime Actions

Available actions depend on state.

Stopped
Start
Starting
Starting...
Running
Restart
Stop
Failed
Restart
View logs

The frontend must disable invalid actions.

22. Save State

The editor should communicate save status.

States:

Saved
Saving...
Unsaved changes
Save failed
Conflict

Example:

✓ Saved

or:

● Unsaved changes
23. File Explorer

The left sidebar contains the project explorer.

Requirements:

Folders
Files
Expand/collapse
Create file
Create folder
Rename
Delete
Search
Refresh

The explorer must support nested directories.

24. Explorer Interaction

Clicking a file:

Explorer
 ↓
Open editor tab
 ↓
Load content

Double-click behavior may follow the interaction established in Stitch.

25. Explorer Context Menu

Possible actions:

Open
Rename
Delete
Copy path
Copy relative path
New file
New folder

Destructive operations require confirmation where appropriate.

26. File Icons

File icons should be consistent.

Examples:

.ts
.tsx
.js
.jsx
.py
.json
.md
.css
.html
.env

Use a single coherent icon system.

Do not introduce unrelated icon styles.

27. File Search

The explorer should provide file search.

Requirements:

Search by filename
Filter
Keyboard navigation
Open result

Suggested shortcut:

Ctrl/Cmd + P
28. Global Code Search

Suggested shortcut:

Ctrl/Cmd + Shift + F

Search should support:

Text
File path
Case sensitivity
Regex where supported

Search results should display:

File
Line
Code preview
29. Monaco Editor

The center editor uses Monaco.

Required features:

Syntax highlighting
Line numbers
Code folding
Minimap
Autocomplete
Diagnostics
Multiple tabs
Breadcrumbs
Find
Replace
Keyboard shortcuts
30. Editor Tabs

Tabs display:

Filename
Modified state
Close action

Example:

● App.tsx
  index.css
  package.json

The modified indicator must be visually subtle and consistent with Stitch.

31. Editor State

The frontend must distinguish:

Local unsaved content
Server-saved content
Runtime-modified content
Conflicting content
32. Editor Conflict

If a file changes externally:

Current editor state
        ↓
Server detects changed hash
        ↓
409 FILE_CHANGED
        ↓
Conflict UI

The UI should provide:

Reload
Compare
Keep Local

where supported.

Never silently overwrite user changes.

33. Editor Diagnostics

Display:

Errors
Warnings
Hints

Diagnostics may originate from:

TypeScript
ESLint
Python tooling
Runtime
Tests
34. Editor Command Palette

RUNIX should provide:

Ctrl/Cmd + K

or the exact shortcut defined by Stitch.

Commands:

Create Project
Open Project
Start Runtime
Stop Runtime
Restart Runtime
Run Tests
Open Terminal
Open Preview
Toggle AI
Import GitHub
Commit
Push
Pull
Open Settings
35. Command Palette Design

The command palette must use the same:

Typography
Radius
Shadow
Border
Spacing
Icon treatment

as the Stitch design.

It should feel like part of RUNIX rather than a separate component library.

36. Terminal

The terminal is located in the bottom panel.

Technology:

xterm.js

Terminal communication:

Browser
 ↓
WebSocket
 ↓
Terminal Service
 ↓
Runtime Manager
 ↓
PTY
 ↓
Container
37. Terminal Tabs

Possible terminal tabs:

Terminal 1
Terminal 2
Terminal 3

Actions:

New terminal
Close terminal
Restart terminal
Clear

Connection status should be visible.

38. Terminal States
Connecting
Connected
Disconnected
Reconnecting
Runtime unavailable

Example:

Connecting to runtime...
39. Terminal Output

Terminal output must be rendered as terminal content.

Do not convert terminal output into generic HTML cards.

ANSI formatting should be supported where xterm.js provides it.

40. Bottom Panel

The bottom panel should contain tabs for:

Terminal
Problems
Output
Tests
Logs
Preview

The exact order and visual presentation should follow Stitch.

41. Problems Panel

Display:

Errors
Warnings
File
Line
Column
Message

Clicking an error should open the associated file and line.

42. Output Panel

Display:

Build output
Run output
Command output
Tool output

Output should be scrollable and searchable where useful.

43. Tests Panel

The Tests panel should show:

Test suite
Test count
Passed
Failed
Skipped
Duration

Example:

Tests
────────────────────
24 passed
2 failed
1 skipped

Duration
4.21s
44. Test Interaction

Actions:

Run all
Run failed
Run file
Run test
Stop

Results should link to source files where possible.

45. Preview Panel

Preview should display the running development application.

The preview architecture is:

Runtime
 ↓
Detected Port
 ↓
Preview Gateway
 ↓
Authenticated Preview
 ↓
Browser Panel
46. Preview States
Waiting for runtime
Starting server
Detecting port
Preview ready
Preview unavailable
Server stopped
47. Preview Controls

Possible controls:

Refresh
Open externally
Copy preview URL
Open DevTools where supported

The preview must respect project authorization.

48. Runtime Panel

Runtime information should include:

Runtime type
Runtime image
Status
CPU
Memory
Storage
Process count
Ports
Container health

Example:

Node.js 22
Running

CPU
32%

Memory
418 MB / 1 GB

Storage
620 MB / 2 GB

Port
5173

Preview
Ready

The exact visual design follows Stitch.

49. Runtime Detail View

The user should be able to inspect:

Runtime status
Resources
Ports
Processes
Logs
Start time
Last activity

Administrative/internal container IDs should not be unnecessarily exposed.

50. Git Source Control Panel

The Source Control UI should display:

Changed files
Staged files
Unstaged files
Deleted files
Added files

Example:

SOURCE CONTROL

Changes
  M src/App.tsx
  M src/index.css
  A src/components/Button.tsx
51. Git Diff

Selecting a file opens a diff.

Display:

Added lines
Removed lines
Modified lines

The diff should be syntax-aware where possible.

52. Git Actions

Supported:

Stage
Unstage
Commit
Push
Pull
Branch
Checkout

Commit requires:

Commit message

Push should require explicit user interaction.

53. GitHub Integration UI

GitHub flows include:

Connect GitHub
Import repository
Select repository
Select branch
Import

Connection state:

Connected
Not connected
Authorization required
54. GitHub Repository Picker

The picker should display:

Repository name
Owner
Visibility
Default branch
Updated time

Search should be supported.

55. AI Agent Panel

The AI Agent panel is a major RUNIX feature.

It should be integrated into the IDE rather than presented as a generic chatbot.

The design must follow the existing Stitch AI panel.

56. AI Agent Panel Structure

Conceptually:

┌──────────────────────────────┐
│ RUNIX AI                     │
│ Coding Agent                 │
├──────────────────────────────┤
│ Task                         │
│                              │
│ Fix the login redirect bug   │
│                              │
├──────────────────────────────┤
│ Context                      │
│ 3 files • auth • tests       │
├──────────────────────────────┤
│ Plan                         │
│ ✓ Inspect login              │
│ ✓ Inspect middleware         │
│ ○ Prepare changes            │
│ ○ Run tests                  │
├──────────────────────────────┤
│ Tool Activity                │
│ ✓ search_code                │
│ ✓ read_file                  │
│ ○ update_file                │
├──────────────────────────────┤
│ Changes                      │
│ 2 files   +18 -7             │
│                              │
│ [Review Diff]                │
├──────────────────────────────┤
│ [Approve] [Reject]           │
└──────────────────────────────┘

This structure is conceptual.

The actual dimensions and styling must come from Stitch.

57. AI Agent Input

The AI input should support:

Natural-language request
Selected code context
Current file context
Project context

Example:

Fix the authentication redirect in this file.
58. AI Context Indicator

The panel should communicate what the agent is using.

Example:

Context

3 files
1 test suite
Current branch: main
Runtime: Running

This provides transparency without exposing hidden reasoning.

59. AI Plan

The agent should display concise plans.

Example:

Plan

1. Inspect session middleware.
2. Trace redirect behavior.
3. Prepare minimal fix.
4. Add regression test.
5. Run authentication tests.
60. AI Tool Activity

Show concise activity:

Reading auth/session.ts
Searching redirect handlers
Inspecting Git status
Preparing patch
Running tests

Do not expose hidden chain-of-thought.

61. AI Diff

When changes are ready:

Changes ready

2 files
+18
-7

[Review Diff]

The user must be able to inspect the patch before applying significant changes.

62. AI Approval

Approval UI must communicate:

What changes
Why
Files affected
Risk
Tests

Buttons:

Approve
Reject
Review
63. AI Statuses

Display:

Queued
Analyzing
Planning
Waiting for approval
Executing
Testing
Completed
Failed
Cancelled
64. AI Empty State

If AI is not configured:

RUNIX AI

Your coding agent is not configured yet.

Configure an AI provider to enable
repository-aware coding assistance.

Do not show fake responses.

65. Notifications

RUNIX should provide lightweight notifications for:

Project created
Runtime started
Runtime stopped
Runtime failed
File saved
Git push completed
Test completed
AI task completed
AI approval required
Deployment completed

Notifications must not obstruct development unnecessarily.

66. Toast Behavior

Toasts should:

Be concise.
Provide meaningful status.
Support dismissal.
Avoid duplicate messages.
Avoid blocking editor interaction.

Example:

✓ Changes saved
67. Loading States

Every asynchronous UI operation should have a clear loading state.

Examples:

Creating project...
Loading files...
Starting runtime...
Connecting terminal...
Importing repository...
Running tests...
Preparing changes...
68. Skeleton Loading

Skeleton loaders should be used where they improve perceived performance.

Avoid excessive skeleton animation.

Follow the motion and loading treatment established by Stitch.

69. Error States

Errors should be:

Specific
Actionable
Recoverable where possible

Example:

Runtime unavailable

The project runtime could not be started.

[Retry]
[View Logs]
70. Empty States

Examples:

No Projects
No projects yet.

Create your first RUNIX project.

[Create Project]
No Git Changes
Working tree clean.
No Tests
No test results yet.
No Terminal
Start a terminal session to begin.
71. Settings

Settings should include:

Profile
Account
Security
AI
GitHub
Appearance
Editor
Runtime preferences

The exact grouping should follow Stitch.

72. Profile Settings

Fields:

Display name
Email
Avatar

Email verification state should be visible where applicable.

73. Security Settings

Include:

Change password
Active sessions
Logout other sessions

Future:

MFA
Passkeys
74. AI Settings

Possible settings:

AI provider
Model
Agent permissions
Approval behavior
Token/usage information

Sensitive API keys must not be rendered after saving.

75. Appearance Settings

Potential controls:

Theme
Editor theme
Density
Reduced motion

The default theme should match Stitch.

76. Responsive Design

RUNIX is primarily a desktop developer environment.

Responsive behavior must preserve usability rather than simply shrinking the desktop layout.

77. Desktop

Desktop should provide the full IDE:

Explorer
Editor
AI
Bottom panel
Top bar

Resizable panels should be supported.

78. Laptop

On smaller laptop widths:

Explorer remains
Editor remains primary
AI may collapse
Bottom panel remains accessible

Secondary panels can become toggleable.

79. Tablet

Tablet mode should prioritize:

Project navigation
Editor
Terminal

The AI and secondary panels may become overlays/drawers.

80. Mobile

The full IDE does not need to behave as a desktop IDE on mobile.

Mobile should prioritize:

Projects
Project details
Runtime status
Git status
AI task management

Full Monaco editing may be limited or intentionally unsupported.

The UI should clearly communicate when a feature requires a larger viewport.

81. Panel Resizing

Desktop panels should support resizing where defined by Stitch.

Potential panels:

Explorer
Editor
AI
Terminal
Preview

Minimum widths must prevent unusable layouts.

82. Panel Persistence

Panel state may persist per user/project.

Examples:

Explorer width
AI panel open/closed
Terminal height
Preview state

Persist only non-sensitive UI state.

83. Keyboard Navigation

RUNIX is a developer product and should have strong keyboard support.

Core shortcuts:

Ctrl/Cmd + P
File search

Ctrl/Cmd + Shift + F
Code search

Ctrl/Cmd + K
Command palette

Ctrl/Cmd + S
Save

Ctrl/Cmd + `
Terminal

Ctrl/Cmd + B
Toggle sidebar where supported

Exact shortcuts must not conflict with Monaco/browser behavior.

84. Keyboard Accessibility

All interactive controls must support:

Tab
Shift + Tab
Enter
Space
Escape
Arrow keys where appropriate

Focus must remain visible.

85. Accessibility

RUNIX should target WCAG 2.2 AA where practical.

Requirements:

Keyboard navigation.
Visible focus.
Semantic HTML.
Accessible labels.
Sufficient contrast.
Screen-reader compatible controls.
Reduced motion support.
Error announcements.
Modal focus trapping.
86. Reduced Motion

When reduced-motion preference is enabled:

Disable unnecessary animations
Reduce transitions
Avoid large motion effects

Editor functionality must remain unchanged.

87. Typography

Typography must follow Stitch.

The implementation should define tokens for:

Display
Heading
Body
Label
Caption
Code
Terminal

Use a consistent developer-oriented type hierarchy.

88. Monospace Typography

Monospace should be used for:

Code
Terminal
File paths
Commands
Git hashes
Technical metadata

Do not use monospace for normal UI text unless the Stitch design explicitly does so.

89. Color System

The RUNIX visual system should use the palette established in Stitch.

The implementation should convert the Stitch visual palette into semantic tokens:

background
surface
surface-elevated
border
text-primary
text-secondary
text-muted
accent
success
warning
error
info

Do not independently invent a new palette.

90. Dark Interface

The core RUNIX application uses a deep developer-oriented dark interface.

The implementation should maintain:

High contrast
Layered surfaces
Subtle borders
Controlled accent color
Readable code
Clear status indicators

Avoid excessive gradients and neon effects.

91. Borders

Borders should be subtle and structural.

Use them to distinguish:

Panels
Inputs
Tabs
Cards
Editor regions
Terminal

Do not add borders to every element.

92. Radius

Component radius must follow Stitch.

Do not globally apply large rounded corners.

Developer tooling should remain precise and compact.

93. Shadows

Use shadows sparingly.

Preferred hierarchy:

Flat
↓
Subtle elevation
↓
Modal elevation

Avoid heavy floating-card effects.

94. Glass Effects

Glass/transparency may be used only where Stitch uses it.

Do not convert the entire interface into glassmorphism.

95. Icons

Icons must be:

Consistent
Recognizable
Compact
Accessible

Icons should not replace text labels where the action is ambiguous.

96. Buttons

Button variants should include:

Primary
Secondary
Ghost
Danger
Icon

All variants must follow Stitch styling.

97. Button States

Every button should support:

Default
Hover
Active
Focus
Disabled
Loading

Loading buttons should prevent duplicate submissions.

98. Inputs

Inputs should support:

Default
Focus
Error
Disabled
Read-only
Loading

Validation messages should be associated with the input.

99. Modals

Modals should be reserved for actions requiring focused attention.

Examples:

Delete project
Delete file
Approval request
Git commit
Runtime configuration
Import repository

Avoid using modals for routine navigation.

100. Dropdowns

Dropdowns should support:

Keyboard navigation
Search where needed
Escape to close
Click outside
Focus restoration
101. Tooltips

Tooltips should explain unfamiliar icon-only actions.

Examples:

Restart runtime
Open preview
Copy path
Toggle AI

Do not use tooltips for information already visible.

102. Data Fetching

Server state should use a predictable data-fetching architecture.

Recommended:

TanStack Query

Responsibilities:

Caching
Refetching
Mutation state
Error handling
Loading state
Invalidation
103. API Client

Create a centralized API client.

Example:

lib/api/
├── client.ts
├── auth.ts
├── projects.ts
├── files.ts
├── runtime.ts
├── git.ts
├── github.ts
├── tests.ts
└── agent.ts

Components should not construct raw fetch requests everywhere.

104. Authentication State

The frontend should expose:

authenticated user
session state
loading state
logout

Protected pages should redirect unauthenticated users.

Server-side protection remains mandatory.

105. Project State

Project state may include:

project metadata
workspace status
runtime status
Git status
active branch

Avoid storing duplicate server state unnecessarily.

106. Editor State

Editor state should contain:

open tabs
active file
local content
dirty state
cursor position
selection
editor settings

Large file content should not be unnecessarily duplicated across global state stores.

107. Runtime State

Runtime state:

status
resource usage
ports
health
last activity

Runtime updates may arrive through WebSocket events.

108. WebSocket Architecture

WebSockets should be encapsulated.

Example:

services/
└── websocket/
    ├── terminal.ts
    ├── agent.ts
    └── runtime.ts

Components should consume structured events rather than directly managing raw WebSocket messages.

109. WebSocket Reconnection

Reconnect using exponential backoff.

Example:

1s
2s
4s
8s
16s

with a maximum delay.

Stop retrying when:

authentication expired
project access revoked
runtime terminated
user closes connection
110. Optimistic UI

Optimistic updates may be used for low-risk UI operations.

Do not use optimistic updates for high-impact operations such as:

Delete project
Delete file
Git push
Deploy
Runtime termination

unless rollback behavior is fully implemented.

111. File Saving

Preferred flow:

Editor
 ↓
Debounce / explicit save
 ↓
API
 ↓
Hash validation
 ↓
Workspace service
 ↓
Saved
 ↓
UI status update
112. Autosave

Autosave behavior must match the intended Stitch/product UX.

If enabled:

User stops typing
 ↓
Debounce
 ↓
Save

If disabled:

Ctrl/Cmd + S
 ↓
Save

The choice must be explicit in implementation.

113. File Conflict UX

When conflict occurs:

File changed externally.

Provide:

Compare
Reload
Keep local

Never silently discard content.

114. Runtime Live Updates

Runtime state should update without full-page reload.

Possible events:

runtime.created
runtime.starting
runtime.running
runtime.stopping
runtime.stopped
runtime.failed
runtime.terminated
115. Preview Port Detection

When a runtime exposes a development server:

Runtime
 ↓
Port detected
 ↓
Frontend receives port event
 ↓
Preview becomes available

Do not assume that every project uses port 3000.

116. Project Loading Sequence

When opening a project:

Load project metadata
        ↓
Load workspace tree
        ↓
Load Git status
        ↓
Load runtime status
        ↓
Initialize editor
        ↓
Connect terminal if open
        ↓
Connect runtime events
        ↓
Initialize AI context

The editor should remain responsive during secondary data loading.

117. IDE Loading State

Avoid showing a blank screen.

Use a structured loading state:

Opening project...

Workspace
✓

Runtime
Loading...

Git
Loading...

Editor
Loading...
118. Error Recovery

The frontend should allow targeted recovery.

Examples:

Runtime failed
→ Restart

Git disconnected
→ Reconnect

Terminal disconnected
→ Reconnect

File save failed
→ Retry

AI provider unavailable
→ Retry / Settings
119. Frontend Security

The frontend must never contain:

Database credentials
Redis credentials
GitHub private keys
AI provider secret keys
Internal service credentials
120. Client-Side Validation

Client validation improves UX.

Server validation remains authoritative.

Example:

Client:
Invalid project name

does not eliminate:

Server:
Project name validation
121. Route Protection

Protected routes:

/dashboard
/projects
/projects/*
/settings

must require authentication.

122. Project Route Protection

Routes such as:

/projects/{projectId}

must verify project access through the server.

The frontend must not assume that a valid route parameter grants access.

123. Error Boundaries

Use React/Next.js error boundaries for:

Application-level failures
Editor failures
Panel failures
Unexpected component errors

A single panel failure should not necessarily crash the entire IDE.

124. IDE Fault Isolation

Where practical:

Editor failure
→ terminal remains functional

AI panel failure
→ editor remains functional

Preview failure
→ editor remains functional

Git panel failure
→ terminal remains functional
125. Performance

RUNIX is a complex browser application.

Performance priorities:

Fast initial application shell.
Lazy-load heavy IDE features.
Lazy-load Monaco where appropriate.
Avoid rendering entire file trees unnecessarily.
Virtualize large lists.
Debounce searches.
Avoid excessive global state updates.
Avoid re-rendering the editor on unrelated state changes.
126. Monaco Performance

Do not recreate the Monaco editor unnecessarily.

Preserve:

Editor instance
Model
Cursor
Selection
Undo history

where possible.

127. Large File Handling

Large files should be handled carefully.

If a file exceeds the supported editor threshold:

Large file

The UI may display:

This file is too large for full editor features.
Open as text
128. File Tree Performance

For large repositories:

Lazy-load directories.
Avoid rendering thousands of nodes at once.
Cache expanded directories.
Search server-side when appropriate.
129. Accessibility of Monaco

Where Monaco accessibility features are available, enable appropriate support.

Surrounding controls must remain keyboard accessible even if editor accessibility differs from normal HTML.

130. Frontend Testing

Frontend tests should use:

Vitest
Playwright

Test levels:

Unit
Component
Integration
End-to-end
131. Unit Tests

Test:

Utilities
Hooks
State logic
API client behavior
Validation
Formatting
132. Component Tests

Test:

Buttons
Forms
Dialogs
Project cards
Runtime indicators
Git status
AI states
133. End-to-End Tests

Critical workflows:

Register
Login
Create project
Open project
Create file
Edit file
Save file
Start runtime
Open terminal
Run command
Open preview
Run tests
Git status
AI task
Logout
134. Visual Regression

The Stitch project should serve as the visual reference during implementation.

Where possible, Playwright visual snapshots should cover:

Landing
Login
Dashboard
Create project
IDE
Terminal
AI panel
Git panel
Runtime panel
Settings

Visual changes should be reviewed intentionally.

135. Stitch Fidelity Review

Before considering a frontend area complete, compare the implementation against the Stitch design.

Review:

Layout
Spacing
Typography
Colors
Borders
Radius
Icons
Panel proportions
Component states
Responsive behavior

Do not accept:

"functionally similar"

as sufficient when the visual implementation materially diverges from Stitch.

136. Component Design System

Base components should include:

Button
IconButton
Input
Textarea
Select
Dropdown
Checkbox
Radio
Tabs
Badge
Tooltip
Modal
Drawer
Toast
Spinner
Skeleton
Avatar
CommandPalette

RUNIX-specific components:

ProjectCard
ProjectSwitcher
FileTree
EditorTabs
EditorPanel
TerminalPanel
ProblemPanel
TestPanel
PreviewPanel
RuntimeStatus
RuntimeMonitor
GitChanges
GitDiff
AIAgentPanel
AgentPlan
AgentToolActivity
AgentApproval
137. Component Rules

Components should:

Have one clear responsibility.
Avoid hidden API calls where possible.
Receive state through props/hooks.
Reuse design tokens.
Support loading/error states.
Support accessibility.
Avoid duplicated styling.
138. Design Tokens

Define centralized tokens.

Example conceptual structure:

tokens/
├── colors
├── typography
├── spacing
├── radius
├── shadows
├── motion
└── breakpoints

Values should be derived from Stitch.

139. Semantic Colors

Use semantic names rather than hard-coded colors throughout components.

Example:

bg-surface
text-primary
border-default
accent-primary
status-success
status-warning
status-error

Avoid:

bg-[#123456]

repeated across many components.

140. Spacing System

Use a consistent spacing scale.

Example:

4
8
12
16
20
24
32
40
48
64

The actual RUNIX values should follow Stitch.

141. Motion System

Motion should be:

Fast
Subtle
Functional

Use animation for:

Panel opening
Modal opening
Status transition
Loading
Toast

Avoid decorative motion.

142. No Generic Dashboard Rule

The RUNIX frontend must NOT become:

Generic SaaS dashboard

Avoid:

Huge statistic cards
Random charts
Excessive gradients
Marketing-style cards everywhere
Unnecessary rounded containers
Generic admin templates

RUNIX is developer infrastructure.

143. No Generic AI Chat Rule

The AI interface must NOT look like:

Generic chat application

It should emphasize:

Repository context
Plan
Tools
Changes
Diff
Tests
Approval
144. Navigation

Navigation must remain lightweight.

Primary navigation should provide access to:

Dashboard
Projects
GitHub
Settings

Project-level navigation should expose:

Code
Source Control
Runtime
Settings

The exact navigation layout follows Stitch.

145. Project Switcher

The project switcher should allow:

Search projects
Recent projects
Open project
Create project

It should not require navigating back to the dashboard.

146. User Menu

User menu may contain:

Profile
Settings
Keyboard shortcuts
Theme
Logout
147. Breadcrumb + Navigation

The frontend should maintain clear location awareness.

Example:

RUNIX / Projects / my-app / Code

or the exact hierarchy established by Stitch.

148. Browser URL State

Important application state should be represented in URLs when useful.

Examples:

/projects/:id
/projects/:id?file=src/App.tsx

Avoid putting sensitive data into URLs.

149. Deep Linking

Users should be able to directly open:

Project
Specific file
Source control
Settings

where supported.

150. Unsaved Changes Protection

If a user attempts to leave a project with unsaved changes:

Unsaved changes

You have unsaved changes in:
src/App.tsx

[Stay] [Leave]
151. Project Deletion

Project deletion is destructive.

UI must require explicit confirmation.

Display:

Project name
Consequences
Workspace deletion
Git/runtime implications

Require an explicit confirmation action.

152. Runtime Stop Confirmation

Normal runtime stop may not require a modal.

However, if stopping will terminate active processes or affect unsaved runtime state, communicate the consequence clearly.

153. Git Push Confirmation

The push workflow should clearly display:

Branch
Commits
Remote

User explicitly triggers push.

154. AI Approval Integration

AI approvals should appear:

Inside AI panel

and may additionally trigger:

Notification

Do not force the user to leave the IDE.

155. Notifications Center

Future versions may provide a notification center for:

AI approvals
Runtime events
Git operations
Deployments
System events
156. Theme Architecture

The frontend should support theme tokens.

Initial theme:

RUNIX Dark

Future:

RUNIX Light
System

The initial implementation should prioritize the Stitch theme.

157. Editor Theme

The Monaco theme should visually match the RUNIX Stitch environment.

The editor should not look disconnected from the surrounding application.

158. Terminal Theme

xterm.js colors should harmonize with the RUNIX design.

Terminal readability has priority over decorative matching.

159. Preview Isolation from Main UI

The preview is user application content and must visually remain distinct from RUNIX controls.

The preview frame should clearly communicate:

RUNIX Preview

without unnecessarily interfering with the user's application.

160. Runtime Status Synchronization

When runtime status changes:

Backend event
 ↓
WebSocket
 ↓
Runtime store
 ↓
Top bar
 ↓
Runtime panel
 ↓
Terminal
 ↓
Preview

All UI surfaces should eventually converge on the same runtime state.

161. Git State Synchronization

Git changes should update:

Source Control panel
File explorer indicators
Editor tabs where relevant

after:

save
stage
unstage
commit
pull
checkout
162. AI State Synchronization

AI task events should update:

AI panel
Notification system
Approval state
Diff state
Test state

without requiring a page refresh.

163. Offline / Network Loss

If network connectivity is lost:

RUNIX connection lost
Reconnecting...

The editor should avoid silently discarding local changes.

164. Network Recovery

After reconnection:

Reconnect WebSockets
Refresh runtime state
Refresh Git state
Check file hashes
Resume safe UI synchronization

Do not automatically overwrite local editor content.

165. Frontend Environment Variables

Only public values may be exposed to the browser.

Example:

NEXT_PUBLIC_API_URL=
NEXT_PUBLIC_APP_URL=

Never:

NEXT_PUBLIC_DATABASE_URL
NEXT_PUBLIC_REDIS_URL
NEXT_PUBLIC_GITHUB_PRIVATE_KEY
NEXT_PUBLIC_AI_API_KEY
166. Frontend Build

Production build:

npm run build

Development:

npm run dev

Validation:

npm run lint
npm run typecheck
npm test

Exact scripts depend on the repository implementation.

167. Frontend CI

CI should validate:

Install
Lint
Typecheck
Unit tests
Build
E2E tests
Visual regression where configured
168. Browser Compatibility

Primary support:

Chrome
Edge
Firefox
Safari

Desktop Chrome/Chromium should receive first-class IDE testing because RUNIX is a browser development environment.

169. Frontend Logging

Client logs must not contain:

Authentication tokens
Cookies
Secrets
Provider API keys
GitHub credentials
Private source code unnecessarily

Production logging should be minimal.

170. Frontend Analytics

If analytics are introduced, avoid collecting:

Source code
Terminal content
AI prompts containing private project data
Secrets
Git credentials

Analytics should focus on product interactions.

171. Privacy-Sensitive UI

The frontend should visually communicate when content is:

Private
Shared
Public

where project visibility exists.

172. Project Visibility

Supported values:

Private

Future:

Public
Organization

The UI must accurately reflect server-side visibility.

173. Frontend Error Codes

The frontend should map backend error codes to useful UI messages.

Example:

FILE_CHANGED
→ "This file changed elsewhere."

RUNTIME_UNAVAILABLE
→ "The runtime is unavailable."

PROJECT_ACCESS_DENIED
→ "You do not have access to this project."

QUOTA_EXCEEDED
→ "The project has reached its storage limit."
174. API Error Boundary

Do not display raw backend exception messages.

Map known error codes.

Unknown errors should use:

Something went wrong.

Request ID: ...
175. Frontend Definition of Done

A frontend feature is complete when:

 Stitch design has been inspected.
 Layout matches Stitch.
 Typography matches Stitch.
 Colors match Stitch.
 Spacing matches Stitch.
 Component states are implemented.
 Loading state exists.
 Error state exists.
 Empty state exists where applicable.
 Keyboard behavior works.
 Accessibility is addressed.
 Responsive behavior is implemented.
 API integration works.
 No fake functionality exists.
 Unit/component tests exist where appropriate.
 E2E coverage exists for critical flows.
 No secrets are exposed.
 TypeScript passes.
 Lint passes.
 Production build passes.
176. Stitch Fidelity Definition of Done

Before marking a screen complete, compare it directly against the Stitch project.

The implementation must be checked for:

┌───────────────────────────────┐
│ Visual                        │
├───────────────────────────────┤
│ Layout                        │
│ Spacing                       │
│ Typography                   │
│ Color                         │
│ Borders                      │
│ Radius                       │
│ Icons                        │
│ Component density            │
│ Panel proportions            │
│ Navigation                   │
│ Interactive states           │
│ Responsive behavior          │
└───────────────────────────────┘

Any significant deviation should be corrected rather than rationalized as an alternative design.

177. Implementation Sequence

Frontend implementation should proceed in this order:

Phase 1 — Foundation
Next.js
TypeScript
Tailwind
Design tokens
Global styles
Font configuration
Routing
API client
Authentication state
Phase 2 — Public Pages
Landing
Login
Register
Forgot password
Reset password
Phase 3 — Dashboard
Dashboard
Navigation
Project cards
Project switcher
Create project
Empty states
Phase 4 — IDE Shell
Top bar
Explorer
Editor
Bottom panel
AI panel
Responsive layout
Phase 5 — Workspace
File tree
File operations
Monaco
Saving
Conflict handling
Search
Phase 6 — Runtime
Runtime status
Terminal
WebSocket
Resource monitor
Port detection
Preview
Phase 7 — Git
Source control
Diff
Stage
Commit
Pull
Push
Branches
GitHub import
Phase 8 — AI
Agent panel
Tasks
Plans
Tool activity
Diff
Approval
Tests
Phase 9 — Polish
Keyboard shortcuts
Accessibility
Responsive behavior
Performance
Error states
Loading states
Visual regression
178. Frontend Implementation Rules for Antigravity

When implementing RUNIX frontend code:

Inspect the existing Stitch project first.
Reproduce the Stitch hierarchy.
Do not replace Stitch with a generic dashboard.
Do not invent new colors without justification.
Do not invent new components when an existing component can be reused.
Keep the IDE visually dense but readable.
Preserve developer-tool conventions.
Keep Monaco as the central workspace.
Keep Terminal, Preview, Tests, and Logs in the bottom workspace area where defined by Stitch.
Keep AI integrated into the IDE.
Use real API states.
Do not create fake runtime behavior.
Do not create fake terminal output.
Do not create fake Git status.
Do not create fake AI responses.
Use loading/error/empty states instead.
Preserve responsive behavior from Stitch.
Test keyboard interactions.
Test critical workflows with Playwright.
Compare finished UI against Stitch before declaring completion.
179. Do Not Redesign During Implementation

The developer must not independently decide that RUNIX would look better with:

Different sidebar
Different dashboard
Different color system
Different card system
Different AI layout
Different IDE hierarchy
Different typography
Different navigation

unless the user explicitly requests a design change.

Implementation and design are separate activities.

The existing Stitch design is the approved design baseline.

180. Stitch-to-Code Mapping

The implementation process should be:

Stitch screen
      ↓
Identify regions
      ↓
Identify reusable components
      ↓
Map to React components
      ↓
Map visual properties to tokens
      ↓
Implement interaction
      ↓
Connect real API
      ↓
Test
      ↓
Compare with Stitch
      ↓
Refine
181. Example Mapping

Stitch:

IDE
├── Header
├── Explorer
├── Editor
├── AI
└── Bottom Panel

React:

<IDELayout>
  <IDEHeader />
  <IDESidebar />
  <EditorWorkspace />
  <AIAgentPanel />
  <BottomPanel />
</IDELayout>

This is an implementation mapping, not permission to change the Stitch layout.

182. Component Ownership

Recommended ownership:

IDELayout
  ├── IDEHeader
  ├── ProjectExplorer
  ├── EditorWorkspace
  │   ├── EditorTabs
  │   ├── Breadcrumbs
  │   └── MonacoEditor
  │
  ├── AIAgentPanel
  │   ├── AgentTask
  │   ├── AgentPlan
  │   ├── AgentTools
  │   ├── AgentDiff
  │   └── AgentApproval
  │
  └── BottomPanel
      ├── TerminalPanel
      ├── ProblemsPanel
      ├── OutputPanel
      ├── TestsPanel
      ├── LogsPanel
      └── PreviewPanel
183. Final Frontend Architecture

The intended architecture is:

                         RUNIX FRONTEND
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
         Public Pages      Dashboard          IDE
                                                  │
                 ┌────────────────────────────────┤
                 │                │                │
                 ▼                ▼                ▼
             Explorer          Editor            AI
                 │                │                │
                 └────────────────┼────────────────┘
                                  │
                                  ▼
                            Bottom Panel
                                  │
            ┌─────────────┬───────┼─────────┬──────────┐
            ▼             ▼       ▼         ▼          ▼
         Terminal      Problems  Output    Tests     Preview
                                  │
                                  ▼
                             RUNIX API
                                  │
             ┌────────────────────┼────────────────────┐
             ▼                    ▼                    ▼
          Workspace            Runtime              Git/API
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  ▼
                             Cloud Runtime
184. Final Principle

RUNIX frontend implementation is not an independent redesign project.

The existing Stitch project defines the intended product experience.

The implementation responsibility is to transform that design into:

Stitch
  ↓
Production React UI
  ↓
Real RUNIX APIs
  ↓
Real runtime
  ↓
Real terminal
  ↓
Real Git
  ↓
Real AI agent

while preserving the visual hierarchy and interaction model.

The fundamental frontend rule is:

Build the RUNIX product shown by Stitch, not a generic interpretation of what a cloud IDE should look like.