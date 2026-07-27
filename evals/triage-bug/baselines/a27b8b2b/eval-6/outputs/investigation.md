# Step 2 and Step 3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

This bug involves the plan-feature skill's internal behavior when parsing CONVENTIONS.md headings. It is not directly reproducible via CLI commands in a read-only context -- it requires a code-path trace.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` invocation on a feature requiring database migration with foreign keys.

**Trace through the affected code**:

1. The plan-feature skill reads `CONVENTIONS.md` content as raw text.
2. It iterates over lines, looking for lines that start with `## ` to identify convention section headings.
3. The heading extraction uses `line[3:]` to extract the section name -- this slices from position 3 to end of string.
4. **Defect location**: `line[3:]` does NOT strip trailing whitespace. If the heading line is `## Migration Patterns  \n`, the extracted key becomes `"Migration Patterns  "` (with trailing spaces).
5. During task enrichment, the skill looks up convention names via exact-match: `if convention_name in discovered_conventions`. The lookup key `"Migration Patterns"` does not match the stored key `"Migration Patterns  "`.
6. The convention is silently skipped -- no warning or error is logged.

**Divergence point**: Step 3 (heading extraction) produces a key with trailing whitespace that fails the exact-match lookup in Step 5.

**Trace outcome**: Bug behavior confirmed via code-path analysis.

## Step 3 -- Codebase Investigation

### Target repository

- **Component**: sdlc-workflow
- **Target repository**: acme-backend (from Repository Registry)
- **Serena instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Code Intelligence note

Per CLAUDE.md Code Intelligence section: "No Serena MCP servers are configured. Code intelligence is not available." Falling back to Read/Grep/Glob analysis using the mock repository context.

### Affected files and symbols

#### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Convention heading extraction** (convention lookup section):

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

- **Symbol**: Heading extraction logic at `line[3:]`
- **Defect**: `line[3:]` does not call `.strip()` on the extracted section name. Trailing whitespace (spaces, tabs) from the heading line is preserved in the dictionary key.

**Convention-aware task enrichment** (task enrichment section):

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

- **Symbol**: Convention matching logic via `in` operator
- **Defect**: Exact-match comparison fails when the key has trailing whitespace but the lookup string does not.

### Existing test coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No repository-level conventions to inform the fix task's Implementation Notes.

### Investigation findings summary

| Finding | Detail |
|---------|--------|
| Affected file | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` |
| Affected symbol (extraction) | `line[3:]` in convention heading loop |
| Affected symbol (matching) | `convention_name in discovered_conventions` |
| Root cause | Missing `.strip()` call on extracted heading text |
| Silent failure | No warning logged when convention match fails |
| Test gap | Existing eval fixture lacks trailing-whitespace headings |
| Existing test file | `evals/plan-feature/files/conventions-mock.md` |
| CONVENTIONS.md present | No |
