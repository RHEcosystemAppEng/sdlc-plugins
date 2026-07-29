# Step 3 -- Codebase Investigation: ACME-511

## Target Repository

| Field | Value |
|---|---|
| Repository | acme-backend |
| Role | Rust backend service |
| Serena Instance | serena_backend |
| Path | /home/dev/repos/acme-backend |

The Component field on ACME-511 is "sdlc-workflow", and the Repository Registry
maps acme-backend as the primary repository. Investigation proceeds against this
repository.

## Code Intelligence

No Serena MCP servers are configured per the project's CLAUDE.md Code Intelligence
section. Falling back to Read/Grep/Glob tools for investigation.

## Investigation Findings

### Convention heading extraction (plan-feature skill)

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill reads `CONVENTIONS.md` headings using the following logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect**: The heading extraction at `line[3:]` does NOT strip trailing whitespace.
If the heading line is `## Migration Patterns  \n`, the extracted section name
becomes `"Migration Patterns  "` (with trailing spaces), which fails exact-match
comparison against the expected `"Migration Patterns"`.

### Convention-aware task enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

This match fails when `convention_name` has trailing whitespace from the extraction
step. The enrichment silently skips conventions that should be applied.

### Existing test coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing
whitespace on headings, so this edge case is not covered by current evals.

### CONVENTIONS.md

The repository does not have a CONVENTIONS.md at its root. No repository-level
conventions to reference in the fix task.

## Persistence-Impact Analysis

The buggy function's output (the extracted `section_name` string) is used for
in-memory dictionary lookups during task enrichment. It is not persisted to a
database -- the convention matching is computed at task-generation time from
the source `CONVENTIONS.md` file.

**Result**: No persistence boundary found. No data migration is needed. Fixing
the heading extraction logic will correct all future convention lookups.

## Summary of Affected Files

| File | Symbol / Location | Issue |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Missing `.strip()` on extracted heading text |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Exact-match fails against whitespace-padded keys |
| `evals/plan-feature/files/conventions-mock.md` | Test fixture | Missing trailing-whitespace edge case |
