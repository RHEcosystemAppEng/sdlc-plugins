# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

The Steps to Reproduce reference a skill invocation (`/plan-feature ACME-100`), not a
runnable command. This is a skill/logic bug, so code-path tracing is the appropriate
approach rather than direct reproduction.

### Code-path trace

**Entry point**: The `/plan-feature` skill invocation triggers the plan-feature SKILL.md
logic, which includes a convention conformance analysis step that reads `CONVENTIONS.md`.

**Trace through convention parsing**:

1. The plan-feature skill reads `CONVENTIONS.md` and splits its content by newline.
2. For each line, it checks if the line starts with `## ` to identify section headings.
3. The heading text is extracted using `line[3:]`, which takes everything after the
   `## ` prefix -- including any trailing whitespace.
4. The extracted section name is stored as a dictionary key in `conventions[section_name]`.

**Trace through convention matching**:

1. During task enrichment, the skill looks up convention names using exact-match
   comparison: `if convention_name in discovered_conventions`.
2. When the heading was `## Migration Patterns  \n`, the stored key is
   `"Migration Patterns  "` (with trailing spaces).
3. The lookup uses the clean name `"Migration Patterns"` (without trailing spaces).
4. The exact match fails: `"Migration Patterns" != "Migration Patterns  "`.
5. No match is found, so the convention is silently skipped.

**Divergence point**: The behavior diverges from expected at the heading extraction
step (`line[3:]`), where trailing whitespace is preserved. The downstream exact-match
comparison then fails because the stored key includes trailing whitespace that the
lookup key does not.

**Silent failure**: No warning or error is emitted when a convention is skipped due
to a failed match. This is a secondary issue -- even if the primary parsing bug is
fixed, a warning for unmatched conventions would improve debuggability.

## Step 3 -- Codebase Investigation

### Target repository

The bug affects the **sdlc-workflow** component. From the Repository Registry:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| acme-backend | Rust backend service | serena_backend | /home/dev/repos/acme-backend |

The relevant code is in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.

### Code Intelligence

No Serena MCP servers are configured per the Code Intelligence section. Investigation
uses Read/Grep/Glob fallback.

### Affected files and symbols

#### 1. Convention heading extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Location**: Convention conformance analysis section

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

The defect is at `line[3:]` -- this extracts the heading text without calling `.strip()`
to remove trailing whitespace. When a CONVENTIONS.md heading has trailing spaces
(e.g., `## Migration Patterns  `), the extracted section name retains those spaces.

#### 2. Convention-aware task enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Location**: Convention-aware task enrichment section

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This exact-match lookup fails when the key in `discovered_conventions` has trailing
whitespace but `convention_name` does not.

### Existing test coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing
whitespace on headings. This edge case is not covered by current evals, which
explains why the bug was not caught during development.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` file at its root. No additional
conventions apply to the fix task.

### Persistence-impact analysis

The buggy function's output (the `conventions` dictionary with section names as keys)
is used to generate Jira task descriptions. The output flows to the Jira API
(`jira.create_issue`) but is not persisted to any local database.

However, **Jira tasks already created** while this bug was present may have missing
convention references in their Implementation Notes. This is a Jira data quality
concern rather than a database persistence issue. No data migration is needed -- the
fix will correct future task generation. Previously generated tasks with missing
conventions would need manual review, but this is outside the scope of the code fix.

**Conclusion**: No persistence boundary found in the local codebase. No data migration
required.
