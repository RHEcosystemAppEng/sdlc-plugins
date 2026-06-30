# Steps 2-3: Codebase Investigation

## Step 2: Code-Path Tracing

### Convention Lookup Logic

The plan-feature skill reads `CONVENTIONS.md` and extracts section headings using the following logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Critical finding**: `line[3:]` does NOT strip trailing whitespace. When the heading line in `CONVENTIONS.md` is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with trailing spaces).

### Convention-Aware Task Enrichment

The task enrichment step matches conventions by exact section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

This match fails silently because `convention_name` (e.g., `"Migration Patterns  "`) has trailing whitespace that does not match the expected key `"Migration Patterns"`. The convention is silently dropped with no warning or error logged.

## Step 3: Scope Assessment

### Affected Files

- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — heading extraction logic: `section_name = line[3:]`

### Test Coverage Gap

The existing test fixture at `evals/plan-feature/files/conventions-mock.md` does NOT cover this edge case. Its headings do not include trailing whitespace, so current evals pass without exercising this code path.

### Isolation

The root cause is isolated to a single code path: heading extraction in plan-feature's convention lookup. The convention-aware task enrichment logic downstream is correct — it would work if the heading extraction produced clean keys.
