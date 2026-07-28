# Steps 2–3 – Investigation: ACME-500

## Step 2 – Reproduce / Trace

### Reproduction approach

The bug describes a skill/documentation defect (not a runnable CLI command), so direct
reproduction is not feasible. Code-path tracing is used instead.

### Entry point

The entry point is the `/plan-feature` skill invocation (Step 5, Convention-aware task
enrichment section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`).

### Trace: CONVENTIONS.md heading extraction

**Location**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention lookup section.

The skill reads `CONVENTIONS.md` and parses headings using the following logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

When `CONVENTIONS.md` contains a heading line with trailing whitespace — e.g.,
`## Migration Patterns  \n` — the extraction `line[3:]` produces `"Migration Patterns  "`
(with trailing spaces). The trailing newline is stripped by the split, but the inline
trailing spaces are NOT stripped.

### Trace: Convention-aware task enrichment

**Location**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention-aware task
enrichment section.

The task enrichment step performs an exact-match lookup:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

Here `convention_name` is expected to be `"Migration Patterns"` (no trailing spaces).
However `discovered_conventions` holds the key `"Migration Patterns  "` (with trailing
spaces). The lookup `"Migration Patterns" in discovered_conventions` returns `False` —
the convention is silently omitted from Implementation Notes.

No warning or error is emitted by the skill. The result is a task description that is
missing the convention reference entirely.

### Trace outcome

- **Divergence point**: heading extraction at `line[3:]` — does not call `.strip()` on
  the extracted text.
- **Effect**: downstream exact-match comparison fails silently.
- **Reproduction**: confirmed by trace — the behavior described in the bug is
  reproducible given a `CONVENTIONS.md` file with trailing whitespace on any heading line.

---

## Step 3 – Codebase Investigation

### Target repository identification

- **Component**: sdlc-workflow → target repository is the sdlc-plugins repo.
- **Repository Registry**: CLAUDE.md lists `acme-backend` (Serena Instance: serena_backend,
  Path: /home/dev/repos/acme-backend). No Serena MCP server is configured (Code Intelligence
  section: "No Serena MCP servers are configured"). Falling back to Read/Grep/Glob.

### Affected files and symbols

**Primary defect location**:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
  - Convention lookup section: heading extraction `line[3:]` — does NOT strip trailing whitespace
  - Convention-aware task enrichment section: exact-match comparison `if convention_name in discovered_conventions`

Both sections are in the same SKILL.md file; the defect originates in the extraction step
and propagates to the comparison step.

### Existing test coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace
on any heading lines. The trailing-whitespace edge case is undetected by current evals.
A new fixture or an augmented fixture is needed to cover this edge case.

### CONVENTIONS.md at repository root

No `CONVENTIONS.md` is present at the repository root of the target repository. No
convention enrichment applies to the fix task itself.

### Persistence-impact analysis

The buggy extraction happens at plan-feature skill execution time (convention lookup during
planning). The output (Implementation Notes text) is written to a Jira task description —
a one-time creation action, not an ongoing database ingestion. Incorrect task descriptions
created before the fix are not automatically corrected by deploying the fix. However:

- The output is created at task-generation time per invocation, not stored to a persistent
  database that is re-queried separately from source data.
- Each `/plan-feature` invocation is independent; fixing the skill ensures all future
  invocations produce correct output.
- No SQL/ORM persistence boundary is present (no INSERT/UPDATE to a data table).

**Conclusion**: No data migration is needed. The fix corrects all future plan-feature
invocations. Previously created tasks with incorrect (missing) convention references are
point-in-time artifacts and would need manual correction if deemed important.

### Summary of findings

| Finding | Detail |
|---------|--------|
| Defect file | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` |
| Defect — extraction | `line[3:]` does not strip trailing whitespace from heading text |
| Defect — comparison | Exact match `convention_name in discovered_conventions` fails silently |
| Missing test coverage | `evals/plan-feature/files/conventions-mock.md` lacks trailing-whitespace fixture |
| No persistence boundary | Fix corrects future invocations; no migration needed |
| No CONVENTIONS.md at root | No convention enrichment applies to the fix task |
