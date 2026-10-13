# Step 3 -- Codebase Investigation: ACME-500

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend (not available -- Code Intelligence section notes no Serena MCP servers configured)
- **Path**: /home/dev/repos/acme-backend
- **Fallback**: Using Read/Grep/Glob tools directly (no Serena available)

## CONVENTIONS.md Lookup

The repository does **not** have a CONVENTIONS.md at its root. No conventions to apply to the generated task's Implementation Notes.

## Affected Code Paths

### 1. Convention Heading Extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention conformance analysis

The plan-feature skill reads CONVENTIONS.md headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect**: The heading extraction at `line[3:]` does NOT call `.strip()` or `.rstrip()` on the extracted text. When a heading line contains trailing whitespace (e.g., `## Migration Patterns  \n`), the extracted section name becomes `"Migration Patterns  "` (with trailing spaces). This preserves the trailing whitespace as part of the dictionary key.

### 2. Convention-Aware Task Enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention-aware task enrichment

The task enrichment step performs an exact-match lookup:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Defect**: The lookup key `convention_name` is the clean name (e.g., `"Migration Patterns"`), but the dictionary was populated with the whitespace-polluted key (`"Migration Patterns  "`). The `in` operator performs exact string comparison, so `"Migration Patterns" != "Migration Patterns  "` and the lookup silently fails. No warning or error is raised -- the convention is simply not included in the generated task.

### 3. Existing Test Coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is completely uncovered by current tests/evals.

## Persistence-Impact Analysis

The buggy functions (`line[3:]` heading extraction and `convention_name in discovered_conventions` lookup) produce in-memory data structures used during task generation. Their output is sent to Jira as part of a task description (via `jira.create_issue`).

**Persistence boundary**: The generated task description is persisted in Jira (external system), but the incorrect behavior is that a convention reference is **omitted** from the output -- meaning no incorrect data is written. The issue is missing content, not corrupted content. If the heading extraction is fixed, future task generations will include the convention. Past tasks created with the bug remain as-is in Jira, but these are task descriptions (guidance documents), not authoritative data records.

**Conclusion**: No data migration is needed. The bug produces missing output rather than incorrect persisted values. Past generated tasks that should have included convention references were simply missing those references -- the tasks themselves are not corrupted data requiring correction.

## Summary of Findings

| Finding | Detail |
|---------|--------|
| Root file | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` |
| Defective operation | `line[3:]` -- heading extraction without `.strip()` |
| Failure mode | Trailing whitespace on CONVENTIONS.md headings causes silent lookup miss |
| Impact | Convention-based guidance silently omitted from generated tasks |
| Existing test coverage | None for trailing whitespace edge case |
| Persistence impact | None -- missing output, not corrupted data |
