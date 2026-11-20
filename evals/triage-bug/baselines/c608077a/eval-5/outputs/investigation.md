# Steps 2–3 – Reproduce/Trace and Codebase Investigation: ACME-511

## Step 2 – Reproduce/Trace

- **Runnable reproduction:** not possible. The Steps to Reproduce are manual browser actions (open the app, Settings > Appearance, toggle Dark Mode, close and reopen the browser). They include no CLI command, curl call, or test command. The environment is "staging", which this eval cannot reach. **Outcome: environment-dependent, not reproduced.**
- **Code-path tracing:** the entry point would be the Settings > Appearance "Dark Mode" toggle and its change handler. From there, the persistence path for the preference would be one of:
  1. a client-side store such as `localStorage`, `sessionStorage`, a cookie, or in-memory state, or
  2. a backend user-preferences API plus a database row.

  On load, the app would need to read the preference back before choosing a theme. The divergence is either that the preference is never written to durable storage or that it is never read back at startup.

## Step 3 – Codebase Investigation

### Target repository

| Signal | Value | Conclusion |
|---|---|---|
| Component field | `sdlc-workflow` | Not a registered repository. This looks like a plugin/skills component, not a UI app. |
| Steps to Reproduce | Browser UI: Settings > Appearance | Points to a frontend web application |
| Repository Registry | Only `acme-backend` (Rust backend service, Serena `serena_backend`, `/home/dev/repos/acme-backend`) | No frontend repository is registered |

The only candidate is **acme-backend**. It could hold the server side of a user-preferences API, if the app stores preferences on the server.

### Code intelligence

The Registry lists Serena instance `serena_backend`, but the Code Intelligence section says "No Serena MCP servers are configured." The skill falls back to Read/Grep/Glob. In this eval, all code context comes from `repo-context-mock.md`.

### Findings from the provided repository context

`repo-context-mock.md` says it simulates code paths "for bug ACME-500", not ACME-511. It contains:

- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`: CONVENTIONS.md heading extraction (`section_name = line[3:]` keeps trailing whitespace) and convention-aware task enrichment (`if convention_name in discovered_conventions:` fails on exact match).
- `evals/plan-feature/files/conventions-mock.md`: an eval fixture with no trailing-whitespace headings.
- No CONVENTIONS.md at the repository root.

**None of this relates to dark mode, theme handling, user preferences, settings UI, browser storage, or session/cookie persistence.** The context has:

- no theme or dark-mode symbols (e.g. `theme`, `darkMode`, `appearance`, `colorScheme`)
- no user-preferences model, endpoint, or table
- no frontend code or test files for the Settings > Appearance panel

Pinning the dark-mode defect on the CONVENTIONS.md whitespace bug would be wrong. That is a separate defect (ACME-500).

### Searches that a real run would perform (not executed here)

On the frontend repo, once registered, and on acme-backend:

- `search_for_pattern` / Grep for `darkMode|dark_mode|theme|colorScheme|prefers-color-scheme|appearance`
- Grep for `localStorage|sessionStorage|document.cookie` near theme code
- `find_symbol` for `Preference`, `UserSettings`, `Theme` in acme-backend, then `find_referencing_symbols` on any preferences endpoint or handler
- Look for existing tests for the settings panel and the preferences API to base the reproducer test on

### Persistence-impact analysis

- No buggy function was located, so no persistence boundary could be traced.
- Based on the symptom, the likely defect is that the value is **never** written durably, or never read back. It is not that a wrong value was persisted at ingestion. If so, no stale records need correcting, and **no data migration is expected**.
- Re-check this once the code is found. If a preferences table exists and holds wrong or defaulted values, a migration may be needed.

### CONVENTIONS.md

None at the acme-backend root, per the mock context. No conventions apply.

### Reusable utilities / existing test patterns

None identified in the provided context for this bug.

### Investigation gaps (blocking a confident root cause)

1. No frontend repository is in the Repository Registry, but the bug is a browser UI behavior.
2. The repository context supplied is for a different bug (ACME-500).
3. The Component (`sdlc-workflow`) does not match the reported behavior and may be mis-set.
4. The environment (staging) and the version are unknown.
