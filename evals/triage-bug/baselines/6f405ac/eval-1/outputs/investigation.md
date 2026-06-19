# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Reproduction approach

This bug affects the plan-feature skill's convention conformance analysis, which is a
skill-level logic issue rather than a directly runnable command. Code-path tracing was
used instead of runnable reproduction.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` invocation triggers convention conformance analysis.

**Trace findings**:

1. The plan-feature skill reads `CONVENTIONS.md` and parses headings using:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```

2. When the heading line is `## Migration Patterns  \n`, the extraction at `line[3:]`
   produces `"Migration Patterns  "` (with trailing spaces) as the section name.

3. The convention-aware task enrichment step later performs an exact-match lookup:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
   ```

4. The lookup key `"Migration Patterns"` (no trailing spaces) does not match the
   stored key `"Migration Patterns  "` (with trailing spaces), so the match fails
   silently.

**Reproduction outcome**: Confirmed via code-path tracing. The bug is deterministic --
any CONVENTIONS.md heading with trailing whitespace will be silently dropped.

## Step 3 — Codebase Investigation

### Target repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend
- **Component**: sdlc-workflow (from Bug metadata)

### Code Intelligence

No Serena MCP servers are configured. Fallback to Read/Grep/Glob used.

### Affected files and symbols

| File | Symbol / Location | Issue |
|------|-------------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Does not strip trailing whitespace from heading text |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Exact-match comparison fails when key has trailing whitespace |

### Root cause location

The defect is in the heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
The line `section_name = line[3:]` does not call `.strip()` on the extracted heading text. This causes
the stored dictionary key to include trailing whitespace, which then fails exact-match lookups
in the task enrichment step.

### Existing test coverage

- **Existing test**: `evals/plan-feature/files/conventions-mock.md` -- the existing eval fixture
  does NOT include trailing whitespace on headings, so this edge case is not covered.
- No other test files were found that exercise convention heading parsing with whitespace variants.

### CONVENTIONS.md lookup

The repository does not have a CONVENTIONS.md at its root. No additional conventions apply.

### Reuse candidates

- The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` can be used as a
  reference for creating the reproducer test fixture -- a variant with trailing whitespace on
  headings should be added.
