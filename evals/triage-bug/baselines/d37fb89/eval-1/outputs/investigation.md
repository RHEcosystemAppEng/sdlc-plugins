# Codebase Investigation — ACME-500

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Code Intelligence

No Serena MCP servers are configured. Investigation performed using Read/Grep/Glob fallback.

## Step 2 — Reproduce/Trace

This bug relates to the plan-feature skill's internal convention-matching logic, which cannot be directly reproduced via a CLI command. Code-path tracing was used instead.

### Code-path trace

1. **Entry point**: `/plan-feature ACME-100` invocation triggers the plan-feature skill.
2. **Convention loading**: The skill reads `CONVENTIONS.md` and parses headings to build a dictionary of convention sections.
3. **Heading extraction**: In `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, the convention lookup iterates over lines:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
   The `line[3:]` slice extracts everything after `## `, including any trailing whitespace. For a heading like `## Migration Patterns  \n`, the extracted key becomes `"Migration Patterns  "` (with two trailing spaces).

4. **Convention matching**: The task enrichment step performs an exact-match lookup:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   The lookup key `"Migration Patterns"` (without trailing spaces) does not match the stored key `"Migration Patterns  "` (with trailing spaces), so the convention is silently skipped.

5. **No error or warning**: The code does not log or warn when a convention match fails, making this a silent failure.

### Trace outcome

The bug is confirmed through code-path tracing. The root cause is the missing `.strip()` call on heading extraction.

## Step 3 — Codebase Investigation

### Affected Files and Symbols

| File | Symbol/Section | Role |
|------|---------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis — heading extraction loop | Contains the defective `line[3:]` extraction without `.strip()` |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment — `convention_name in discovered_conventions` | Performs exact-match lookup that fails due to whitespace mismatch |

### Existing Test Coverage

- **Existing fixture**: `evals/plan-feature/files/conventions-mock.md` — the current eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals.
- **No reproducer test exists** for trailing-whitespace handling in convention headings.

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No additional conventions to reference in the fix task.

### Patterns and Reuse Candidates

- The convention heading parsing logic is centralized in the plan-feature skill's SKILL.md convention conformance analysis section.
- The fix should be applied at the extraction point (`line[3:]`) by adding `.strip()` to normalize the heading text.
- Existing eval patterns in `evals/plan-feature/` can serve as a model for creating a new eval fixture that includes trailing whitespace on headings.
