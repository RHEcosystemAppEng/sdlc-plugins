# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Reproduction approach

The bug involves a skill invocation (`/plan-feature`) and its internal convention-matching logic. This is not directly runnable as a CLI command — it requires code-path tracing rather than direct reproduction.

### Code-path trace

**Entry point**: `/plan-feature ACME-100` invocation on a feature requiring a database migration with foreign keys.

**Trace through convention conformance analysis:**

1. The plan-feature skill reads the contents of `CONVENTIONS.md` from the target repository.

2. It iterates over lines, extracting section headings:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```

3. When the heading line is `## Migration Patterns  \n` (with trailing whitespace), the extraction `line[3:]` produces `"Migration Patterns  "` (with two trailing spaces).

4. The convention dictionary is keyed by this un-stripped name.

5. During task enrichment, the skill attempts an exact-match lookup:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```

6. The lookup key `"Migration Patterns"` does not match the stored key `"Migration Patterns  "`, so the match fails silently.

**Divergence point**: The behavior diverges from expected at step 3 — the heading extraction does not strip trailing whitespace, causing all subsequent exact-match lookups against that heading to fail.

**Trace outcome**: Bug behavior confirmed through code-path analysis. The root cause is deterministic — any `CONVENTIONS.md` heading with trailing whitespace will be silently dropped.

## Step 3 — Codebase Investigation

### Target repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

Note: Code Intelligence section indicates no Serena instances are configured, so fallback to Read/Grep/Glob was used (simulated via repo-context-mock.md).

### Affected files and symbols

| File | Symbol/Section | Role |
|------|---------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis — heading extraction | Contains the defective `line[3:]` extraction that does not strip whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment — exact-match lookup | Contains the lookup that fails due to un-stripped keys |

### Code paths involved

1. **Convention lookup** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   - Reads `CONVENTIONS.md` and splits by newline
   - Matches lines starting with `## ` to identify section headings
   - Extracts heading name via `line[3:]` without `.strip()`
   - Stores section content keyed by the un-stripped heading name

2. **Convention-aware task enrichment** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   - Iterates over expected convention names (clean, no trailing whitespace)
   - Uses `in` operator for exact-match lookup against the convention dictionary
   - Match fails when the dictionary key has trailing whitespace

### Existing test coverage

- **Eval fixture**: `evals/plan-feature/files/conventions-mock.md` — existing fixture does NOT include trailing whitespace on headings, so this edge case is not covered by current evals.
- **Gap**: No test or eval exercises the trailing-whitespace scenario.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to reference in the fix task's Implementation Notes (beyond the bug fix itself).

### Reusable patterns

- The eval infrastructure in `evals/plan-feature/` provides the pattern for adding a new eval fixture that includes trailing whitespace on headings.
- The existing `conventions-mock.md` fixture can be used as a template for the new test fixture.

### Decomposition guard (Step 6)

This bug has a **single root cause**: the missing `.strip()` call on extracted heading names in the convention lookup. The same defect manifests in two places (extraction and lookup), but they are part of the same code path, not independent issues. A single Task is appropriate — no decomposition needed.
