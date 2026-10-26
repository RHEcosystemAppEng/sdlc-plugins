# Step 3 -- Codebase Investigation: ACME-511

## Target repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

Determined from Repository Registry in CLAUDE.md, matching Component `sdlc-workflow`.

## Code Intelligence

No Serena MCP servers are configured. Falling back to Read/Grep/Glob.

## Investigation findings

### Affected code path: convention heading extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill extracts convention headings using the following logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect**: The heading extraction at `line[3:]` does NOT strip trailing whitespace.
If the heading line is `## Migration Patterns  \n`, the extracted section name becomes
`"Migration Patterns  "` (with trailing spaces), which fails exact-match comparison
against the expected `"Migration Patterns"`.

### Affected code path: convention-aware task enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md SS{convention_name}: {action}")
```

This match fails when `convention_name` has trailing whitespace from the extraction step.

### Test coverage gap

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing
whitespace on headings, so this edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root.

## Persistence-impact analysis

The buggy function's output (convention section names) is used for in-memory matching
during task enrichment. The extracted section names are not persisted to a database --
they are computed at processing time and discarded after the skill execution completes.

**Result**: No persistence boundary found. No data migration is needed.

## Summary of affected files and symbols

| File | Symbol/Section | Issue |
|------|---------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Heading extraction (`line[3:]`) | Missing `.strip()` on extracted heading text |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment | Exact-match fails due to trailing whitespace |
| `evals/plan-feature/files/conventions-mock.md` | Test fixture | No trailing whitespace edge case coverage |
