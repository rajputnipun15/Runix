RUNIX — Design System

**Document:** 14-DESIGN-SYSTEM.md  
**Product:** RUNIX  
**Status:** Implementation Specification  
**Version:** 1.0  
**Last Updated:** 2026-09-29

---

# 1. Purpose

This document defines the reusable visual and interaction system for RUNIX.

The RUNIX design system exists to ensure that every part of the product feels like the same application.

The design system covers:

- Color
- Typography
- Spacing
- Layout
- Borders
- Radius
- Shadows
- Icons
- Buttons
- Inputs
- Navigation
- Panels
- Cards
- Tables
- Tabs
- Modals
- Drawers
- Tooltips
- Status indicators
- Notifications
- Editor UI
- Terminal UI
- Git UI
- Runtime UI
- AI UI
- Responsive behavior
- Accessibility
- Motion

---

# 2. Primary Design Source

The existing **RUNIX Stitch project** is the primary visual source of truth.

The design system must be derived from the Stitch implementation and visual language.

Priority:

```text
Stitch
  ↓
Design tokens
  ↓
Reusable components
  ↓
Product screens

If an existing Stitch component conflicts with a generic design-system convention, the Stitch design takes precedence unless the user explicitly requests a redesign.

3. Design Philosophy

RUNIX is developer infrastructure.

The visual language should communicate:

Precision
Control
Speed
Technical depth
Reliability
Clarity
Professionalism

The interface should feel appropriate for developers who spend significant amounts of time inside the product.

4. Visual Direction

RUNIX should maintain a:

Deep dark foundation
Layered surface hierarchy
Restrained accent color
High text contrast
Compact developer-tool density
Precise spacing
Subtle borders
Controlled elevation
Strong monospace treatment for technical content

Avoid:

Excessive gradients
Neon-heavy styling
Generic SaaS cards
Cartoon illustrations
Excessive glassmorphism
Oversized rounded cards
Decorative UI that reduces information density
Generic chatbot styling
5. Brand
Name
RUNIX
Tagline
Build. Run. Ship. Anywhere.

The RUNIX wordmark should follow the existing Stitch treatment.

Do not introduce an alternative logo treatment during implementation.

6. Design Token Architecture

Design tokens should be centralized.

Recommended structure:

frontend/
└── styles/
    ├── globals.css
    ├── tokens.css
    └── themes.css

Or:

frontend/
└── design-system/
    ├── tokens.ts
    ├── colors.ts
    ├── typography.ts
    ├── spacing.ts
    ├── motion.ts
    └── components/

The implementation may use CSS variables, Tailwind tokens, TypeScript constants, or a combination.

7. Token Naming

Use semantic token names.

Preferred:

--color-bg
--color-surface
--color-surface-elevated
--color-border
--color-text-primary
--color-text-secondary
--color-text-muted
--color-accent
--color-success
--color-warning
--color-error

Avoid coupling components to arbitrary raw colors.

Bad:

bg-[#15151c]

repeated throughout the application.

Preferred:

bg-surface

or:

background: var(--color-surface);
8. Color System

The exact RGB/HEX values must be extracted from the approved Stitch design.

The implementation should expose semantic color roles.

Core Roles
background
surface
surface-secondary
surface-elevated
surface-hover
surface-active
border
border-strong
text-primary
text-secondary
text-muted
text-disabled
accent
accent-hover
accent-active
9. Background Hierarchy

The application should use multiple dark surfaces rather than one flat background.

Conceptually:

Level 0
Application background

Level 1
Primary surface

Level 2
Elevated surface

Level 3
Modal / command palette / overlay

Example hierarchy:

┌──────────────────────────────────────────┐
│ Application background                   │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │ Surface                            │  │
│  │                                    │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │ Elevated surface             │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘

Exact visual levels must follow Stitch.

10. Accent Color

RUNIX uses a restrained primary accent based on the Stitch design.

The accent should be used for:

Primary actions
Active navigation
Selected tabs
Focus indicators
Important links
Selected editor elements where appropriate

Do not apply the accent to every component.

11. Semantic Status Colors

Status colors:

Success
Warning
Error
Info
Neutral

Typical meanings:

Success → Running / Passed / Connected
Warning → Attention / Pending / Degraded
Error → Failed / Stopped unexpectedly / Invalid
Info → Informational state
Neutral → Inactive / Unknown

The exact colors must follow Stitch.

12. Status Indicator

Runtime status should use a compact indicator.

Example:

● Running

or:

● Connected

Avoid oversized badges for simple status information.

13. Status Rules

Status must never depend solely on color.

Use:

Color
+
Icon or symbol
+
Text

Example:

✓ Tests passed
⚠ Runtime degraded
× Runtime failed

This improves accessibility.

14. Typography

Typography should follow the Stitch project.

The design system should define:

Display
Heading 1
Heading 2
Heading 3
Body
Body Small
Label
Caption
Code
Terminal
15. Font Roles

Recommended role separation:

UI font
→ navigation, buttons, labels, general content

Monospace font
→ source code, terminal, paths, commands, Git metadata

The exact font family must follow Stitch.

16. Typography Hierarchy

The visual hierarchy should generally be:

Page title
    ↓
Section title
    ↓
Component heading
    ↓
Body
    ↓
Secondary text
    ↓
Metadata

Do not use excessive font sizes inside the IDE.

17. Font Weight

Use a restrained weight scale.

Typical:

400
500
600
700

Use heavier weights for hierarchy rather than decorative emphasis.

18. Line Height

UI text should use compact but readable line heights.

Code and terminal line heights should prioritize readability and editor conventions.

19. Monospace Rules

Monospace is appropriate for:

File paths
Git branches
Commit hashes
Commands
Terminal
Source code
Runtime metadata
Port numbers
Technical identifiers

Example:

src/components/Button.tsx
20. Spacing System

Use a consistent spacing scale.

Recommended conceptual scale:

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
80
96

The final values must be aligned with Stitch.

21. Spacing Principles

Use:

Small spacing
→ related elements

Medium spacing
→ related groups

Large spacing
→ separate sections

Example:

Label
  8px
Input
  16px
Next field

Avoid random spacing values.

22. Density

RUNIX should maintain a professional developer-tool density.

The UI should display substantial information without becoming cramped.

Target:

Compact
but
readable
23. Layout Grid

The application should use a consistent layout grid.

Primary IDE regions:

Top bar
Sidebar
Main editor
AI panel
Bottom panel

These regions should align consistently.

24. IDE Layout

Conceptual structure:

┌──────────────────────────────────────────────────────────┐
│ Header                                                   │
├────────────┬───────────────────────────────┬─────────────┤
│            │                               │             │
│ Explorer   │ Editor                        │ AI          │
│            │                               │             │
│            │                               │             │
├────────────┴───────────────────────────────┴─────────────┤
│ Terminal / Problems / Tests / Output / Preview           │
└──────────────────────────────────────────────────────────┘

Actual dimensions are determined by Stitch.

25. Panel Borders

Use subtle borders to communicate structural separation.

Good:

Editor | AI

with a subtle divider.

Avoid:

Every card
Every button
Every text group

having a visible border.

26. Border Tokens

Define:

border-subtle
border-default
border-strong
border-focus
border-error
27. Radius System

Radius should follow Stitch.

Recommended semantic roles:

radius-sm
radius-md
radius-lg
radius-xl
radius-full

Use larger radius primarily for:

Modals
Floating panels
Major cards
Selected surfaces where Stitch specifies it

Developer workspace panels should generally remain structurally precise.

28. Shadows

Define:

shadow-none
shadow-sm
shadow-md
shadow-lg

Use shadows sparingly.

Preferred hierarchy:

Flat surfaces
↓
Subtle elevation
↓
Modal elevation
29. Cards

RUNIX cards should primarily group meaningful information.

Examples:

Project card
Runtime summary
GitHub repository
Settings section

Avoid turning every UI element into a card.

30. Project Card

A project card should contain:

Project name
Description
Template
Status
Last modified
Optional Git branch

Actions may include:

Open
More
31. Cards Should Not Become Dashboards

Avoid:

10 giant metric cards
Large empty whitespace
Decorative charts
Unrelated statistics

RUNIX should prioritize actual developer workflow.

32. Buttons

Button hierarchy:

Primary
Secondary
Ghost
Danger
Icon
33. Primary Button

Used for:

Create Project
Start Runtime
Save
Approve

Primary action should be visually distinct.

34. Secondary Button

Used for:

Cancel
Open Preview
View Diff
Configure
35. Ghost Button

Used for:

Toolbar actions
Low-priority controls
Panel actions
36. Danger Button

Used for:

Delete project
Delete file
Terminate
Destructive operation

Danger styling should not be used merely to attract attention.

37. Icon Button

Use for compact IDE actions:

Refresh
Close
Settings
Search
More
Split
Maximize

Icon-only buttons require accessible labels and tooltips where appropriate.

38. Button States

Every button must define:

Default
Hover
Active
Focus
Disabled
Loading
39. Loading Button

Example:

Creating...

rather than:

Create

while the action is executing.

Prevent duplicate submissions.

40. Inputs

Input design must match Stitch.

States:

Default
Hover
Focus
Filled
Error
Disabled
Read-only
41. Input Labels

Every form input should have an associated label.

Avoid relying solely on placeholders.

42. Input Errors

Example:

Project name
[my project]

Project names cannot contain spaces.

The error should appear near the relevant input.

43. Search Input

Search inputs should visually communicate:

Search
Keyboard shortcut where useful
Clear action
Loading state
44. Tabs

Tabs are heavily used inside RUNIX.

Examples:

Editor tabs
Terminal tabs
Bottom panel tabs
Settings sections
45. Tab States
Active
Inactive
Hover
Focus
Disabled
Modified

The active state must be visually obvious without relying only on color.

46. Editor Tabs

Example:

App.tsx    index.css    package.json

Modified:

● App.tsx

The modified state must be subtle but visible.

47. Bottom Panel Tabs

Example:

Terminal
Problems
Output
Tests
Logs
Preview

The active panel should be immediately identifiable.

48. Navigation

Navigation should be compact and predictable.

Primary areas:

Dashboard
Projects
GitHub
Settings

Project-level navigation:

Code
Source Control
Runtime
Settings
49. Active Navigation

Active navigation should use:

Accent
Background treatment
Text weight
Icon state

as appropriate to Stitch.

50. Sidebars

The sidebar should support:

Expanded
Collapsed
Overlay

depending on viewport.

51. Explorer Sidebar

The explorer is a high-density interface.

Priorities:

File visibility
Hierarchy
Fast interaction
Keyboard navigation
Low visual noise
52. File Tree

Tree indentation should be consistent.

Example:

src/
  components/
    Button.tsx
    Card.tsx
  App.tsx
  main.tsx

Folder/file distinction should be visually clear.

53. File Tree Selection

Selected file should have a strong but restrained highlight.

Do not use a large card-like selection container.

54. Context Menus

Context menus should be:

Compact
Keyboard accessible
Consistent

Actions:

Open
Rename
Delete
New file
New folder
Copy path
55. Modal System

Modals should use:

Overlay
Dialog surface
Header
Content
Actions
56. Modal Hierarchy

Example:

Delete Project

This action permanently deletes:
• Workspace
• Runtime configuration
• Project metadata

This cannot be undone.

[Cancel] [Delete Project]

The most consequential action should be visually explicit.

57. Drawer System

Drawers are useful for:

AI panel on smaller screens
Runtime details
Mobile project navigation
58. Command Palette

The command palette should feel like a core RUNIX control surface.

Structure:

┌──────────────────────────────────────┐
│ Search commands...                   │
├──────────────────────────────────────┤
│ Project                              │
│   Open Project                       │
│   Create Project                     │
│                                      │
│ Runtime                              │
│   Start Runtime                      │
│   Restart Runtime                    │
│                                      │
│ Development                          │
│   Open Terminal                      │
│   Run Tests                          │
└──────────────────────────────────────┘
59. Command Palette Design Rules
Fast.
Keyboard-first.
Searchable.
Categorized.
Compact.
No unnecessary animation.
Accessible.
60. Tooltips

Tooltips should:

Explain icon-only controls.
Appear after a short delay.
Not block interaction.
Be accessible.

Avoid tooltip overload.

61. Badges

Badges are appropriate for:

Runtime status
Git branch
Project visibility
AI task state
Test result

Do not use badges for every metadata field.

62. Runtime Status Component

Possible variants:

Running
Starting
Stopped
Stopping
Failed
Terminating
Terminated

Example:

● Running
63. Test Status Component

Possible variants:

Passed
Failed
Skipped
Running
Not Run
64. Git Status Component

Possible indicators:

Modified
Added
Deleted
Renamed
Untracked

Use familiar Git conventions.

65. Progress Indicators

Use progress indicators for operations such as:

Project creation
Repository import
Runtime startup
Deployment
Large file operations

If exact progress cannot be measured, use an indeterminate indicator rather than a fake percentage.

66. Toasts

Toast categories:

Success
Info
Warning
Error

Example:

✓ Project created

or:

⚠ Runtime failed to start

The actual visual treatment follows Stitch.

67. Notification Rules

Notifications should:

Be short.
State what happened.
Provide action where useful.
Avoid interrupting the editor.
Automatically disappear for low-priority events.
68. Skeletons

Skeletons should represent the actual shape of content.

Do not use generic full-page spinners for every operation.

69. Empty States

Empty states should contain:

Title
Short explanation
Primary action

Example:

No projects yet.

Create a project to start building.

[Create Project]
70. Error States

Error states should include:

What failed
Why it matters
What user can do

Example:

Runtime unavailable

RUNIX could not start the development environment.

[Retry] [View Logs]
71. AI Agent Design

The AI Agent has a distinct design system within RUNIX.

It must visually emphasize:

Task
Context
Plan
Tools
Changes
Tests
Approval
72. AI Agent Should Not Look Like Chat

Avoid:

Chat bubbles
Avatar-heavy conversation UI
Generic assistant cards
Large empty chat space

The agent is a development workflow.

73. AI Task Header

Example:

RUNIX AI
Coding Agent

Fix the login redirect bug
74. AI Context

Show concise context metadata:

3 files
Auth
2 tests
Current branch: main
75. AI Plan Component

Each plan item should have:

Status icon
Description

Example:

✓ Inspect authentication
✓ Read session middleware
○ Prepare patch
○ Run tests
76. AI Tool Activity

Tool activity should be chronological.

Example:

10:41  search_code
10:41  read_file
10:42  inspect_git
10:42  update_file
10:42  run_tests

Timestamps may be omitted if unnecessary.

77. AI Diff Component

The diff component should provide:

Files changed
Lines added
Lines removed
Review action
Apply action
Reject action
78. AI Approval Component

Approval should clearly identify risk.

Example:

Changes require approval

3 files
+42
-11

Risk: Medium

[Review Diff]
[Approve]
[Reject]
79. AI Test Result

After testing:

Tests

24 passed
0 failed

Duration 4.21s

✓ Validation complete
80. Editor Design

The editor is the visual center of the IDE.

The surrounding interface should not compete with the code.

Priorities:

Code readability
File navigation
Diagnostics
Tabs
Cursor/selection visibility
81. Editor Chrome

Keep editor chrome compact.

Avoid unnecessary:

Large headers
Large buttons
Decorative elements
82. Editor Breadcrumb

Breadcrumbs should communicate file location without consuming excessive vertical space.

83. Editor Diagnostics

Use subtle indicators:

Red → error
Yellow → warning
Blue/neutral → information

Exact colors must follow Stitch.

84. Terminal Design

Terminal should visually behave like a terminal.

Use:

Monospace
High contrast
Dark surface
ANSI colors
Cursor
Scrollback

Avoid placing terminal output inside generic cards.

85. Terminal Header

May contain:

Terminal
Session selector
New session
Restart
Clear
Close
86. Preview Design

Preview should feel like a browser embedded inside RUNIX.

Potential structure:

Preview
────────────────────────
Address / port
Refresh
Open externally
────────────────────────
User application
87. Runtime Monitor Design

Runtime monitor should emphasize:

State
CPU
Memory
Storage
Ports
Health

Avoid turning the monitor into a generic analytics dashboard.

88. Resource Meters

Meters should communicate capacity clearly.

Example:

Memory
418 MB / 1 GB
████████░░

If the Stitch design uses another representation, use the Stitch version.

89. Git Diff Design

Git diff should prioritize:

Code
File identity
Change context

The surrounding controls should remain secondary.

90. Source Control Design

Source control should display changes in a compact list.

Example:

Changes

M  src/App.tsx
M  src/index.css
A  src/components/Button.tsx
91. Project Settings Design

Settings should use a clear two-level hierarchy where appropriate:

Settings
├── General
├── Runtime
├── GitHub
├── AI
└── Security

The exact Stitch layout takes precedence.

92. Form Design

Forms should:

Group related fields.
Use clear labels.
Explain constraints.
Show inline errors.
Disable invalid submission.
Preserve user input after recoverable errors.
93. Destructive Actions

Destructive controls should be visually distinct but not excessive.

Examples:

Delete project
Delete file
Terminate runtime

Always communicate consequence.

94. Focus States

Every interactive element needs a visible focus state.

Focus should not be removed merely to achieve visual minimalism.

95. Hover States

Hover states should communicate interactivity without dramatic visual changes.

Avoid:

Large scaling
Strong glow
Large color shifts
96. Active States

Active controls should have a clear state.

Examples:

Active tab
Selected file
Selected navigation item
Pressed toolbar action
97. Disabled States

Disabled components should communicate:

Not currently available

but remain sufficiently legible.

98. Motion

Motion should support comprehension.

Good uses:

Panel open
Panel close
Toast enter/exit
Status change
Loading
Modal transition

Bad uses:

Constant floating
Decorative animations
Excessive parallax
Continuous gradients
99. Motion Timing

Use a small set of transition durations.

Conceptually:

Fast
100–150ms

Normal
150–250ms

Slow
250–350ms

Exact values should be tuned to Stitch.

100. Reduced Motion

Respect:

prefers-reduced-motion

When enabled:

Remove non-essential motion.
Reduce transitions.
Avoid animated decorative effects.
101. Responsive Design Tokens

Define breakpoints based on actual RUNIX layout needs.

Conceptually:

mobile
tablet
laptop
desktop
wide desktop

Do not force generic framework breakpoints if they do not match the Stitch layout.

102. Desktop Behavior

Full workspace:

Explorer
Editor
AI
Bottom panel
103. Laptop Behavior

Prioritize:

Editor
Explorer
Bottom panel

AI may collapse into a toggleable panel.

104. Tablet Behavior

Prioritize:

Editor
Terminal
Project navigation

Secondary panels become overlays.

105. Mobile Behavior

Mobile should prioritize project management rather than attempting to reproduce the complete desktop IDE.

Supported:

Projects
Project status
Runtime status
Git status
AI task status
Settings
106. Accessibility

RUNIX should target WCAG 2.2 AA where practical.

Requirements:

Keyboard navigation
Focus visibility
Semantic controls
Accessible labels
Contrast
Screen-reader support
Reduced motion
Error announcements
107. Contrast

Important text must maintain sufficient contrast against its surface.

Do not use extremely low-contrast gray text merely for aesthetic purposes.

108. Icon Accessibility

Icon-only buttons require:

aria-label

Example:

<button aria-label="Restart runtime">
109. Modal Accessibility

Dialogs must:

Trap focus.
Restore focus.
Support Escape where appropriate.
Have an accessible title.
Clearly identify destructive actions.
110. Keyboard Accessibility

The following workflows should be keyboard accessible:

Open file
Search code
Open command palette
Switch tabs
Open terminal
Navigate explorer
Run tests
Approve AI change
111. Screen Reader Support

Important state changes should be announced where appropriate.

Examples:

Runtime started.
File saved.
Tests completed.
AI approval required.
112. Design System Component API

Reusable components should expose semantic props.

Example:

<Button
  variant="primary"
  size="md"
  loading={isCreating}
>
  Create Project
</Button>

Avoid component APIs that require raw visual values.

Bad:

<Button
  color="#6C5CE7"
  radius="14px"
  padding="13px"
/>
113. Component Variants

Components should use controlled variants.

Example:

Button
├── primary
├── secondary
├── ghost
└── danger

Not dozens of arbitrary styles.

114. Design Token Enforcement

ESLint or code review should discourage excessive raw color usage.

Preferred:

className="bg-surface text-primary"

instead of repeated custom colors.

115. Tailwind Integration

Tailwind should consume RUNIX semantic tokens.

Example conceptual configuration:

theme: {
  extend: {
    colors: {
      background: "var(--color-background)",
      surface: "var(--color-surface)",
      border: "var(--color-border)",
      primary: "var(--color-text-primary)",
      secondary: "var(--color-text-secondary)",
      accent: "var(--color-accent)",
    },
  },
}

The actual values should be derived from Stitch.

116. Global CSS

Global CSS should define:

Root variables
Font loading
Base body styles
Selection
Scrollbar treatment
Focus styles
Reduced-motion behavior
117. Scrollbars

Scrollbars should be visually integrated with the dark RUNIX environment while maintaining usability.

Do not make scrollbars invisible.

118. Text Selection

Text selection should remain visible and accessible.

Editor/terminal selection behavior should follow their native interaction models.

119. Z-Index System

Define a consistent stacking hierarchy.

Example:

Base
10

Sticky UI
20

Dropdown
40

Tooltip
50

Modal
70

Command palette
80

Critical overlay
100

Actual values may vary.

Avoid arbitrary z-index values across components.

120. Overlay System

Overlays should correctly manage:

Backdrop
Focus
Scroll locking
Z-index
Escape
Click outside
121. Scroll Lock

When a modal or full-screen mobile drawer opens:

Body scrolling
→ disabled

Underlying content must not scroll accidentally.

122. Design Consistency Rules

If a component already exists:

Reuse it.

Do not create:

ButtonV2
ButtonNew
CustomButton

for every new feature.

123. Feature-Specific Styling

Feature-specific styling should use shared tokens.

Example:

AI panel
→ shared surface
→ shared border
→ shared text
→ shared spacing

It should not introduce an unrelated visual system.

124. Design Review Checklist

Before completing a screen:

[ ] Matches Stitch layout
[ ] Matches Stitch spacing
[ ] Matches Stitch typography
[ ] Matches Stitch colors
[ ] Matches Stitch borders
[ ] Matches Stitch radius
[ ] Matches Stitch icons
[ ] Matches Stitch states
[ ] Responsive
[ ] Accessible
[ ] Keyboard accessible
[ ] Loading state
[ ] Empty state
[ ] Error state
125. Visual Regression Checklist

For each important screen compare:

Desktop
Laptop
Tablet
Mobile where applicable

Check:

Header
Sidebar
Content
Panels
Typography
Spacing
Buttons
Inputs
Status
Dialogs
126. Stitch Change Management

If the Stitch project changes later:

Updated Stitch
      ↓
Review visual changes
      ↓
Update tokens/components
      ↓
Update affected screens
      ↓
Run visual regression

Do not manually diverge from the latest approved design.

127. Design System Ownership

The design system should be implemented centrally.

Feature teams should consume the design system rather than recreating primitives.

128. Component Documentation

Reusable components should document:

Purpose
Props
Variants
States
Accessibility
Usage examples
129. Storybook

Storybook may be introduced if useful for component development.

Potential stories:

Button
Input
Tabs
Modal
Badge
RuntimeStatus
FileTree
AgentApproval
GitDiff
TerminalHeader

It is optional and should not become a prerequisite for product development unless adopted.

130. Design Tokens Example

Conceptual token structure:

:root {
  --color-background: ...;
  --color-surface: ...;
  --color-surface-elevated: ...;

  --color-border: ...;
  --color-border-strong: ...;

  --color-text-primary: ...;
  --color-text-secondary: ...;
  --color-text-muted: ...;

  --color-accent: ...;
  --color-accent-hover: ...;

  --color-success: ...;
  --color-warning: ...;
  --color-error: ...;
  --color-info: ...;

  --space-1: ...;
  --space-2: ...;
  --space-3: ...;
  --space-4: ...;

  --radius-sm: ...;
  --radius-md: ...;
  --radius-lg: ...;

  --shadow-sm: ...;
  --shadow-md: ...;
}

The actual values MUST be populated from the approved Stitch visual system.

131. Component Architecture

Recommended:

components/
├── ui/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Modal.tsx
│   ├── Tabs.tsx
│   ├── Badge.tsx
│   ├── Tooltip.tsx
│   └── ...
│
├── layout/
│   ├── AppShell.tsx
│   ├── Sidebar.tsx
│   ├── TopBar.tsx
│   └── Panel.tsx
│
├── editor/
│   ├── EditorTabs.tsx
│   ├── FileTree.tsx
│   ├── Breadcrumbs.tsx
│   └── MonacoEditor.tsx
│
├── runtime/
│   ├── RuntimeStatus.tsx
│   ├── RuntimeMonitor.tsx
│   └── ResourceMeter.tsx
│
├── terminal/
│   ├── TerminalPanel.tsx
│   └── TerminalTabs.tsx
│
├── git/
│   ├── GitChanges.tsx
│   ├── GitDiff.tsx
│   └── BranchSelector.tsx
│
└── ai/
    ├── AIAgentPanel.tsx
    ├── AgentPlan.tsx
    ├── AgentActivity.tsx
    ├── AgentDiff.tsx
    └── AgentApproval.tsx
132. Do Not Over-Abstract

Do not create abstractions solely to reduce file count.

A component should be extracted when:

It is reused.
It has meaningful internal behavior.
It represents a clear design-system primitive.
It improves maintainability.
133. Design System and Business Logic

Visual components should not directly contain complex business logic.

Prefer:

UI component
   ↓
Hook / feature service
   ↓
API

rather than:

UI component
   ↓
raw API
   ↓
business logic
   ↓
state
134. Design System and API Errors

Reusable UI components should receive normalized states.

Example:

<RuntimeStatus
  status="failed"
/>

rather than requiring every component to interpret backend errors independently.

135. Design System and Loading

Reusable loading components should include:

Spinner
Skeleton
Progress
InlineLoader
ButtonLoader
PanelLoader
136. Design System and Empty States

Reusable empty-state component:

<EmptyState
  title="No projects yet"
  description="Create your first RUNIX project."
  action={<Button>Create Project</Button>}
/>
137. Design System and Errors

Reusable error component:

<ErrorState
  title="Runtime unavailable"
  description="The runtime could not be started."
  action={<Button>Retry</Button>}
/>
138. Design System and Notifications

Use a centralized notification system.

Example:

notify({
  type: "success",
  title: "Project created",
});

Avoid individual features implementing their own toast systems.

139. Design System and Keyboard Shortcuts

Keyboard shortcuts should be registered through a centralized mechanism.

Avoid multiple components independently registering conflicting global shortcuts.

140. Design System and Focus Management

Focus behavior should be deliberate.

Examples:

Open modal
→ focus first meaningful control

Close modal
→ restore previous focus

Open command palette
→ focus search

Open file
→ focus editor
141. Design System and Performance

Reusable components should avoid unnecessary rendering.

Important areas:

File tree
Editor
Terminal
AI tool activity
Git diff
Logs

These can contain large amounts of data.

142. Virtualization

Use virtualization when displaying:

Thousands of files
Large logs
Large test results
Large Git diffs
Long AI tool history
143. Design System and Internationalization

The initial release may use English only.

However, UI text should not be hard-coded into deeply coupled logic if future localization is anticipated.

144. Design System and Error Copy

Error messages should be:

Short
Specific
Actionable
Non-technical where possible

Technical details can be exposed through logs or expandable details.

145. Design System and Developer Language

RUNIX is a developer product.

Use technical terms correctly:

Runtime
Workspace
Branch
Commit
Repository
Terminal
Preview
Build
Test
Deployment
Agent

Do not replace precise technical terms with overly simplified consumer terminology.

146. Design System and Brand Consistency

Every screen should feel like:

RUNIX

rather than a collection of third-party component libraries.

Third-party libraries should be visually normalized through RUNIX tokens.

147. Third-Party Component Normalization

If a third-party component is used:

Third-party component
       ↓
RUNIX styling adapter
       ↓
RUNIX visual system

Do not expose unrelated default library styling directly to users.

148. Monaco Integration

Monaco is a specialized component.

Its internal styling should remain functional.

RUNIX should customize:

Theme
Background
Selection
Cursor
Diagnostics
Tabs around editor

without attempting to redesign Monaco's core editing behavior.

149. xterm Integration

xterm.js is similarly specialized.

Customize:

Background
Foreground
Cursor
Selection
Font
Font size
Line height
ANSI palette

according to Stitch.

150. Preview Integration

Preview should remain technically isolated from RUNIX CSS.

Do not inject RUNIX global styles into user applications.

151. User Application Isolation

The preview iframe/application must not inherit:

RUNIX CSS
RUNIX fonts
RUNIX JavaScript state
RUNIX authentication state

unless explicitly required by the preview architecture.

152. Security and Design System

Visual UI must never be used as a security mechanism.

For example:

Disabled-looking button

does not replace:

Server-side authorization
153. Design System and Permissions

The UI should reflect permissions:

Read-only user
→ edit controls disabled/hidden

Owner
→ management controls visible

But server-side permission enforcement remains authoritative.

154. AI Permission UI

If an AI action requires approval, the interface must make that state explicit.

Example:

Approval required

Do not disguise approval as a normal button click.

155. Destructive UI

Destructive actions should communicate:

Irreversible
Potentially disruptive
Requires confirmation
156. Final Visual Rules

RUNIX frontend should consistently follow:

1. Stitch is the visual source of truth.
2. Developer workflow takes priority over decoration.
3. Information density should be high but readable.
4. Surfaces should remain visually structured.
5. Accent color should be restrained.
6. Borders should be subtle.
7. Typography should be precise.
8. Technical information should use monospace where appropriate.
9. Animation should be functional.
10. Accessibility is part of the design.
11. Responsive behavior should preserve functionality.
12. Reusable components should use shared tokens.
13. Third-party components must be visually normalized.
14. No fake states.
15. No fake functionality.
16. No generic SaaS dashboard replacement.
17. No generic AI chatbot replacement.
157. Stitch Fidelity Rule

The implementation is considered visually correct only when the final rendered UI can be compared against the approved Stitch screen and the following are materially consistent:

Layout
Hierarchy
Spacing
Typography
Color
Surface treatment
Borders
Radius
Icons
Component density
Interaction states
Responsive behavior

The objective is not to approximate Stitch.

The objective is to implement it faithfully.

158. Final Design-System Principle

RUNIX should feel like one coherent developer environment from the landing page to the deepest terminal session.

The design hierarchy is:

RUNIX Brand
      ↓
Stitch Visual Language
      ↓
Design Tokens
      ↓
Reusable Components
      ↓
Product Screens
      ↓
IDE Workspace
      ↓
Developer Workflow

The fundamental rule is:

Stitch defines how RUNIX looks and behaves visually; the RUNIX architecture defines how it works