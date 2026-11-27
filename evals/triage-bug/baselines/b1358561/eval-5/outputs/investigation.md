# Steps 2–3 – Reproduction/Trace and Codebase Investigation: ACME-511

## Step 2 – Reproduce/Trace

The Steps to Reproduce are manual browser interactions (Settings > Appearance >
toggle Dark Mode > close/reopen browser). There are no runnable CLI/curl/test
commands, so direct reproduction is not possible in this session. Code-path
tracing was attempted instead (below).

Expected trace for this class of bug:
1. Entry point: Dark Mode toggle handler in the Settings > Appearance UI.
2. Write path: where the toggle value is stored (in-memory state, sessionStorage,
   localStorage/cookie, or a backend user-preferences endpoint).
3. Read path: app bootstrap / theme initialization on page load.
4. Divergence: the value written in (2) is not available, or is not read, in (3)
   after a full browser restart.

## Step 3 – Codebase Investigation

### Target repository

- Component field: `sdlc-workflow`
- Repository Registry has a single entry: **acme-backend** (Rust backend service,
  Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`).
- Code Intelligence section states no Serena servers are configured, so the
  fallback (Read/Grep/Glob) applies. In this eval, the repository content is
  supplied by `repo-context-mock.md`.

### Findings from the provided repository context

The repository context (`repo-context-mock.md`) does **not** contain any code
related to this bug. It explicitly describes code paths "for bug ACME-500" and
covers only:

- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — CONVENTIONS.md heading
  extraction (`line[3:]` without stripping trailing whitespace) and convention
  name matching in task enrichment.
- `evals/plan-feature/files/conventions-mock.md` — an eval fixture lacking
  trailing-whitespace headings.
- No CONVENTIONS.md at the repository root.

None of these relate to dark mode, theme selection, user preferences, settings UI,
browser storage, or session handling. Searches over the provided context for
`dark`, `theme`, `appearance`, `preference`, `localStorage`, `sessionStorage`,
`cookie`, and `settings` return no matches.

### Mismatch between bug and registry

- The bug describes a **front-end/browser** behavior (settings panel, browser
  restart). The only registered repository is a **Rust backend service**. The
  front-end application that renders Settings > Appearance is not in the
  Repository Registry.
- The Component (`sdlc-workflow`) does not obviously correspond to a UI theming
  module either.

### Affected files / symbols

**Not identified.** No file paths or symbols could be confirmed. Per the skill's
rules ("Do not guess"; "File paths must be real paths discovered during
repository or code analysis"), none are asserted here.

### Persistence-impact analysis

Not performable — no buggy function was located, so its output cannot be traced to
a persistence boundary. If the fix involves a backend user-preferences table, it
is likely that no existing rows contain *incorrect* values (the bug is a missing
write/read, not a wrong computed value), so a data migration is probably not
required — but this must be confirmed once the code is found.

### Test patterns / reuse candidates

None discoverable from the provided context (the only test fixture referenced is a
plan-feature eval for CONVENTIONS.md, unrelated to this bug).

### CONVENTIONS.md

Not present at the repository root (per repo context).

### Investigation gaps to resolve before/while implementing

1. Identify the front-end repository that hosts Settings > Appearance and add it to
   the Repository Registry (with a Serena instance if available).
2. Locate the dark-mode toggle handler and its storage mechanism.
3. Locate theme initialization at app startup.
4. Determine whether acme-backend exposes a user-preferences API that the front end
   should be calling, and whether the theme preference is part of it.
