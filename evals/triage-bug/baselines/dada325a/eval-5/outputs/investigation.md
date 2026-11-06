# Steps 2 and 3 – Reproduction/Trace and Codebase Investigation (ACME-511)

## Step 2 – Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce are manual browser interactions: open the app, go to Settings >
Appearance, toggle Dark Mode, close and reopen the browser. There are no CLI commands,
curl calls, or test commands to run, and the eval runs offline with no access to the
staging deployment. **Reproduction outcome: environment-dependent / not attempted.**

### Code-path tracing

Entry point from the Steps to Reproduce: the **Settings > Appearance > "Dark Mode" toggle**
in the web UI. The expected flow for a persisted UI preference is:

1. Toggle change handler updates the in-memory theme state.
2. The preference is written to durable storage, either client-side (`localStorage`,
   cookie, IndexedDB) or server-side (user-preferences API, then the database).
3. On application bootstrap, the stored preference is read and applied before or at
   first render.

The bug report (state reverts after a full browser restart) shows that step 2 or step 3
is broken. Likely points of divergence:
- The value is kept only in memory or in `sessionStorage`, which is cleared when the browser closes.
- The value is written but never read back on bootstrap. The theme initializer uses a hard-coded default of `light`.
- The value is read too late and then overwritten by a default.
- A server-side preferences endpoint is not called, or its response is ignored.

The available code context does not show which of these applies. See Step 3.

## Step 3 – Codebase Investigation

### Target repository

- Component on the Bug: `sdlc-workflow`
- Repository Registry (CLAUDE.md) has one entry: **acme-backend** (Rust backend service),
  Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`.
- Code Intelligence says **no Serena MCP servers are configured**, so the
  fallback (Read/Grep/Glob) applies. In this eval, the provided repository context
  (`repo-context-mock.md`) stands in for the repository.

### Findings from the repository context

The context in `repo-context-mock.md` covers:

| File | Content | Relevant to ACME-511? |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (convention conformance) | `CONVENTIONS.md` heading extraction with `line[3:]` does not strip trailing whitespace | **No.** This concerns parsing CONVENTIONS.md headings |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (task enrichment) | Exact-match lookup `convention_name in discovered_conventions` fails on trailing whitespace | **No** |
| `evals/plan-feature/files/conventions-mock.md` | Eval fixture with no trailing-whitespace headings | **No** |
| `CONVENTIONS.md` | Not present at repo root | N/A. No conventions to apply |

The mock header says the context was prepared for **bug ACME-500** (a CONVENTIONS.md
heading whitespace defect), not ACME-511.

**No code related to the defect was found.** The investigated context contains none of the following:
- Settings / Appearance UI component or dark-mode toggle handler
- Theme provider, theme state store, or theme bootstrap/initialization code
- Client-side persistence calls (`localStorage`, `sessionStorage`, cookies)
- User-preference API endpoint, model, or database table (for example a `user_preferences`
  table or `theme` column)
- Existing tests for theme or preference behavior

There is also a structural mismatch. The only registered repository is a **Rust backend
service**, but the bug describes front-end UI behavior. Either the front-end repository is
missing from the Repository Registry, or persistence is meant to be backend-driven
(a preferences API) and that code is not in the provided context.

### Persistence-impact analysis

- The buggy function could not be identified, so the output could not be traced to a persistence boundary.
- Even so, a data migration is **unlikely to be needed**. The symptom is a preference that is
  *not stored* or *not read back*. That is different from an incorrect value written at
  ingestion time. If the fix adds a new server-side column or table for the
  preference, that is a **schema** migration, not a corrective data migration. The
  implementer should confirm this once the code is located.

### CONVENTIONS.md lookup

No `CONVENTIONS.md` at the repository root, so there are no conventions to apply.

### Reusable utilities / test patterns

None identified in the available context.

### Decomposition Guard (Step 6) check

The bug describes one symptom with one expected behavior. Nothing points to multiple
independent root causes, so the guard is **not triggered**. One Task is appropriate.

### Investigation summary

| Goal | Status |
|---|---|
| Affected files/symbols identified | **Not determined.** No relevant code in the provided context |
| Code paths involved | Inferred only (toggle, persist, bootstrap/read). Not confirmed in code |
| Patterns for Implementation Notes | None found |
| Existing test files for the reproducer | None found |
| Reusable utilities | None found |
| Persistence boundary | Not determined. Corrective data migration unlikely |

Following the skill's "Do not guess" rule, the root cause analysis and Task below give the
defect location as **unconfirmed** and do not invent file paths.
