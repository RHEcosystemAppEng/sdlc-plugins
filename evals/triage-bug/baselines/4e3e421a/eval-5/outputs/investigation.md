# Steps 2–3 – Reproduce/Trace and Codebase Investigation: ACME-511

## Step 2 – Reproduce/Trace

### Runnable reproduction

None of the Steps to Reproduce are runnable commands. They are manual browser actions
(open the app, Settings > Appearance, toggle Dark Mode, close and reopen the browser).
No CLI, curl or test command is given, so direct reproduction was **not attempted**.
Outcome: **environment-dependent / not reproduced** (staging deployment, browser session lifecycle).

### Code-path tracing

- Entry point from the steps: the UI action **Settings > Appearance > "Dark Mode" toggle**.
- Expected path: toggle handler -> save the preference (client storage such as
  `localStorage` or a cookie, or a backend user-preferences endpoint) -> on app start, read
  the saved preference -> apply the theme.
- Where behavior diverges (from the report): after a full browser restart the preference is
  missing or ignored, and the app falls back to the default (light). This points to one of these:
  1. The preference is kept only in memory or in `sessionStorage`. Both are cleared when the browser closes.
  2. The preference is written, but the startup code never reads it back (or reads it after the default theme has already been applied).
  3. If it is stored on the server: there is no persistence endpoint or column, or the save call is never made.

## Step 3 – Codebase Investigation

### Target repository

- Component field: `sdlc-workflow`.
- Repository Registry has one entry: **acme-backend** (Rust backend service,
  Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`).
- Code Intelligence: **no Serena MCP servers are configured**, so the Read/Grep/Glob fallback
  applies. (In this eval, the repository context comes from `repo-context-mock.md`.)

### Findings from repository context

The repository context (repo-context-mock.md) was reviewed in full. It describes:

| File | Content | Related to ACME-511? |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | CONVENTIONS.md heading extraction (`line[3:]` does not strip trailing whitespace) | **No.** This is about convention-section matching. |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`if convention_name in discovered_conventions`) | **No** |
| `evals/plan-feature/files/conventions-mock.md` | Eval fixture with no trailing-whitespace headings | **No** |
| CONVENTIONS.md | Not present at the repo root | n/a |

The context file says it simulates the code paths for **ACME-500**, a different bug, not ACME-511.

**No code related to the dark mode / theme / appearance settings / preference persistence
was found.** Specifically, the available context contains no evidence of:
- a theme or dark-mode toggle component or handler
- client-side storage use (`localStorage`, `sessionStorage`, cookies) for preferences
- a backend user-preferences endpoint, model, table or column
- startup or hydration logic that applies a saved theme

There is also a mismatch to note. The registered repository is a **Rust backend service**,
while the bug is a **browser UI** behavior. The Component (`sdlc-workflow`) also does not map
to a frontend. The frontend repository that owns the Settings > Appearance UI may be missing
from the Repository Registry.

### Persistence-impact analysis

- No buggy function was identified, so there is no output to trace to a persistence boundary.
- If the fix adds server-side storage of the preference, that is a **new** persistence path,
  not a correction of stale data. No existing records hold wrong values, so **no data
  migration is needed** for this bug.

### Existing test patterns

- None found for UI theme or preference persistence in the available context. The only test
  artifact in the context is `evals/plan-feature/files/conventions-mock.md`, which is unrelated.

### Reusable utilities

- None identified in the available context.

### Decomposition Guard (Step 6) check

- Only one symptom (theme preference not persisted) is reported, and there is no evidence of
  several independent defects. **No decomposition trigger.** One Task is appropriate.

### Investigation summary

| Goal | Result |
|---|---|
| Affected files/symbols identified | **No.** Not found in the available repository context. |
| Code paths understood | Only from the bug report (UI toggle -> persist -> rehydrate). Not confirmed in code. |
| Patterns for Implementation Notes | None discovered |
| Existing test files for the reproducer | None discovered |
| Persistence impact / migration needed | No |
| CONVENTIONS.md | Not present |
