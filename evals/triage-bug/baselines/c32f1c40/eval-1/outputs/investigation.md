# Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Code-path tracing

The bug cannot be directly reproduced via CLI since it involves a skill invocation
(`/plan-feature`). A code-path trace was performed instead.

**Entry point**: `/plan-feature ACME-100` skill invocation.

**Trace path**:

1. The plan-feature skill reads `CONVENTIONS.md` from the target repository root.
2. It parses the file line-by-line, looking for lines starting with `## `.
3. For each heading line, it extracts the section name using `line[3:]` (everything after `## `).
4. The extracted section name is used as a dictionary key in `conventions[section_name]`.
5. Later, the task enrichment step looks up convention names with an exact match: `if convention_name in discovered_conventions`.

**Divergence point**: At step 3, `line[3:]` does NOT strip trailing whitespace. When the
heading line is `## Migration Patterns  \n`, the extracted key becomes `"Migration Patterns  "`
(with two trailing spaces). The subsequent exact-match lookup in step 5 compares
`"Migration Patterns"` against `"Migration Patterns  "`, which fails silently.

**Reproduction outcome**: Confirmed via code-path trace. The bug is deterministic --
any CONVENTIONS.md heading with trailing whitespace will be silently dropped.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend (from Repository Registry)
- **Component**: sdlc-workflow (from Bug issue)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Affected files and symbols

#### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Convention conformance analysis** -- heading extraction logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

The defect is at `line[3:]` -- this extracts the heading text but does not call `.strip()`
or `.rstrip()` to remove trailing whitespace. The fix is to use `line[3:].strip()`.

**Convention-aware task enrichment** -- exact-match lookup:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

This lookup uses exact string matching. When `convention_name` has trailing whitespace
from the extraction step, it fails to match the expected key without whitespace.

### Existing test coverage

- **File**: `evals/plan-feature/files/conventions-mock.md`
- **Coverage gap**: The existing eval fixture does NOT include trailing whitespace on
  headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to
reference in the generated task's Implementation Notes.

### Persistence-impact analysis

The convention conformance analysis produces output that is written directly into
Jira task descriptions (via `jira.create_issue`). However, this is task-generation-time
output, not data ingestion into a database table. The incorrect behavior (missing
convention in task description) is a **computed-at-generation-time** result, not a
persisted value that would require a data migration to correct.

**Conclusion**: No persistence boundary found. No data migration is needed. Fixing the
heading extraction logic will correct all future task generations. Previously generated
tasks with missing conventions would need to be regenerated (re-run `/plan-feature`),
but this is an operational step, not a data migration.
