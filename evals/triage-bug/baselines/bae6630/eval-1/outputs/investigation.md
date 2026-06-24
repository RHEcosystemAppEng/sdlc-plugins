# Steps 2-3 -- Codebase Investigation Findings for ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction method: Code-path tracing

This bug involves a skill behavior (plan-feature convention conformance analysis) that cannot
be directly reproduced via CLI commands in a read-only context. Code-path tracing was used instead.

### Trace findings

**Entry point**: `/plan-feature ACME-100` invocation, which triggers the convention conformance
analysis within the plan-feature skill.

**Code path traced**:

1. The plan-feature skill reads `CONVENTIONS.md` and parses headings to build a conventions dictionary.
2. The heading extraction logic at `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` uses:
   ```python
   section_name = line[3:]  # Extracts heading text after "## "
   ```
   This does NOT call `.strip()` on the extracted heading text.
3. When a heading line contains trailing whitespace (e.g., `## Migration Patterns  \n`), the
   extracted section name becomes `"Migration Patterns  "` (with trailing spaces).
4. The task enrichment step later attempts an exact match:
   ```python
   if convention_name in discovered_conventions:
   ```
   The lookup key `"Migration Patterns"` (without trailing spaces) does not match the stored key
   `"Migration Patterns  "` (with trailing spaces), so the convention is silently skipped.
5. No warning or error is emitted when a convention name fails to match.

**Divergence point**: The heading extraction at `line[3:]` is where the behavior diverges from
expected. The lack of `.strip()` causes the exact-match comparison to fail silently.

**Reproduction outcome**: Confirmed via code-path tracing. The bug is deterministic and will occur
whenever a CONVENTIONS.md heading line has trailing whitespace.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend
- **Component**: sdlc-workflow (from Bug metadata)

Note: Per the Code Intelligence section in CLAUDE.md, no Serena MCP servers are actually configured.
Investigation was performed using Read/Grep/Glob fallback (simulated via the mock repo context).

### Affected files and symbols

| File | Symbol/Section | Role |
|------|---------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis -- heading extraction (`line[3:]`) | **Defect location**: extracts heading without stripping trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | **Failure point**: exact-match lookup fails due to whitespace mismatch |
| `evals/plan-feature/files/conventions-mock.md` | Existing eval fixture | **Gap**: does not include trailing whitespace on headings, so this edge case is untested |

### Existing test coverage

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT include
trailing whitespace on headings. This means the trailing-whitespace edge case is not covered by
current evals, explaining why this regression was not caught.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions apply to the fix task.

### Patterns discovered for fix guidance

1. **Heading extraction pattern**: `line[3:]` needs to be changed to `line[3:].strip()` to normalize
   trailing whitespace.
2. **Silent failure pattern**: The convention lookup does not log a warning when a convention name
   is not found. Adding a warning would improve observability for similar issues.
3. **Test fixture pattern**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md`
   can be extended with a trailing-whitespace variant to serve as a reproducer test.
