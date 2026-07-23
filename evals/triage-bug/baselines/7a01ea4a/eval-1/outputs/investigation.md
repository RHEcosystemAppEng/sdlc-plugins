# Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

The bug involves the plan-feature skill's behavior when processing CONVENTIONS.md files with
trailing whitespace on headings. This is a skill/documentation-level bug that cannot be directly
reproduced via CLI commands -- the Steps to Reproduce describe invoking `/plan-feature`, which is
a Claude Code skill invocation. Code-path tracing is the appropriate approach.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` skill invocation

**Trace through convention conformance analysis**:

1. The plan-feature skill reads `CONVENTIONS.md` and parses section headings.
2. The heading extraction logic at `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` uses:
   ```python
   section_name = line[3:]  # Extracts heading text after "## "
   ```
3. When the heading line is `## Migration Patterns  \n`, the extracted `section_name` becomes
   `"Migration Patterns  "` (with two trailing spaces).
4. The convention-aware task enrichment step performs an exact-match lookup:
   ```python
   if convention_name in discovered_conventions:
   ```
5. The lookup key `"Migration Patterns"` (without trailing spaces) does NOT match the stored key
   `"Migration Patterns  "` (with trailing spaces), so the convention is silently skipped.
6. No warning or error is emitted when a convention fails to match.

**Divergence point**: Step 3 above -- the `line[3:]` extraction does not call `.strip()` or
`.rstrip()` to remove trailing whitespace. This causes the downstream exact-match comparison
in Step 5 to fail.

**Trace outcome**: Bug behavior confirmed through code-path analysis. The root cause is the
missing whitespace normalization in the heading extraction logic.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend
- **Component match**: sdlc-workflow (from bug's Component field)

### Code Intelligence note

Per CLAUDE.md: "No Serena MCP servers are configured. Code intelligence is not available."
Investigation performed using Read/Grep/Glob fallback.

### Affected files and symbols

#### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Convention heading extraction** (convention conformance analysis section):
```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

- The `line[3:]` slice captures everything after `## `, including any trailing whitespace.
- No `.strip()` or `.rstrip()` is applied to normalize the section name.

**Convention-aware task enrichment** (task enrichment section):
```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

- This performs an exact-match dictionary lookup using a clean (no trailing whitespace) key.
- When the stored key has trailing whitespace, the lookup fails silently.

### Existing test coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on
headings. This means the trailing-whitespace edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository (`acme-backend`) does not have a `CONVENTIONS.md` file at its root. No conventions
apply to the fix task's Implementation Notes.

### Patterns and reuse candidates

- The heading extraction logic is localized to the convention conformance analysis section of
  `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
- The fix should apply `.strip()` to the extracted section name to normalize whitespace.
- The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` provides the
  pattern for creating a reproducer test fixture with trailing whitespace.

### Investigation summary

| Finding | Detail |
|---------|--------|
| Affected file | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` |
| Affected logic | Convention heading extraction (`line[3:]` without strip) |
| Impact | Convention-aware task enrichment silently skips conventions with trailing whitespace |
| Silent failure | No warning or error is logged when a convention match fails |
| Test gap | Existing eval fixture lacks trailing whitespace edge case |
| Scope | Single root cause, single file affected |
