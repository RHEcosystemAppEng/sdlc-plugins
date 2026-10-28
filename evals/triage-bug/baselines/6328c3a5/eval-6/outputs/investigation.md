# Step 3 -- Codebase Investigation: ACME-500

## Target Repository

Based on the **Component** field (`sdlc-workflow`) and the code paths referenced in the Steps to Reproduce (the `/plan-feature` skill), the target repository is:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| acme-backend | Rust backend service | serena_backend | /home/dev/repos/acme-backend |

**Code Intelligence note**: No Serena MCP servers are configured. Falling back to Read/Grep/Glob for codebase investigation.

## Affected Files and Symbols

### 1. Convention Conformance Analysis -- Heading Extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill reads `CONVENTIONS.md` headings using the following logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect**: The heading extraction at `line[3:]` does NOT strip trailing whitespace.
If the heading line is `## Migration Patterns  \n`, the extracted section name becomes
`"Migration Patterns  "` (with two trailing spaces), which fails exact-match comparison
against the expected `"Migration Patterns"`.

### 2. Convention-Aware Task Enrichment -- Exact Match Lookup

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

**Defect**: This lookup uses exact string matching via `in` (dictionary key lookup).
When `convention_name` is `"Migration Patterns"` but the dictionary key is
`"Migration Patterns  "` (with trailing spaces), the lookup evaluates to `False`
and the convention is silently skipped -- no warning or error is logged.

## Test Coverage Analysis

### Existing test fixture

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does **NOT** include trailing
whitespace on headings. This edge case is not covered by current evals, which is why
the bug was not caught during development.

## CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No repository-level
conventions to incorporate into the generated task's Implementation Notes.

## Persistence-Impact Analysis

**Result**: No persistence boundary found.

The convention lookup and task enrichment logic operate at **generation time** -- they
compute the task description content each time the `/plan-feature` skill runs. The output
(task description text) is sent to the Jira API for task creation but is not persisted
locally in the repository.

Trace path:
- `conventions_content.split('\n')` (reads CONVENTIONS.md)
- `conventions[section_name] = current_section_content` (in-memory dictionary)
- `notes.append(...)` (in-memory list)
- Task description assembled and sent to Jira API

Since the output is computed at generation time and not written to a local database,
**no data migration is needed**. Fixing the heading extraction logic will correct all
future task generation runs.

## Decomposition Guard Assessment (Step 6)

This bug has a **single root cause**: the heading extraction at `line[3:]` does not
strip trailing whitespace. The match failure in the task enrichment step is a direct
consequence of this single defect, not an independent issue.

**Conclusion**: A single Task is appropriate. No decomposition needed.
