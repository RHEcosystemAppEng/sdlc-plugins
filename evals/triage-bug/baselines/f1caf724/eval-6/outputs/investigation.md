# Step 3 -- Codebase Investigation: ACME-500

## Target Repository

Based on the Component field (`sdlc-workflow`) and the code paths referenced in the bug description (`/plan-feature` skill), the target repository is:

- **Repository**: acme-backend (from Repository Registry)
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

However, the Code Intelligence section notes: "No Serena MCP servers are configured. Code intelligence is not available." Falling back to Read/Grep/Glob for investigation.

## Affected Files and Symbols

### Primary defect: Convention heading extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention conformance analysis

The heading extraction logic does not strip trailing whitespace:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

When the heading line is `## Migration Patterns  \n`, `line[3:]` produces `"Migration Patterns  "` (with trailing spaces). This raw string is stored as the dictionary key.

### Secondary impact: Convention-aware task enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention-aware task enrichment

The task enrichment step matches conventions by exact section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The match fails because `convention_name` (e.g., `"Migration Patterns"`) does not equal the key stored with trailing whitespace (`"Migration Patterns  "`).

## Existing Test Coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals, which explains why the bug was not caught during development.

## CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No additional conventions to apply to the fix task.

## Persistence-Impact Analysis

The buggy function's output (the `conventions` dictionary with section names as keys) is used to generate task descriptions that are posted to Jira via the API. The incorrect behavior causes missing content in generated task descriptions.

- **Persistence boundary**: The output is written to Jira issue descriptions via `jira.create_issue`. Once created, the task description is persisted in Jira.
- **Impact**: Previously generated tasks from plan-feature runs against repositories with trailing-whitespace CONVENTIONS.md headings may have incomplete Implementation Notes (missing convention references). However, this is content omission rather than data corruption -- the tasks are simply missing information rather than containing incorrect values.
- **Data migration needed**: No. The fix corrects future behavior. Existing tasks with missing convention references would need manual review, but no automated data migration is feasible since the omitted content was never stored.

## Summary of Findings

| Finding | Detail |
|---------|--------|
| Root file | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` |
| Root symbol | Convention heading extraction logic (`line[3:]`) |
| Impact file | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (task enrichment) |
| Impact | Exact-match lookup fails due to trailing whitespace in key |
| Failure mode | Silent -- no warning or error logged |
| Test gap | `evals/plan-feature/files/conventions-mock.md` lacks trailing whitespace test case |
