# Step 2 & 3 – Reproduction Trace and Codebase Investigation: ACME-500

## Step 2 – Reproduce / Trace

- The Steps to Reproduce call a skill (`/plan-feature ACME-100`) against a live Jira feature. You cannot run this as a read-only command, so **code-path tracing** was used instead of direct reproduction.
- Entry point: plan-feature convention conformance analysis -> convention-aware task enrichment.
- Divergence point: CONVENTIONS.md heading extraction keeps trailing whitespace. The later exact-match lookup then fails for `"Migration Patterns  "` vs `"Migration Patterns"`.
- Reproduction outcome: **confirmed by trace** (deterministic and not environment-dependent).

## Step 3 – Target repository

- Component `sdlc-workflow` and the code paths in the report point to the plan-feature skill.
- Repository Registry: **acme-backend** — Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`.
- Code Intelligence section: "No Serena MCP servers are configured." -> **Read/Grep/Glob fallback** applies. For this eval the repository content comes from repo-context-mock.md.

## Affected files and symbols

### 1. `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Convention conformance analysis (heading extraction)

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

- `line[3:]` takes everything after `"## "` with **no `.strip()` / `.rstrip()`**.
- For `## Migration Patterns  ` the stored key becomes `"Migration Patterns  "`.

### 2. `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Convention-aware task enrichment (lookup)

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

- Exact-match dictionary membership. `"Migration Patterns" in {"Migration Patterns  ": ...}` is `False`.
- There is no `else` branch and no warning when an expected convention is missing, so the miss is **silent**.

## Call path

```
CONVENTIONS.md content
  -> convention conformance analysis: section_name = line[3:]     (key keeps trailing spaces)
  -> discovered_conventions["Migration Patterns  "]
  -> task enrichment: "Migration Patterns" in discovered_conventions -> False
  -> notes.append(...) skipped, no warning
  -> generated task Implementation Notes omit the convention
```

## Existing tests / fixtures

- `evals/plan-feature/files/conventions-mock.md` is the existing plan-feature conventions eval fixture. It has **no** trailing whitespace on headings, so this edge case is not covered.
- The reproducer should follow that fixture pattern: add a variant fixture with trailing-whitespace headings, plus an eval case in `evals/plan-feature/evals.json`.

## Reuse candidates

- `evals/plan-feature/files/conventions-mock.md` — base fixture to copy for the trailing-whitespace variant.
- Heading extraction logic in plan-feature SKILL.md — the single place to normalise. The lookup side needs no new helper once keys are normalised at extraction.

## CONVENTIONS.md lookup

- The target repository has **no CONVENTIONS.md** at its root, so there are no repo conventions to add to Implementation Notes.

## Persistence-impact analysis

- The buggy output (convention section names) only lives in memory during a plan-feature run and goes into generated Jira task text. No database write (`insert`/`update`/ORM/SQL) appears anywhere in the call chain.
- **No persistence boundary found** -> no data migration is needed. Tasks already generated with the convention missing are not fixed by any migration. They can be regenerated or edited by hand if needed. This is not part of the fix scope.

## Decomposition Guard (Step 6)

- One root cause (heading text not normalised) shows up at two points in the same file: extraction stores the bad key, and lookup misses it silently. This is a single defect, so it is **not** a decomposition trigger. One Task is appropriate. Adding the missing-convention warning is part of the same fix, because the bug report specifically complains about silent dropping.
