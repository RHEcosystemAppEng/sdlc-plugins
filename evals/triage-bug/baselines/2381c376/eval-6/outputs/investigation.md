# Step 3 -- Codebase Investigation: ACME-500

## Target Repository

- **Repository**: acme-backend
- **Component**: sdlc-workflow (from bug metadata)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Investigation Findings

### Affected Code Path 1: Convention Heading Extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention conformance analysis

The plan-feature skill reads `CONVENTIONS.md` headings using a line-by-line parser:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect**: The heading extraction at `line[3:]` does NOT strip trailing whitespace.
When the heading line is `## Migration Patterns  \n`, the extracted section name becomes
`"Migration Patterns  "` (with two trailing spaces). This key is stored in the `conventions`
dictionary with trailing whitespace included.

### Affected Code Path 2: Convention-Aware Task Enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention-aware task enrichment

The task enrichment step matches conventions by exact section name comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Defect**: The lookup uses `convention_name` (which is the clean, expected name like
`"Migration Patterns"`) to check against `discovered_conventions` (which contains the
whitespace-polluted key `"Migration Patterns  "`). The exact-match `in` check fails
because `"Migration Patterns" != "Migration Patterns  "`.

No error or warning is raised on match failure -- the convention is silently dropped.

### Existing Test Coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace
on headings. This means the whitespace edge case is not covered by current evals and would
not have been caught by existing tests.

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No repository-level conventions
apply to this fix task.

### Persistence-Impact Analysis

The bug affects the plan-feature skill's task generation output (Implementation Notes in
Jira task descriptions). Tracing the output:

1. `section_name` (with trailing whitespace) is stored in an in-memory `conventions` dictionary
2. The dictionary is used during task description generation
3. The generated description is posted to Jira via `jira.create_issue`

**Assessment**: The output is a Jira task description, not persisted to a database table.
Jira tasks that were already created with missing convention references are the "stale data,"
but they exist as Jira issues (not database rows in the application). No data migration is
needed within the application codebase. Previously generated tasks with missing conventions
would need manual review but this is outside the scope of a code fix.

**Conclusion**: No persistence boundary found in the application codebase. No data migration required.

### Symbols and Patterns Summary

| Symbol / Pattern | File | Role |
|---|---|---|
| Convention heading parser (`line[3:]`) | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Extracts section names without stripping whitespace |
| Convention lookup (`convention_name in discovered_conventions`) | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Exact-match fails when keys have trailing whitespace |
| Eval fixture (conventions-mock.md) | `evals/plan-feature/files/conventions-mock.md` | Missing trailing-whitespace test case |
