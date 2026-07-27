# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

The bug involves the plan-feature skill's internal convention parsing logic. This is
a code-path tracing scenario rather than a runnable reproduction, because the steps
reference a `/plan-feature` skill invocation that depends on a full Jira-connected
environment.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` skill invocation.

**Trace through convention parsing**:

1. The plan-feature skill reads `CONVENTIONS.md` from the target repository root.
2. It splits the file content by newlines and iterates over each line.
3. For lines starting with `## `, it extracts the heading text using `line[3:]`.
4. The extracted heading becomes the key in a `conventions` dictionary.

**Divergence point identified**: At step 3, `line[3:]` extracts everything after
`## ` including trailing whitespace. For the heading line `## Migration Patterns  \n`,
the extracted key becomes `"Migration Patterns  "` (with two trailing spaces).

**Downstream failure**: When the task enrichment step looks up conventions by name
using `if convention_name in discovered_conventions`, it uses the clean name
`"Migration Patterns"` (without trailing spaces). This exact-match comparison fails
against the key `"Migration Patterns  "`, so the convention is silently skipped.

**No warning or error**: The code does not log when a convention lookup fails to match,
resulting in silent omission.

**Reproduction outcome**: Confirmed via code-path tracing. The root cause is
deterministic -- any CONVENTIONS.md heading with trailing whitespace will trigger
this bug.

## Step 3 -- Codebase Investigation

### Target repository

| Field | Value |
|-------|-------|
| Repository | acme-backend |
| Serena Instance | serena_backend |
| Path | /home/dev/repos/acme-backend |

The Component field (`sdlc-workflow`) and the Steps to Reproduce (referencing
`/plan-feature`) confirm the bug is in the `plugins/sdlc-workflow/skills/plan-feature/`
code path.

### Code Intelligence note

Per the CLAUDE.md Code Intelligence section: "No Serena MCP servers are configured.
Code intelligence is not available." Falling back to Read/Grep/Glob analysis of
the repository context provided.

### Affected files and symbols

#### 1. Convention heading extraction -- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

**Defect**: `line[3:]` preserves trailing whitespace from the heading line. Should
use `line[3:].strip()` or `line[3:].rstrip()` to normalize the key.

#### 2. Convention-aware task enrichment -- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

**Impact**: This exact-match lookup fails when the dictionary key has trailing
whitespace but the lookup key does not.

### Existing test coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing
whitespace on headings. This edge case has no test coverage.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions
apply to the fix task itself.

### Investigation summary

| Finding | Detail |
|---------|--------|
| Affected file | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` |
| Affected symbol | Convention heading extraction loop (`line[3:]`) |
| Defect type | Missing string normalization (trailing whitespace not stripped) |
| Silent failure | No warning logged when convention lookup misses |
| Test gap | `evals/plan-feature/files/conventions-mock.md` lacks trailing whitespace test case |
| Fix scope | Single root cause, single file -- no decomposition needed |
