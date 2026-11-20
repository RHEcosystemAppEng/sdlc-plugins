# Steps 2–3 – Reproduce/Trace and Codebase Investigation: ACME-500

## Step 2 – Reproduce / Trace

Reproduction is not directly runnable (requires invoking `/plan-feature ACME-100` against a live
Jira feature — a skill/documentation bug). Used **code-path tracing** instead.

Trace:
1. Entry point: `/plan-feature ACME-100` -> plan-feature Step 3 "CONVENTIONS.md lookup"
   (reads `<repo Path>/CONVENTIONS.md`).
2. Heading extraction (convention conformance analysis) in
   `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]          # no .strip()
           conventions[section_name] = current_section_content
   ```
   With input `## Migration Patterns  `, `section_name == "Migration Patterns  "`.
3. Convention-aware task enrichment (same file, "Convention-aware task enrichment"):
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   `"Migration Patterns" in {"Migration Patterns  ": ...}` -> False.
4. Divergence point: the dict key carries trailing whitespace, so the exact-match lookup fails and
   the branch that appends the note is skipped with no else/warning -> convention silently dropped.

Outcome: **confirmed by trace** (Actual Result matches the traced behaviour).

## Step 3 – Codebase Investigation

- **Target repository:** acme-backend (Registry Path `/home/dev/repos/acme-backend`), chosen from
  Component `sdlc-workflow` and the `/plan-feature` code path. Registry lists Serena instance
  `serena_backend`, but the Code Intelligence section states no Serena servers are configured ->
  Read/Grep/Glob fallback (simulated via repo-context-mock.md).

### Affected files / symbols

| File | Symbol / Section | Role |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis — heading extraction `section_name = line[3:]` | **Defect site**: heading text not whitespace-normalized |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment — `if convention_name in discovered_conventions` | Consumer: exact-match lookup fails; no warning on miss |

### Impact analysis
- Every convention whose `## ` heading has trailing whitespace (or tabs / `\r` from CRLF files) is
  dropped from all generated tasks. CRLF-authored CONVENTIONS.md files would trigger the same
  failure on every heading (`"Migration Patterns\r"`).
- Downstream: implement-task follows the task faithfully and misses the convention (e.g., missing
  FK indexes in migrations).

### Tests / fixtures
- `evals/plan-feature/files/conventions-mock.md` — existing plan-feature conventions fixture; has
  no trailing whitespace on headings, so the edge case is uncovered. Pattern to follow for a new
  fixture + eval assertion.

### CONVENTIONS.md
- Not present at the acme-backend root -> no repo conventions to apply to the fix task.

### Persistence-impact analysis
- Output of the buggy logic (convention name -> task Implementation Notes) is consumed at
  task-generation time and written into Jira task descriptions, not a database. No database
  persistence boundary (no table/column, no insert/update) -> **no data migration needed**.
  (Already-generated Jira tasks that missed conventions are out of scope for an automated fix.)

### Decomposition guard (Step 6)
- Single root cause (unnormalized heading key) manifesting at extraction and lookup -> **not** a
  decomposition trigger; one Task is appropriate.
