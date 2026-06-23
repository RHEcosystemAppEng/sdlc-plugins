# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Code-path tracing

The bug cannot be directly reproduced via CLI commands because it involves the plan-feature skill's internal convention parsing logic. Tracing through the code paths described in the bug report and repository context:

1. **Entry point**: The user runs `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
2. **Convention loading**: The plan-feature skill reads `CONVENTIONS.md` and parses headings to build a map of convention sections.
3. **Heading extraction logic** (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
4. **Defect identified**: When the heading line is `## Migration Patterns  \n`, the extraction `line[3:]` produces `"Migration Patterns  "` (with trailing spaces). The code does NOT strip trailing whitespace from the extracted heading.
5. **Convention matching** (in the task enrichment step):
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
   ```
   This exact-match lookup uses `"Migration Patterns"` (without trailing spaces) as the key, which does NOT match `"Migration Patterns  "` (with trailing spaces) in the dictionary. The convention is silently skipped.

**Trace outcome**: The bug is confirmed through code-path analysis. The trailing whitespace on the heading causes the dictionary key to include extra spaces, and the subsequent exact-match lookup fails silently.

## Step 3 — Codebase Investigation

### Target repository

- **Repository**: acme-backend (based on Component: sdlc-workflow)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

Note: Code Intelligence section states "No Serena MCP servers are configured. Code intelligence is not available." Investigation uses Read/Grep/Glob fallback.

### Affected files and symbols

| File | Symbol/Location | Role |
|------|----------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis — heading extraction (`line[3:]`) | **Root cause** — does not strip trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment — `convention_name in discovered_conventions` lookup | **Failure point** — exact-match fails due to whitespace mismatch |

### Root cause location

The defect is in the heading extraction logic:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

This should be:

```python
section_name = line[3:].strip()  # Strip trailing whitespace from heading
```

### Existing test coverage

- **Existing eval fixture**: `evals/plan-feature/files/conventions-mock.md` — does NOT include trailing whitespace on headings, so this edge case is not covered by current evals.
- **No reproducer test exists** for the trailing-whitespace scenario.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to include in Implementation Notes.

### Reuse candidates

No existing utility functions for whitespace-aware heading parsing were found. The fix is localized to the heading extraction line.

### Summary of findings

The bug has a single root cause: the heading extraction logic at `line[3:]` does not strip trailing whitespace, causing exact-match convention lookups to fail silently when `CONVENTIONS.md` headings have trailing spaces. The fix is to add `.strip()` to the heading extraction. A reproducer test should use a `CONVENTIONS.md` fixture with trailing whitespace on a heading and assert that the convention is still matched and included in the generated task's Implementation Notes.
