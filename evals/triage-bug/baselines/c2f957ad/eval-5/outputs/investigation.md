# Steps 2–3 – Reproduce/Trace and Codebase Investigation: ACME-511

## Step 2 – Reproduce/Trace

- Steps to Reproduce are manual browser UI interactions (Settings > Appearance > Dark Mode
  toggle, close/reopen browser). There are no runnable CLI/API/test commands, so a runnable
  reproduction was not attempted.
- Code-path tracing was attempted instead. Entry point: the Settings > Appearance
  "Dark Mode" toggle handler and the application's startup theme initialization.
- Expected divergence point: either (a) the toggle handler never writes the preference to
  durable storage (localStorage / cookie / server-side user settings), or (b) the value is
  written but app startup does not read it back and defaults to light mode.

## Step 3 – Codebase Investigation

### Target repository

- Component field: `sdlc-workflow`.
- Repository Registry contains a single entry: **acme-backend** (Rust backend service,
  Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`).
- Code Intelligence: no Serena servers are configured, so investigation falls back to
  Read/Grep/Glob over the provided repository context (repo-context-mock.md).

### Findings from the provided repository context

The repository context (repo-context-mock.md) describes code paths for a **different bug
(ACME-500)**: CONVENTIONS.md heading extraction in
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (`line[3:]` not stripping trailing
whitespace) and the convention-aware task enrichment match. The test fixture referenced is
`evals/plan-feature/files/conventions-mock.md`.

None of this is related to ACME-511. Searches of the provided context for terms relevant to
this bug found no matches:

| Search term | Matches |
|---|---|
| `dark`, `theme`, `appearance` | 0 |
| `localStorage`, `sessionStorage`, `cookie` | 0 |
| `preference`, `settings`, `user_settings` | 0 |

### Observations / gaps

1. **No affected files or symbols identified.** The investigation could not locate the
   dark-mode toggle handler, theme initialization code, or any preference storage path.
2. **Possible repository mismatch.** The bug describes browser UI behavior (a frontend
   concern), while the only registered repository is a Rust backend. If preferences are
   stored server-side, acme-backend may own a user-settings endpoint/table; if they are
   stored client-side, the defect lives in a frontend repository that is not in the
   Repository Registry. The Component (`sdlc-workflow`) also does not narrow this down.
3. **CONVENTIONS.md**: the repository context states there is no CONVENTIONS.md at the
   repository root, so no conventions inform the task.
4. **Existing tests**: no test files related to theme/preference persistence were found
   in the provided context.

### Persistence-impact analysis

- Could not trace a buggy function to a persistence boundary because no function was
  identified.
- Note: this bug is about a preference that is *not* persisted (or not read back), not
  about an incorrect value being persisted. Even if the fix adds server-side persistence,
  existing stored records would not contain wrong values, so a data migration is **not
  expected** to be needed. This should be re-checked once the actual code path is found
  (e.g., if a `user_settings.theme` column exists and has been written with a wrong default).

### Decomposition Guard (Step 6)

No evidence of multiple independent root causes. A single Task is appropriate.
