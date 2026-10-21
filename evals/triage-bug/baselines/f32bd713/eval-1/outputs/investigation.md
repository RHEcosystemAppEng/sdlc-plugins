# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Code-path tracing

The bug cannot be directly reproduced via runnable commands (it involves a skill
invocation that produces Jira task descriptions). Code-path tracing is used instead.

**Entry point**: `/plan-feature ACME-100` skill invocation.

**Trace through convention conformance analysis**:

1. The plan-feature skill reads `CONVENTIONS.md` and parses section headings using a
   line-by-line scan:

   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```

2. When the heading line is `## Migration Patterns  \n` (with trailing whitespace),
   `line[3:]` produces `"Migration Patterns  "` (with trailing spaces) rather than
   the expected `"Migration Patterns"`.

3. The convention-aware task enrichment step performs an exact match:

   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
   ```

4. The match fails because `"Migration Patterns"` (the lookup key) does not equal
   `"Migration Patterns  "` (the stored key with trailing whitespace). The convention
   is silently skipped with no warning.

**Divergence point**: The divergence occurs at `line[3:]` in the heading extraction.
The code does not call `.strip()` or `.rstrip()` on the extracted section name,
causing trailing whitespace from the source file to propagate into the dictionary
key used for later lookups.

**Reproduction outcome**: Confirmed via code-path trace. The bug is deterministic:
any trailing whitespace on a `## ` heading in `CONVENTIONS.md` will cause the
corresponding convention to be silently dropped.

## Step 3 -- Codebase Investigation

### Target Repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Affected Files and Symbols

| File | Symbol/Location | Issue |
|------|-----------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Does not strip trailing whitespace from extracted section name |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Exact match fails when dictionary key has trailing whitespace |

### Code Paths Involved

1. **Heading extraction path**: `conventions_content.split('\n')` -> `line.startswith('## ')` -> `line[3:]` -> `conventions[section_name] = ...`
2. **Convention matching path**: `convention_name in discovered_conventions` -> `notes.append(...)` (never reached due to key mismatch)

### Existing Test Coverage

- **Existing eval fixture**: `evals/plan-feature/files/conventions-mock.md` -- this
  fixture does NOT include trailing whitespace on headings, so the edge case is not
  covered by current evals.
- No dedicated test exists for whitespace handling in convention heading extraction.

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions apply
to the fix task itself.

### Persistence-Impact Analysis

The buggy function's output (the extracted convention section names) is used to
generate Jira task descriptions at task-creation time. The output flows into the
Jira `description` field via `jira.create_issue`. However:

- The incorrect behavior is in the **convention lookup logic**, not in persisted
  data storage within the application's own database.
- Jira task descriptions created while the bug was present may be missing convention
  references, but these are Jira issues (external system), not application database
  records.
- The fix corrects future convention lookups. Previously created tasks with missing
  conventions would need manual review but do not constitute a data migration scenario.

**Conclusion**: No persistence boundary found within the application. No data
migration is needed. The fix corrects future behavior.

### Reuse Candidates

No existing whitespace-stripping utilities were identified in the convention parsing
code. Standard Python `str.strip()` is the appropriate fix mechanism.

### Investigation Summary

The bug is a single-root-cause defect: `line[3:]` in the heading extraction does not
strip trailing whitespace, causing exact-match lookup failures downstream. The fix is
localized to the heading extraction code in the plan-feature skill's convention
conformance analysis. No decomposition is needed (Step 6 -- single root cause).
