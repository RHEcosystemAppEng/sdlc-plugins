# Codebase Investigation -- Step 3

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend
- **Component match**: sdlc-workflow (from Bug's Component field)

## Code Intelligence

No Serena MCP servers are configured. Falling back to Read/Grep/Glob for investigation.

## Convention Heading Extraction

### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill reads `CONVENTIONS.md` headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Finding**: The heading extraction at `line[3:]` does NOT strip trailing whitespace. If the heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces). This is the root of the bug.

## Convention-Aware Task Enrichment

### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by section name using exact string comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Finding**: The match fails because `convention_name` (e.g., `"Migration Patterns"`) does not equal the key stored in `discovered_conventions` (e.g., `"Migration Patterns  "` with trailing spaces). The `in` operator performs exact key matching, so the trailing whitespace causes a silent mismatch.

## Existing Test Coverage

### File: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This means the edge case is not covered by current evals.

## CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to carry forward into the task's Implementation Notes from the repository itself.

## Persistence-Impact Analysis

The bug affects the plan-feature skill's convention heading extraction and task enrichment logic. These are text-processing functions that operate at task-generation time. The output (task descriptions with Implementation Notes) is written to Jira via the API, but this is the expected output medium, not a database persistence concern.

- The buggy function's output is a Jira task description, written once at plan-feature execution time.
- Previously generated tasks that were missing convention references due to this bug already exist in Jira. However, these are Jira issues (not database rows in the application), and correcting them would require re-running plan-feature, not a data migration.
- **No persistence boundary found in application code.** No data migration is needed.

## Summary of Affected Code

| File | Symbol/Location | Issue |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Does not strip trailing whitespace from heading text |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Exact match fails against keys with trailing whitespace |
| `evals/plan-feature/files/conventions-mock.md` | Test fixture | Does not include trailing whitespace edge case |
