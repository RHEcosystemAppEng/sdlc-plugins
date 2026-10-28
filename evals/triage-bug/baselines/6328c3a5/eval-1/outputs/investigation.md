# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction Method: Code-path tracing

This bug involves a skill's text parsing logic and cannot be directly reproduced via
CLI commands. The Steps to Reproduce describe a `/plan-feature` invocation, which is
an internal skill workflow. Code-path tracing was used instead.

### Trace Findings

**Entry point**: `/plan-feature ACME-100` invocation triggers the plan-feature skill.

**Execution path**:

1. The plan-feature skill reads `CONVENTIONS.md` and parses section headings.
2. The heading extraction logic splits content by newlines and checks for lines
   starting with `## `:

   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```

3. When the heading line is `## Migration Patterns  \n` (with trailing whitespace),
   `line[3:]` extracts `"Migration Patterns  "` (with trailing spaces).

4. The convention-aware task enrichment step performs an exact match:

   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
   ```

5. The lookup key `"Migration Patterns"` does not match the stored key
   `"Migration Patterns  "` -- the convention is silently skipped with no
   warning or error logged.

**Divergence point**: The behavior diverges at the heading extraction step
(`line[3:]`), which does not strip trailing whitespace. The downstream exact-match
comparison then fails silently.

## Step 3 -- Codebase Investigation

### Target Repository

- **Repository**: acme-backend (based on Component: sdlc-workflow)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

**Note**: Code Intelligence section states "No Serena MCP servers are configured."
Fallback to Read/Grep/Glob was used.

### Affected Files and Symbols

| File | Symbol/Location | Role |
|------|----------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | **Defect location** -- extracts heading without stripping whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | **Failure point** -- exact match fails due to trailing whitespace in key |

### Root Cause Code

**Defective code** (heading extraction):
```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

**Correct code** should be:
```python
section_name = line[3:].strip()  # Strip trailing whitespace from heading
```

### Existing Test Coverage

- **Existing test fixture**: `evals/plan-feature/files/conventions-mock.md`
- **Coverage gap**: The existing fixture does NOT include trailing whitespace on
  headings, so this edge case is not covered by current evals.

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to
reference in the generated task's Implementation Notes.

### Persistence-Impact Analysis

The buggy function's output (extracted convention section names) is used to generate
task description text, which is then written to Jira via API. However:

- The convention names are **computed at generation time** from source data
  (`CONVENTIONS.md` file content) each time `/plan-feature` is invoked.
- No values are persisted to a local database -- the output is sent to Jira as
  task description text.
- Previously generated tasks that were missing conventions are already in Jira,
  but these are Jira issue descriptions, not database records under the
  application's control.

**Conclusion**: No persistence boundary found within the application. No data
migration is needed. Previously generated tasks with missing conventions are a
Jira content issue outside the scope of a code fix.

### Reusable Patterns

- The existing eval fixture at `evals/plan-feature/files/conventions-mock.md`
  provides the pattern for creating convention test fixtures. A new fixture (or
  modification of the existing one) should include trailing whitespace on headings
  to test this edge case.
