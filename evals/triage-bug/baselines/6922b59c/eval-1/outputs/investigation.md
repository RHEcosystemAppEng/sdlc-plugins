# Codebase Investigation — ACME-500

## Step 2: Scope Identification

The bug affects the **plan-feature** skill in the **sdlc-workflow** plugin, specifically the convention conformance analysis that reads and matches headings from `CONVENTIONS.md`.

### Affected Code Paths

1. **Convention heading extraction** — `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
2. **Convention-aware task enrichment** — same file, downstream of extraction

## Step 3: Codebase Investigation Findings

### Root Cause: Trailing-whitespace heading extraction

The convention lookup code in plan-feature extracts heading text using `line[3:]`, which does **not** strip trailing whitespace:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Does NOT strip trailing whitespace
        conventions[section_name] = current_section_content
```

When the heading line in `CONVENTIONS.md` is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with trailing spaces). The downstream convention-aware task enrichment performs an exact-match comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

This match fails because `"Migration Patterns"` != `"Migration Patterns  "`.

### Why it is silent

There is no fallback, warning, or fuzzy-match logic. When the exact match fails, the convention is simply skipped with no diagnostic output.

### Test coverage gap

The existing eval fixture (`evals/plan-feature/files/conventions-mock.md`) does **not** include trailing whitespace on headings, so this edge case is not covered by current evals.

### Fix location

The fix is in the plan-feature convention lookup — `line[3:]` should be replaced with `line[3:].strip()` (or equivalent) to normalize heading text before storing it as the section key.
