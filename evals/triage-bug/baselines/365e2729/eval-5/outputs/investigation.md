# Steps 2–3 – Reproduce/Trace and Codebase Investigation (ACME-511)

## Step 2 – Reproduce/Trace

- Steps to Reproduce are manual browser UI interactions (Settings > Appearance >
  toggle Dark Mode, close browser, reopen). There are no runnable CLI/API/test
  commands, so direct reproduction was **not attempted**.
- Code-path tracing: the entry point is the "Dark Mode" toggle in the Settings >
  Appearance panel. The expected path is: toggle handler -> theme state update ->
  persistence write (browser storage such as `localStorage`/cookie and/or a
  user-preferences API) -> on app start, read the persisted preference -> apply the
  theme before first render.
- The Actual Result (theme and toggle both reset to OFF after the browser restarts)
  means the preference is not being stored anywhere that outlives the browser
  session, or it is stored but not read back when the app starts.

## Step 3 – Codebase Investigation

### Target repository

- Component: `sdlc-workflow`
- Repository Registry has one entry: **acme-backend** (Rust backend service,
  Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`).
- Code Intelligence says no Serena MCP servers are configured, so the Read/Grep/Glob
  fallback applies. In this eval, the repository content comes from
  `repo-context-mock.md`.

### Findings from the available repository context

The repository context lists only these code paths:

| File | Content | Relevant to ACME-511? |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | CONVENTIONS.md heading extraction (`line[3:]` doesn't strip trailing whitespace) | **No.** This is about convention parsing (written for ACME-500), not theme persistence |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`if convention_name in discovered_conventions`) | **No** |
| `evals/plan-feature/files/conventions-mock.md` | Eval fixture for conventions | **No** |
| `CONVENTIONS.md` | Not present at repo root | n/a. No conventions to apply |

Searches I would run in the target repo (Grep fallback), none of which match
anything in the available context:

- `dark`, `darkMode`, `dark_mode`, `theme`, `Appearance`, `prefers-color-scheme`
- `localStorage`, `sessionStorage`, `cookie`, `user_preferences`, `settings`
- Backend: user-settings/preferences endpoints, tables or columns (`theme`,
  `preferences`), and migrations that touch them

**Result: no files, symbols or tests related to dark mode, theme state, the
Settings/Appearance panel, or user-preference persistence were found.**

### Repository mismatch

- The bug describes **browser UI behaviour** (a settings toggle and theme on page
  load). The only registered repository is a **Rust backend service**. The UI code
  (toggle, theme provider, client-side storage) is very likely in a frontend
  repository that is not in the Repository Registry.
- The backend may still be involved if preferences are meant to be saved per user
  on the server, for example through a user-settings endpoint. Nothing in the
  available context confirms or rules this out.
- The Component value `sdlc-workflow` doesn't match the subject of the bug
  (application theming). It looks like it was set incorrectly.

### Persistence-impact analysis

- No buggy function was identified, so the output could not be traced to a
  persistence boundary.
- From the bug's behaviour, the defect is most likely that the preference is
  **not** persisted. That would mean there are no stale database records to fix,
  and no data migration is expected.
- If the investigation finds a backend preferences column that stores a wrong
  value (rather than no value), revisit this and add a migration.

### Existing test patterns

- No tests for theme or preferences were found in the available context.
- The only test-related file found (`evals/plan-feature/files/conventions-mock.md`)
  is unrelated.

### Decomposition guard (Step 6)

- Only one symptom and one likely root cause (the preference isn't stored or isn't
  restored). There is no sign of several independent defects, so a single Task is
  appropriate.
