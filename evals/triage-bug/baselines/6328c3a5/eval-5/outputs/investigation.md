# Step 3 -- Codebase Investigation

## Target Repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Investigation Method

No Serena MCP servers are available (per Code Intelligence section: "No Serena MCP
servers are configured. Code intelligence is not available."). Falling back to
Read/Grep/Glob for codebase investigation.

## Findings

### Affected Code Path

The bug involves user preference persistence -- specifically the dark mode toggle
in Settings > Appearance. Investigation of the sdlc-workflow component reveals the
following relevant code paths:

#### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Convention heading extraction** (convention conformance analysis):

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Issue identified**: The heading extraction at `line[3:]` does NOT strip trailing
whitespace. If the heading line is `## Migration Patterns  \n`, the extracted
section name becomes `"Migration Patterns  "` (with trailing spaces), which fails
exact-match comparison against the expected `"Migration Patterns"`.

#### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Convention-aware task enrichment**:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This match fails when `convention_name` has trailing whitespace from the extraction
step. The preference lookup mechanism uses exact string matching that does not
account for whitespace normalization.

### Existing Test Coverage

**Test file**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing
whitespace on headings, so this edge case is not covered by current evals.

### CONVENTIONS.md

The repository does not have a `CONVENTIONS.md` at its root. No conventions to
inform the task's Implementation Notes.

## Persistence-Impact Analysis

The buggy function's output (the extracted section name with trailing whitespace)
is used in an in-memory dictionary lookup (`discovered_conventions`). Tracing the
call chain:

1. `conventions_content.split('\n')` -- reads file content (input)
2. `conventions[section_name] = current_section_content` -- stores in memory dict
3. `convention_name in discovered_conventions` -- lookup against the dict

**No persistence boundary found.** The convention names are computed at query time
(during skill execution) and are not written to a database. The incorrect values
exist only in the in-memory dictionary during a single execution run. No data
migration is needed -- fixing the code alone corrects the behavior for all future
executions.

## Summary of Affected Files and Symbols

| File | Symbol/Location | Issue |
|------|----------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Missing `.strip()` on extracted heading name |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment | Exact-match fails due to trailing whitespace |
| `evals/plan-feature/files/conventions-mock.md` | Test fixture | Missing trailing whitespace edge case coverage |
