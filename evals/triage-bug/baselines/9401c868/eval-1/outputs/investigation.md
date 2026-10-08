# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

The Steps to Reproduce reference a skill invocation (`/plan-feature ACME-100`), not a directly
runnable command. This is a skill/workflow bug that cannot be reproduced via CLI execution.
Code-path tracing is used instead.

### Code-path trace

**Entry point**: The `/plan-feature` skill invocation triggers the convention conformance
analysis, which reads `CONVENTIONS.md` and enriches generated task descriptions with
matching conventions.

**Trace through convention lookup** (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):

1. The skill reads the contents of `CONVENTIONS.md` and splits by newline.
2. For each line starting with `## `, it extracts the heading text using `line[3:]`.
3. The extracted section name is stored as a key in the `conventions` dictionary.

**Divergence point identified**: The extraction at `line[3:]` does NOT call `.strip()` or
`.rstrip()` on the result. When a heading line contains trailing whitespace (e.g.,
`## Migration Patterns  \n`), the extracted key becomes `"Migration Patterns  "` (with
two trailing spaces) instead of `"Migration Patterns"`.

**Trace through convention-aware task enrichment** (same file):

1. The task enrichment step performs an exact-match lookup: `if convention_name in discovered_conventions`.
2. The lookup key `convention_name` is the clean name `"Migration Patterns"` (without trailing spaces).
3. The dictionary key from extraction is `"Migration Patterns  "` (with trailing spaces).
4. The exact match fails silently -- no `else` branch, no warning logged.
5. The convention is omitted from the generated task's Implementation Notes.

**Reproduction outcome**: Confirmed via code-path trace. The bug is deterministic -- any
CONVENTIONS.md heading with trailing whitespace will be silently dropped.

## Step 3 -- Codebase Investigation

### Target repository

Based on the Component field (`sdlc-workflow`) and the code paths referenced in the bug
description, the target repository is **acme-backend** (from the Repository Registry).

- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Affected files and symbols

| File | Symbol/Location | Role |
|------|----------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention lookup logic (`line[3:]`) | Heading extraction -- missing `.strip()` |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`if convention_name in discovered_conventions`) | Exact-match comparison that fails with trailing whitespace |

### Root cause location

The defect is in the convention lookup logic within `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

This should be:

```python
section_name = line[3:].strip()  # Strip trailing whitespace from heading
```

### Test coverage gap

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT include
trailing whitespace on headings. This edge case is not covered by current evals, which is
why the bug was not caught during development.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` file at its root. No additional conventions
to apply to the fix task.

### Persistence-impact analysis

The buggy function processes CONVENTIONS.md headings and generates task descriptions that
are created as Jira issues. The output (task descriptions) is persisted to Jira at creation
time. However:

- This is not a database table within the application -- it is external Jira issue content.
- Previously created tasks with missing conventions are not retroactively correctable via
  a data migration within the application.
- The fix corrects future task generation behavior.

**Conclusion**: No persistence boundary within the application codebase. No data migration
is needed. Previously generated tasks with missing conventions are a Jira content issue
outside the scope of a code fix.

### Reuse candidates

- `evals/plan-feature/files/conventions-mock.md` -- existing convention fixture that can
  be extended or duplicated to create a trailing-whitespace variant for the reproducer test.
- Existing plan-feature eval infrastructure -- the reproducer test should follow the same
  eval pattern used by existing plan-feature tests.

### Investigation summary

- **Single root cause**: The heading extraction does not strip trailing whitespace.
- **Single file affected**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
- **No decomposition needed**: This is a single defect with a single fix location.
  The Decomposition Guard (Step 6) does not trigger.
