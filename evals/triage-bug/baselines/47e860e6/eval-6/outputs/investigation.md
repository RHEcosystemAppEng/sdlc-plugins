# Steps 2 & 3 — Reproduce/Trace and Codebase Investigation (ACME-500)

## Step 2 — Reproduce / Trace

### Runnable reproduction?

The Steps to Reproduce call a Claude Code skill (`/plan-feature ACME-100`), which needs Jira access and an interactive agent session. There is no CLI or curl command that can be run read-only. **Outcome: not directly reproducible.** The skill falls back to code-path tracing.

### Code-path trace

1. **Entry point:** `/plan-feature ACME-100`, which loads `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
2. **CONVENTIONS.md load / heading extraction** (plan-feature convention conformance analysis):
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]          # no .strip() / .rstrip()
           conventions[section_name] = current_section_content
   ```
   Input line `## Migration Patterns  ` gives the key `"Migration Patterns  "` (two trailing spaces).
3. **Convention-aware task enrichment** (same SKILL.md):
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   The lookup key `"Migration Patterns"` is not equal to `"Migration Patterns  "`, so the lookup returns False.
4. **Divergence point:** step 3 has no else-branch, warning, or fuzzy fallback. The note is never appended and nothing is reported. This matches the Actual Result: the convention is silently dropped.

## Step 3 — Codebase Investigation

### Target repository

- Component `sdlc-workflow` and the paths in the bug both point to the `plugins/sdlc-workflow/...` tree. In the eval CLAUDE.md, the only entry in the Repository Registry is **acme-backend** (Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`), so the investigation targets that repository as described in `repo-context-mock.md`.
- **Code Intelligence:** the CLAUDE.md says "No Serena MCP servers are configured", so the skill falls back to Read/Grep/Glob. (In this eval, the file contents come from `repo-context-mock.md`.)

### Affected files and symbols

| File | Location / symbol | Role in the bug |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis: heading extraction `section_name = line[3:]` | **Defect site.** Keeps trailing whitespace in section names. |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment: `if convention_name in discovered_conventions:` | **Manifestation site.** The exact-match lookup fails silently, with no warning when a convention cannot be matched. |

### Impact analysis (referencing consumers)

- The `conventions` / `discovered_conventions` map feeds only plan-feature's task enrichment, which writes Implementation Notes into generated Jira Task descriptions.
- Every heading with trailing whitespace is affected, not only `Migration Patterns`. The same trailing-space issue would also apply to `\r` at the end of the line in CRLF files, because `split('\n')` leaves `\r` on each line. That is a closely related case of the same defect.

### Tests and fixtures

- `evals/plan-feature/files/conventions-mock.md` (as listed in the repo context) is the existing conventions fixture. Its headings have **no** trailing whitespace, so current evals do not cover this edge case. (In the real sdlc-plugins checkout, `evals/plan-feature/files/` has no `conventions-mock.md`. The repo-context mock is the source of truth for this eval.)
- Reproducer pattern: add a fixture variant whose heading has trailing whitespace (e.g., `## Migration Patterns  `), plus an eval case that asserts the generated Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns`.

### CONVENTIONS.md lookup

- The repository root has **no CONVENTIONS.md**, so there are no repo conventions to add to Implementation Notes.

### Reusable utilities

- None identified. The fix is a normalization (`.strip()` / `.rstrip()`) at the extraction point. Applying the same normalization to the lookup key keeps both sides consistent.

### Persistence-impact analysis

- Trace: `section_name` → `conventions` dict (in-memory) → `discovered_conventions` lookup → `notes` list → Implementation Notes text in a newly generated Jira task.
- **No persistence boundary found.** There is no database write (`insert`/`update`/ORM/SQL). Section names are recomputed from CONVENTIONS.md on every plan-feature run.
- **No data migration needed.** Jira tasks already generated without the convention are a one-off historical artifact and not system data. If needed, they can be re-planned manually. The fix task does not include a migration.

### Step 6 — Decomposition Guard check

There is a single root cause: unnormalized heading text in extraction. It shows up at extraction and at lookup in the same file. The missing warning on a non-match is part of the same fix scope (it makes the silent drop visible) and is not an independent defect. **Not a decomposition trigger.** A single Task is appropriate, so no user prompt is needed.
