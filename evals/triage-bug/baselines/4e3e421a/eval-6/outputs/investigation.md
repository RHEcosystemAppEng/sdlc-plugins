# Steps 2–3 – Reproduce/Trace and Codebase Investigation: ACME-500

## Step 2 – Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce require running the `/plan-feature ACME-100` skill, which calls Jira
and an LLM agent. That cannot be run as a read-only command, and external services are not
allowed here. Outcome: **not directly reproducible. Traced through the code path instead.**

### Code-path trace

1. **Entry point:** `/plan-feature ACME-100` → `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
2. **Convention discovery:** plan-feature reads the target repo's `CONVENTIONS.md` and builds a
   map from section heading to content:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]          # no .strip()
           conventions[section_name] = current_section_content
   ```
   With the input `## Migration Patterns  `, the result is
   `section_name == "Migration Patterns  "` (two trailing spaces).
3. **Convention-aware task enrichment:** conventions are looked up by exact key:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   `"Migration Patterns" in {"Migration Patterns  ": ...}` → `False`.
4. **Divergence point:** the membership check fails and there is no `else` branch, warning, or
   log. The note is never added, so the generated task's Implementation Notes leave out the
   convention. This matches the Actual Result exactly.

## Step 3 – Codebase Investigation

### Target repository

- Component `sdlc-workflow` and the referenced code paths both point to the plan-feature
  skill.
- Registry entry: **acme-backend** — Serena instance `serena_backend`, Path
  `/home/dev/repos/acme-backend`.
- Code Intelligence says no Serena servers are configured, so the Read/Grep/Glob fallback
  applies. In this eval, the investigation used the supplied mock repository context
  (repo-context-mock.md) in place of live tool calls.

### Affected files and symbols

| File | Location / Symbol | Role in bug |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis: heading extraction loop (`section_name = line[3:]`) | **Defect site.** The heading text keeps its trailing whitespace. |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`if convention_name in discovered_conventions`) | Consumer. The exact-match lookup fails silently, with no warning when an expected convention is missing. |

### Impact analysis (callers / consumers)

- Every convention heading in any `CONVENTIONS.md` with trailing whitespace is affected, not
  just "Migration Patterns".
- Every Implementation Notes entry that cites conventions in plan-feature-generated tasks
  depends on this lookup. Downstream, `/implement-task` never sees the convention, so code
  can be written that breaks repo conventions (for example, missing FK indexes).
- Similar heading-parsing code may exist in other skills that read `CONVENTIONS.md`
  (triage-bug Step 3, implement-task). That is worth a quick check during the fix, but it is
  out of scope unless the same defect is confirmed there.

### Existing tests and patterns

- `evals/plan-feature/files/conventions-mock.md` is the existing plan-feature conventions
  fixture. Its headings have **no** trailing whitespace, so current evals do not cover this
  edge case.
- Reproducer pattern: add a variant fixture (or modify a copy) with `## Migration Patterns  `
  (trailing spaces), plus a plan-feature eval case in `evals/plan-feature/evals.json`. The
  case asserts that the generated Implementation Notes contain
  `Per CONVENTIONS.md §Migration Patterns`.

### Reusable utilities

- No shared heading-normalization helper was found in the mock context. The fix is a local
  normalization (`.strip()` / `.rstrip()`) at the extraction point.

### CONVENTIONS.md lookup

- The target repository has **no** `CONVENTIONS.md` at its root, so there are no
  repo-specific conventions to add to the Implementation Notes.

### Persistence-impact analysis

- The buggy output (a convention section-name map) exists only while plan-feature runs and
  ends up in generated Jira task text. Nothing writes it to an application database: no
  `insert`/`update`/ORM/SQL write appears in the call chain.
- **No persistence boundary found → no data migration needed.** Tasks already generated with
  the convention missing can be fixed by hand or re-planned. That is an operational note, not
  a schema/data migration.

### Decomposition Guard (Step 6) check

There is a single root cause: unnormalized heading extraction. The silent failure in the
consumer is a symptom of the same defect, plus a small hardening item (warn on a missing
expected convention) in the same file. **No decomposition needed.** One Task is appropriate.
