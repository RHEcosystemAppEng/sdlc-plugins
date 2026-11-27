# Steps 2-3 — Reproduce/Trace and Codebase Investigation (ACME-500)

## Step 2 — Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce call a skill (`/plan-feature ACME-100`) that needs Jira and an LLM agent session. That is not a read-only CLI command, so the bug **cannot be reproduced directly**. Code-path tracing was used instead.

### Code-path trace

1. **Entry point:** `/plan-feature ACME-100` runs `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
2. **Convention lookup (conformance analysis):** plan-feature reads `CONVENTIONS.md` and builds a map from section name to content:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
   With the input line `## Migration Patterns  `, `section_name` becomes `"Migration Patterns  "` with two trailing spaces.
3. **Convention-aware task enrichment:** conventions are matched by exact section name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   The lookup key `"Migration Patterns"` does not equal the stored key `"Migration Patterns  "`. The `in` check returns `False`, so no note is added.
4. **Where behavior diverges:** in step 2, `line[3:]` keeps trailing whitespace. In step 3 the exact-match lookup then fails, and the code has no else branch and no warning. The convention is dropped **silently**, which matches the Actual Result.

Outcome: **confirmed by trace.** The Actual Result follows directly from the code path above.

## Step 3 — Codebase Investigation

### Target repository

- Component `sdlc-workflow` and the affected path `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` identify the target.
- Repository Registry entry: `acme-backend`, Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`.
- Code Intelligence says no Serena servers are configured, so Read/Grep/Glob would be used. For this eval, the findings come from `repo-context-mock.md`.

### Affected files and symbols

| File | Location / symbol | Role in bug |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis: heading extraction loop (`section_name = line[3:]`) | **Defect site.** It does not strip trailing whitespace from the heading text. |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`if convention_name in discovered_conventions`) | Consumer. Its exact-match lookup fails on the unnormalized key, and a miss produces no warning. |

### Impact analysis (callers and consumers)

- The extracted `conventions` map is used only by the task-enrichment step in the same skill. Every convention whose heading has trailing whitespace (or a trailing tab) is dropped from all generated tasks.
- No other skill is shown consuming this extraction logic. This is a single defect, so the decomposition guard does not apply.

### Test files and patterns

- `evals/plan-feature/files/conventions-mock.md` is the existing plan-feature conventions eval fixture. Its headings have **no** trailing whitespace, so current evals do not cover this edge case.
- The reproducer should follow the existing eval pattern: a fixture file under `evals/plan-feature/files/` plus an eval entry with assertions in `evals/plan-feature/evals.json`.

### Reusable utilities / patterns

- The repository context shows no shared heading-normalization helper. The fix is to normalize in place by stripping the extracted heading (for example `line[3:].strip()`) and to normalize the lookup key the same way.

### CONVENTIONS.md lookup

- The repository has no `CONVENTIONS.md` at its root, so no repo-specific conventions apply to the Implementation Notes.

### Persistence-impact analysis

- The buggy output is the convention section-name map. It is used in memory, during the plan-feature run, to build task descriptions. **No persistence boundary was found**: nothing writes the extracted heading to a database.
- Tasks already created in Jira by earlier plan-feature runs may lack the convention. They are generated artifacts, not stored computed values. **No data migration is needed.**

### Decomposition guard (Step 6) check

There is one root cause: heading extraction does not normalize whitespace. It shows up in two adjacent steps of one file. This is **not** a decomposition trigger, so a single Task is appropriate.
