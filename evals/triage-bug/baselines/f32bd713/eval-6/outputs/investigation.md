# Step 3 -- Codebase Investigation: ACME-500

## Target Repository

| Field | Value |
|-------|-------|
| Repository | acme-backend |
| Role | Rust backend service |
| Serena Instance | serena_backend |
| Path | /home/dev/repos/acme-backend |

The target repository was identified from the **Component** field (`sdlc-workflow`) and the code paths referenced in the Steps to Reproduce (the `plan-feature` skill's convention lookup).

## Code Intelligence

No Serena MCP servers are configured per the project's Code Intelligence section. Investigation uses Read/Grep/Glob fallback.

## Affected Files and Symbols

### 1. Convention Heading Extraction -- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill reads `CONVENTIONS.md` headings using the following logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect**: The heading extraction at `line[3:]` does NOT strip trailing whitespace. When the heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces). This key is stored in the `conventions` dictionary with trailing whitespace included.

### 2. Convention-Aware Task Enrichment -- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by exact section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

**Defect**: The lookup uses exact string match (`convention_name in discovered_conventions`). Since the dictionary key is `"Migration Patterns  "` (with trailing whitespace) but the lookup key is `"Migration Patterns"` (clean), the match fails silently. No warning or error is produced -- the convention is simply omitted from the generated task.

### 3. Existing Test Coverage -- `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is completely uncovered by current evals.

## CONVENTIONS.md Lookup

The repository (`acme-backend`) does not have a `CONVENTIONS.md` at its root. No repository-level conventions apply to the fix task.

## Persistence-Impact Analysis

The buggy function's output (the `conventions` dictionary with section names as keys) is used to generate task descriptions that are posted to Jira via the API. The incorrect behavior results in missing convention references in task descriptions.

**Persistence boundary analysis:**

1. **Trace output to persistence boundary**: The `conventions` dictionary is read during task generation. The generated task description (with the missing convention reference) is written to Jira via `jira.create_issue()`.
2. **Assessment**: The incorrect output IS persisted to Jira (task descriptions with missing convention references). However, this is a **content generation bug**, not a data corruption bug. Each task is generated fresh when `/plan-feature` is invoked. Existing tasks with missing conventions are a consequence of the bug but do not need a data migration -- they represent historical outputs at the time of generation.
3. **Conclusion**: No data migration is needed. Fixing the heading extraction logic corrects all future task generations. Previously generated tasks with missing conventions are historical artifacts that were correct given the code behavior at the time.

## Summary of Findings

| Finding | File | Symbol/Location | Impact |
|---------|------|-----------------|--------|
| Missing `.strip()` on heading extraction | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading parser (`line[3:]`) | Trailing whitespace in headings produces mismatched dictionary keys |
| Silent failure on convention lookup | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Task enrichment (`convention_name in discovered_conventions`) | Missing conventions silently omitted, no warning logged |
| No test coverage for trailing whitespace | `evals/plan-feature/files/conventions-mock.md` | Eval fixture | Edge case uncovered |
