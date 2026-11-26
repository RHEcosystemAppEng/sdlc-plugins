# Steps 2-3 — Reproduce/Trace and Codebase Investigation: ACME-500

## Step 2 — Reproduce / Trace

### Runnable reproduction

Not attempted. The Steps to Reproduce require running the `/plan-feature` skill against a live
Jira feature (ACME-100). That is an interactive, Jira-backed workflow, not a self-contained CLI
or test command, and external tools are out of scope for this run. Outcome: **environment-dependent;
used code-path tracing instead.**

### Code-path tracing

1. **Entry point:** `/plan-feature ACME-100` → the plan-feature skill
   (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`).
2. **Convention conformance analysis (heading extraction):** the skill reads `CONVENTIONS.md`
   and builds a map from section name to content:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
   Input line `## Migration Patterns  ` gives key `"Migration Patterns  "` (two trailing spaces).
3. **Convention-aware task enrichment (lookup):**
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   The lookup uses `convention_name = "Migration Patterns"`. The dict holds
   `"Migration Patterns  "`, so `in` returns False. No note is appended, and there is no `else`
   branch, so nothing is logged.
4. **Divergence point:** the behavior goes wrong at the extraction step (`line[3:]` with no
   strip). It becomes visible at the enrichment step, which silently skips the miss.

The trace matches the Actual Result exactly: the convention is missing and no warning is shown.

## Step 3 — Codebase Investigation

### Target repository

- Component `sdlc-workflow` and the code paths named in the bug point to the plan-feature skill.
- Repository Registry entry: `acme-backend` (Serena instance `serena_backend`, path
  `/home/dev/repos/acme-backend`).
- Code Intelligence says no Serena servers are configured, so investigation uses the
  **Read/Grep/Glob fallback** (simulated here from repo-context-mock.md).

### Affected files and symbols

| File | Location / symbol | Role in the bug |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis: heading-extraction loop (`section_name = line[3:]`) | **Defect site.** Trailing whitespace is not stripped from heading text |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`if convention_name in discovered_conventions`) | Where the failure shows. Exact-match lookup misses, with no warning on a miss |

### Impact analysis

- Every convention whose `CONVENTIONS.md` heading has trailing whitespace (spaces or tabs, and
  `\r` from CRLF line endings) is dropped from generated tasks. CRLF files are especially
  exposed because `split('\n')` leaves a trailing `\r` on every heading.
- Only plan-feature task enrichment is affected. The defect is a single root cause in one file,
  so the **Decomposition Guard (Step 6) is not triggered**.

### Existing tests / fixtures

- `evals/plan-feature/files/conventions-mock.md` is the existing plan-feature conventions eval
  fixture. Its headings have **no** trailing whitespace, so current evals do not cover this
  edge case. It shows the fixture format to copy for a reproducer fixture.

### Reusable patterns

- Use Python `str.strip()` / `rstrip()` on the extracted heading. This is the standard idiom and
  needs no new helper.
- The plan-feature eval structure (`evals/plan-feature/evals.json` plus `files/` fixtures) is
  the pattern for adding a reproducer eval case.

### CONVENTIONS.md lookup

The target repository has **no** `CONVENTIONS.md` at its root, so no repository conventions apply
to the Implementation Notes.

### Persistence-impact analysis

The buggy output is the in-memory `conventions` dict. It feeds the generated task description
text. Tracing callers shows no database write (`insert`/`update`/`save`/ORM/SQL). The value is
recomputed on every plan-feature run. **No persistence boundary, so no data migration is needed.**
Tasks generated earlier without the convention can be regenerated or edited by hand. That is
noted in the Task but is not a migration.
