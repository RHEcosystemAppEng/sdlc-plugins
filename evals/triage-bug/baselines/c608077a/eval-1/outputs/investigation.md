# Steps 2–3 — Reproduce/Trace and Codebase Investigation (ACME-500)

## Step 2 — Reproduce / Trace

### Runnable reproduction

Not attempted. The Steps to Reproduce require a `/plan-feature` skill invocation against
a live Jira feature (ACME-100), which is an interactive skill run with Jira side effects,
not a read-only command. This is a skill/documentation-level bug, so **code-path tracing**
is used instead.

### Code-path trace

1. **Entry point**: `/plan-feature ACME-100` → `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
2. **Convention lookup** (convention conformance analysis): the skill reads the target
   repository's `CONVENTIONS.md` and builds a map of section name → section content:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
3. **Divergence point**: `line[3:]` returns everything after `"## "` verbatim. For the input
   line `## Migration Patterns  `, the key stored is `"Migration Patterns  "` (two trailing
   spaces), not `"Migration Patterns"`.
4. **Convention-aware task enrichment**: later the skill matches by exact name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   `"Migration Patterns" in {"Migration Patterns  ": ...}` is `False`, so no note is appended.
5. **No else-branch / no warning**: when a convention is not found, nothing is logged, which
   produces the "silently dropped" Actual Result.

Trace outcome: the Actual Result is fully explained by the trace — **confirmed by trace**.

## Step 3 — Codebase Investigation

### Target repository

- Component `sdlc-workflow` and the file paths in the trace point to the plan-feature skill.
- Repository Registry entry: `acme-backend` (Serena instance `serena_backend`, path
  `/home/dev/repos/acme-backend`). The repository context fixture (repo-context-mock.md)
  describes this repository as containing `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
- Code Intelligence: no Serena servers are configured, so the Read/Grep/Glob fallback applies
  (simulated here via repo-context-mock.md).

### Affected files and symbols

| File | Location / symbol | Role in bug |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis — CONVENTIONS.md heading extraction (`section_name = line[3:]`) | **Defect**: heading text not whitespace-normalized before being used as a map key |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`if convention_name in discovered_conventions`) | Consumer: exact-match lookup fails against the un-stripped key; no warning on miss |

Both locations are in the same file and stem from a single root cause (un-normalized heading
keys). This is **not** a decomposition trigger (Step 6) — one Task is appropriate.

### Impact analysis (callers / consumers)

- The extracted `conventions` map is the only source used by convention-aware task
  enrichment, so every convention whose heading carries trailing whitespace (spaces or tabs,
  and also `\r` from CRLF line endings, since the split is on `'\n'` only) is dropped.
- Any repository whose CONVENTIONS.md was edited in an editor that preserves trailing
  whitespace, or saved with Windows line endings, is affected.

### Existing tests / patterns for the reproducer

- `evals/plan-feature/files/conventions-mock.md` — existing eval fixture for plan-feature
  convention handling. Its headings have **no** trailing whitespace, so this edge case is
  currently uncovered. The reproducer should be a new fixture modelled on it, plus a
  corresponding eval entry in `evals/plan-feature/evals.json`.

### Reusable patterns

- The existing heading-extraction logic is the place to fix; no new helper is needed —
  normalizing with `.strip()` (or `.rstrip()` plus `\r` removal) at the extraction point
  covers both the map key and all downstream lookups.
- The existing `conventions-mock.md` fixture structure should be reused for the new
  whitespace fixture.

### CONVENTIONS.md lookup

The repository has **no** `CONVENTIONS.md` at its root — no repository-specific conventions
to apply to the Task's Implementation Notes.

### Persistence-impact analysis

The defective output (the convention section-name map) is computed in-memory during each
`/plan-feature` run and consumed immediately to build task descriptions. It is not written
to any database. **No persistence boundary found — no data migration required.**
(Previously generated Jira tasks that omitted conventions are not auto-corrected, but these
are not database records owned by the codebase; re-running plan-feature after the fix
regenerates correct output.)

### Decomposition guard check (Step 6)

Single root cause (heading extraction does not strip whitespace) manifesting at two points in
one file. Decomposition Guard **not triggered**.
