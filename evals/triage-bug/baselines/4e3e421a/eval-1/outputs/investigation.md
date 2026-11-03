# Steps 2–3 – Reproduce/Trace and Codebase Investigation

## Step 2 – Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce require invoking the `/plan-feature ACME-100` skill against a live Jira
Feature. This is a skill/documentation-level bug, not a CLI or API command that can run in a
read-only way. It cannot be reproduced directly here, because no Jira access is allowed and it is
an LLM-driven skill. **Reproduction outcome: not directly reproducible, so code-path tracing was used instead.**

### Code-path trace

1. **Entry point:** `/plan-feature ACME-100` loads `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
2. **CONVENTIONS.md lookup:** during repository analysis, plan-feature reads the target repo's
   `CONVENTIONS.md` and runs its *convention conformance analysis*. The heading-extraction logic is:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
   For the input line `## Migration Patterns  `, `line[3:]` gives `"Migration Patterns  "`
   (two trailing spaces). The key is stored with the whitespace still attached.
3. **Convention-aware task enrichment:** later, plan-feature matches conventions by exact name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   The lookup key `"Migration Patterns"` is not equal to the stored key `"Migration Patterns  "`.
   The membership test returns `False`, so the note is never appended.
4. **Divergence point:** the expected behavior (the convention appears in Implementation Notes)
   diverges from the actual behavior (it is silently omitted) at the heading extraction in step 2.
   The un-normalized key then makes the exact-match lookup in step 3 fail. The `if` has no `else`
   branch and no warning, so the failure is silent.

## Step 3 – Codebase Investigation

### Target repository

- Component `sdlc-workflow` and the code path `plugins/sdlc-workflow/skills/plan-feature/` identify
  the target repository as **acme-backend**. It is the only Registry entry, at Path
  `/home/dev/repos/acme-backend`, with Serena instance `serena_backend`.
- Code Intelligence says no Serena MCP servers are configured. Following the skill's fallback, the
  investigation used Read/Grep/Glob, simulated here from `repo-context-mock.md`.

### Affected files and symbols

| File | Section / Symbol | Role in bug |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis (heading extraction, `section_name = line[3:]`) | **Defect site**: the extracted heading is not stripped of trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`if convention_name in discovered_conventions`) | **Manifestation site**: the exact-match lookup fails with no warning |

### Impact analysis (callers/consumers)

- The `conventions` / `discovered_conventions` map is used only by plan-feature's task enrichment,
  which writes the "Per CONVENTIONS.md §..." lines into generated task Implementation Notes.
- Downstream, `implement-task` uses those Implementation Notes. A dropped convention means
  implement-task never sees it, so generated code may break repo conventions (for example, missing
  `Index::create()` for FK columns).
- Any heading with trailing whitespace is affected, not just `Migration Patterns`. Trailing tabs
  and Windows `\r` line endings (`## Heading\r` after `split('\n')`) cause the same failure, since
  `line[3:]` keeps them.

### Existing tests / patterns for the reproducer

- `evals/plan-feature/files/conventions-mock.md` is the existing plan-feature conventions eval
  fixture. Its headings have **no** trailing whitespace, so current evals do not cover this edge case.
- Reproducer pattern: add a plan-feature eval fixture, or a variant of the existing one, whose
  `## Migration Patterns  ` heading has trailing whitespace. Pair it with a feature that needs an
  FK migration. Assert that the generated task's Implementation Notes contain
  `Per CONVENTIONS.md §Migration Patterns`.

### Reusable utilities / patterns

- The fix needs no new helper. Normalizing the extracted heading with the standard
  `strip()` / `rstrip()`, on both the stored key and the lookup key, follows the existing
  extraction logic.
- The existing plan-feature eval layout under `evals/plan-feature/files/` is the pattern for the
  new fixture.

### CONVENTIONS.md lookup

- No `CONVENTIONS.md` exists at the acme-backend repository root, so there are no repo conventions
  to apply to the fix task.

### Persistence-impact analysis

- Tracing the buggy output: `section_name` goes into the `conventions` map, then
  `discovered_conventions` lookup, then `notes.append(...)`, then the generated Jira task
  description text.
- None of these hops write to a database (no `insert`/`update`/`save`/ORM/SQL). The value is
  computed fresh on each `/plan-feature` invocation.
- **No persistence boundary found. No data migration is needed.** Note: Jira tasks already
  generated by affected plan-feature runs will lack the dropped convention. That is not database
  state. If needed, re-run plan-feature or edit those tasks by hand, outside this fix's scope.

### Decomposition Guard (Step 6) check

- There is a single root cause: the extracted heading is not normalized. It shows up at two points
  in one file (extraction and lookup). This is **not** a decomposition trigger, so one Task is appropriate.
- The missing warning on a failed match is a direct part of the same defect, which makes the
  failure silent. It is in scope as a hardening criterion in the same Task, not a separate root cause.
