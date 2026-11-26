# Steps 2 & 3 – Reproduce/Trace and Codebase Investigation: ACME-511

## Step 2 – Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce are manual browser interactions (open app, Settings > Appearance,
toggle Dark Mode, close and reopen the browser). There are no CLI commands, curl calls, or
test commands to run. **Direct reproduction is not possible** in this session (and Bash
would not be used to change anything anyway).

Outcome: **not reproduced — environment-dependent (requires a browser and the staging
deployment).**

### Code-path tracing

Expected trace for this bug:

1. Entry point: the "Dark Mode" toggle in the Settings > Appearance UI.
2. Toggle handler: updates in-memory theme state (component state / store).
3. Persistence step: should write the preference to durable storage (browser
   `localStorage`/cookie on the client, or a user-preferences record on the backend).
4. App bootstrap: on load, should read the stored preference and apply it before the
   first render, falling back to light mode only if no preference exists.

Divergence: the reported behavior (toggle reset to OFF after a full browser restart) means
either step 3 never writes the value durably (e.g., it is held only in memory or in
`sessionStorage`, which is cleared when the browser closes), or step 4 does not read it
back on startup and initializes to the light-mode default.

The provided repository context did not contain code for any of these steps, so the
divergence point could not be pinned to a specific file (see Step 3).

## Step 3 – Codebase Investigation

### Target repository

- Component: `sdlc-workflow`
- Repository Registry (claude-md-bug-config.md) has one entry: **acme-backend**
  (Rust backend service, Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`).
- acme-backend is the only registered repository, so it is the target by default. But it is
  a Rust **backend** service, and the bug is about a **frontend** UI preference (theme
  toggle / browser persistence). No frontend repository is registered.

### Tooling

- The Code Intelligence section says "No Serena MCP servers are configured", even though the
  Registry lists `serena_backend`. Following that section (and the eval rule to make no MCP
  calls), the Read/Grep/Glob fallback applies. The codebase is simulated by
  `repo-context-mock.md`.

### Findings from the provided repository context

The mock repository context (`repo-context-mock.md`) says it covers **bug ACME-500**, not
ACME-511. Its contents:

| File | Content | Relevant to ACME-511? |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (convention lookup) | CONVENTIONS.md heading extraction via `line[3:]` does not strip trailing whitespace | **No** — unrelated to theme persistence |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (task enrichment) | Exact-match on `convention_name` fails when it has trailing whitespace | **No** |
| `evals/plan-feature/files/conventions-mock.md` | Eval fixture without trailing-whitespace headings | **No** |
| CONVENTIONS.md | Not present at the repository root | n/a — no conventions to apply |

**No code related to dark mode, theme state, the Settings > Appearance panel, user
preferences, `localStorage`/`sessionStorage`/cookies, or a preferences API was found** in
the provided context. Searches I would run against the real repo, none of which the mock
can answer:

- Symbols: `theme`, `darkMode`, `dark_mode`, `ThemeProvider`, `useTheme`, `preferences`,
  `UserPreferences`, `appearance`, `settings`
- Patterns: `localStorage`, `sessionStorage`, `document.cookie`, `prefers-color-scheme`,
  `data-theme`, `/preferences`, `/settings`

I did **not** reuse the trailing-whitespace defect from the mock as the cause of ACME-511.
It is a different bug (ACME-500) in a different area.

### Affected files / symbols

- **Not identified.** None of the provided material includes files that implement the dark
  mode toggle or its persistence.

### Existing test files and patterns

- No frontend/UI test files or theme-related tests were found in the provided context.
- The only test-like artifact in the mock is `evals/plan-feature/files/conventions-mock.md`,
  which does not apply.

### Reusable utilities

- None identified in the provided context.

### Persistence-impact analysis (database)

- The preference may be stored client-side (browser storage) or server-side (a user
  preferences table). Neither path appears in the provided context, so no database
  persistence boundary was found.
- Even if the backend stores the preference, the bug is that the value is **missing** after
  a restart, not that a wrong value was written. Existing records would not be stale, so
  **no data migration is required** based on what is available. Revisit this if the
  investigation finds that a wrong value (e.g., always `light`) is written to a
  preferences table at save time.

### Decomposition Guard (Step 6) check

The symptom points to a single defect: the theme preference is not saved durably and/or not
restored on load. That is one root-cause area, so the guard does not trigger.

### Investigation gaps (to carry forward)

1. The real files and symbols for the dark mode toggle and its persistence are unknown.
2. The repository that owns the frontend is not in the Repository Registry. Only
   `acme-backend` (Rust backend) is registered.
3. The Affects Version is unknown (see version-resolution.md), so the investigation cannot
   be scoped to a specific release.
