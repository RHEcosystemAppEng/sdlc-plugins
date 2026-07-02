# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Reproduction Method

This bug involves a skill's internal logic (plan-feature convention conformance analysis), not a directly runnable command. Code-path tracing was used instead of direct reproduction.

### Code-Path Trace

**Entry point**: `/plan-feature ACME-100` invocation on a feature requiring database migration with foreign keys.

**Trace through convention lookup** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):

1. The plan-feature skill reads `CONVENTIONS.md` and iterates over lines to extract section headings.
2. The heading extraction logic is:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
3. When the heading line is `## Migration Patterns  \n` (with trailing spaces), `line[3:]` produces `"Migration Patterns  "` (with trailing whitespace preserved).
4. This key is stored in the `conventions` dictionary as `"Migration Patterns  "`.

**Trace through convention-aware task enrichment** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):

1. The enrichment step looks up conventions by name:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
2. The lookup key `convention_name` is `"Migration Patterns"` (without trailing whitespace).
3. The dictionary key is `"Migration Patterns  "` (with trailing whitespace).
4. The exact-match comparison `"Migration Patterns" in discovered_conventions` returns `False`.
5. The convention is silently skipped — no warning or error is emitted.

**Trace conclusion**: The divergence occurs at the heading extraction step. The extraction does not strip trailing whitespace, causing an exact-match mismatch downstream. The bug is **confirmed by trace**.

## Step 3 — Codebase Investigation

### Target Repository

- **Repository**: acme-backend
- **Component**: sdlc-workflow
- **Serena Instance**: serena_backend (however, Code Intelligence section notes no Serena instances are configured; falling back to Read/Grep/Glob)

### Affected Files and Symbols

| File | Symbol/Section | Role |
|------|---------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis — heading extraction loop | **Defect location**: `line[3:]` does not call `.strip()` or `.rstrip()` |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment — `convention_name in discovered_conventions` lookup | **Failure point**: exact-match comparison fails due to trailing whitespace in key |

### Existing Test Coverage

| Test File | Covers Trailing Whitespace? |
|-----------|---------------------------|
| `evals/plan-feature/files/conventions-mock.md` | **No** — existing eval fixture does not include trailing whitespace on headings |

No existing test covers this edge case.

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to incorporate into the fix task's Implementation Notes.

### Investigation Summary

- **Single root cause**: The heading extraction code uses `line[3:]` without stripping trailing whitespace, causing downstream exact-match lookups to fail silently.
- **No warning mechanism**: There is no logging or warning when a convention section is skipped due to a name mismatch.
- **No test coverage**: The existing eval fixtures do not test headings with trailing whitespace.
- **Fix scope**: The fix is localized to the heading extraction logic in plan-feature's convention conformance analysis. A single `.strip()` call on the extracted section name would resolve the issue.
