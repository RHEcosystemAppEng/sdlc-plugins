# Steps 2-3 — Reproduction/Trace and Codebase Investigation: ACME-500

## Step 2 — Reproduce / Trace

### Runnable reproduction
Not attempted. The Steps to Reproduce invoke a Claude Code skill (`/plan-feature ACME-100`)
that depends on Jira and an interactive agent session; there is no deterministic CLI/curl/test
command to run read-only. Outcome: **environment-dependent — traced via code path instead**.

### Code-path trace
1. **Entry point**: `/plan-feature ACME-100` -> `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
2. plan-feature reads the target repository's `CONVENTIONS.md` during its
   **convention conformance analysis** step.
3. Heading extraction logic (excerpt from SKILL.md):
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
   For the input line `## Migration Patterns  `, `section_name` becomes
   `"Migration Patterns  "` (two trailing spaces preserved). Note also that a CRLF file
   would leave a trailing `\r` for the same reason.
4. **Convention-aware task enrichment** step (excerpt from SKILL.md):
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   Lookup key `"Migration Patterns"` does not equal the stored key `"Migration Patterns  "`,
   so the membership test is False.
5. **Divergence point**: there is no `else` branch — no warning, no fallback. The note
   `Per CONVENTIONS.md §Migration Patterns: ...` is never appended, matching the Actual Result
   (convention silently dropped).

## Step 3 — Codebase Investigation

### Target repository
- Component `sdlc-workflow` and the file paths in the trace point to the
  `plugins/sdlc-workflow/skills/plan-feature/` code path.
- Repository Registry lists a single repository: **acme-backend**
  (Serena instance `serena_backend`, Path `/home/dev/repos/acme-backend`). The task is
  scoped to this repository.

### Code intelligence
- The Registry names `serena_backend`, but the Code Intelligence section states no Serena MCP
  servers are configured. Per the skill's fallback, investigation uses Read/Grep/Glob on the
  repository path (simulated here by repo-context-mock.md; no external tools called).

### Affected files and symbols

| File | Location / symbol | Role in bug |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis — heading extraction `section_name = line[3:]` | **Defect origin**: heading text is not normalized (no `.strip()` / trailing-whitespace trim) |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment — `if convention_name in discovered_conventions:` | **Manifestation**: exact-match lookup fails; no warning on miss |

Single root cause (un-normalized heading key) manifesting in two adjacent steps of the same
file — **not** a decomposition trigger (Step 6): one Task is appropriate.

### Impact analysis (callers / consumers)
- Every convention section read by plan-feature passes through the same extraction, so any
  heading with trailing spaces/tabs (or `\r` from CRLF line endings) is silently dropped, not just
  `Migration Patterns`.
- Consumers: generated Task descriptions' Implementation Notes -> `/implement-task`, which then
  implements without the convention (e.g., missing `Index::create()` for FK columns).

### Existing tests / fixtures
- `evals/plan-feature/files/conventions-mock.md` — existing plan-feature conventions eval fixture.
  Its headings have **no trailing whitespace**, so the edge case is uncovered. This is the pattern
  to follow for the reproducer (a fixture variant with trailing whitespace on a heading, plus an
  eval case in `evals/plan-feature/evals.json` asserting the convention note appears).

### Reuse candidates
- Existing heading extraction loop in plan-feature SKILL.md — fix in place by normalizing the key
  (trim trailing whitespace) rather than introducing a new parser.
- `evals/plan-feature/files/conventions-mock.md` — base fixture to copy/extend for the reproducer.

### CONVENTIONS.md lookup
- No `CONVENTIONS.md` at the acme-backend repository root. No repo-specific conventions to apply.

### Persistence-impact analysis
- The buggy output (convention-name dict keys -> Implementation Notes text) is computed at
  planning time inside the skill run and written only into newly generated Jira task descriptions.
  No database `insert`/`update`/ORM write exists on this path.
- **No persistence boundary found** — no data migration required. (Previously generated tasks
  that omitted conventions are not auto-correctable; they could be re-planned manually if needed,
  but that is out of scope for the fix task.)

### Decomposition guard (Step 6)
- Single root cause -> single Task. No user prompt needed.
