# Step 2 & 3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction Method: Code-Path Tracing

The Steps to Reproduce describe a skill invocation (`/plan-feature ACME-100`), not directly runnable commands. The bug involves the plan-feature skill's internal convention parsing logic. Code-path tracing is the appropriate method.

### Trace Findings

**Entry point:** `/plan-feature ACME-100` skill invocation triggers convention conformance analysis.

**Trace path:**

1. The plan-feature skill reads `CONVENTIONS.md` and splits content by newline.
2. For each line starting with `## `, it extracts the heading text using `line[3:]`.
3. The extracted heading is used as a dictionary key in `conventions[section_name]`.
4. Later, during task enrichment, convention names are matched via exact comparison: `if convention_name in discovered_conventions`.

**Divergence point:** Step 2 above. When the heading line is `## Migration Patterns  \n` (with trailing whitespace), `line[3:]` produces `"Migration Patterns  "` (with trailing spaces). The exact match in Step 4 against the expected `"Migration Patterns"` (without trailing spaces) fails, causing the convention to be silently dropped with no warning.

## Step 3 -- Codebase Investigation

### Target Repository

- **Component:** sdlc-workflow
- **Repository:** acme-backend (from Repository Registry)
- **Serena Instance:** serena_backend
- **Path:** /home/dev/repos/acme-backend

### Code Intelligence Note

Per CLAUDE.md Code Intelligence section: "No Serena MCP servers are configured. Code intelligence is not available." Fallback to Read/Grep/Glob.

### Affected Files and Symbols

#### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Convention heading extraction (bug location):**

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does NOT strip trailing whitespace
        conventions[section_name] = current_section_content
```

The heading extraction at `line[3:]` does NOT call `.strip()` on the result. If the heading line has trailing whitespace (e.g., `## Migration Patterns  `), the extracted section name becomes `"Migration Patterns  "` (with trailing spaces).

**Convention-aware task enrichment (failure point):**

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This exact match fails when `convention_name` is `"Migration Patterns"` but the dictionary key is `"Migration Patterns  "` (with trailing whitespace).

### Existing Test Coverage

**File:** `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No repository-level conventions to include in the generated task's Implementation Notes.

### Persistence-Impact Analysis

**Trace from buggy function output to persistence boundary:**

The buggy function (convention heading extraction) produces an in-memory dictionary of conventions that is consumed during task description generation. The generated task description is then posted to Jira via the API (`jira.create_issue`).

1. `conventions[section_name]` (in-memory dict) -> used by task enrichment logic -> generates Implementation Notes text -> passed to `jira.create_issue()` as part of the task description.

2. The Jira issue creation is a write operation, but the affected data is the **task description text** in Jira, not application data in a database table. The task description is regenerated each time the skill runs -- it is not ingested once and then read repeatedly.

**Conclusion:** No persistence boundary in the application database. The output is a Jira task description generated at invocation time. If the bug is fixed, re-running the skill produces correct output. No data migration is needed.

### Summary of Findings

| Finding                         | Detail                                                                  |
|---------------------------------|-------------------------------------------------------------------------|
| Bug location                    | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- heading extraction |
| Root function                   | Convention heading parser: `line[3:]` without `.strip()`                |
| Failure mode                    | Silent -- no warning or error logged when convention match fails        |
| Impact                          | Conventions with trailing whitespace on headings are silently dropped   |
| Existing test coverage          | None -- eval fixtures do not include trailing whitespace on headings    |
| Persistence impact              | None -- output is a Jira task description, not persisted app data       |
| CONVENTIONS.md                  | Not present at repository root                                         |
