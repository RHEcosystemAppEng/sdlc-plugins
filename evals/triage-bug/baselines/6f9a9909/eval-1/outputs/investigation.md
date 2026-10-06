# Codebase Investigation: ACME-500

## Summary

Bug ACME-500 reports that the plan-feature skill silently drops conventions from `CONVENTIONS.md` when heading lines contain trailing whitespace. Investigation confirms the root cause is in the heading extraction logic of the plan-feature convention lookup.

## Investigated Code Paths

### 1. Convention Heading Extraction (plan-feature convention lookup)

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The plan-feature skill reads `CONVENTIONS.md` headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Finding**: The heading extraction at `line[3:]` does NOT strip trailing whitespace. When a heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces). This is the direct cause of the bug.

### 2. Convention-Aware Task Enrichment (plan-feature task generation)

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by exact section name comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Finding**: This match fails because `convention_name` (e.g., `"Migration Patterns"`) does not equal the stored key `"Migration Patterns  "` (with trailing whitespace). The convention is silently skipped -- no warning or error is raised, so the user has no indication that a convention was missed.

### 3. Existing Test Coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

**Finding**: The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is entirely uncovered by current evals, explaining why the bug was not caught during development.

### 4. Repository CONVENTIONS.md

The repository itself does not have a `CONVENTIONS.md` at its root, which means this bug surfaces only in downstream projects that maintain their own `CONVENTIONS.md` files (as reported by the user).

## Root Cause Identification

The root cause is the heading extraction expression `line[3:]` in the plan-feature convention lookup. This slicing operation preserves any trailing whitespace from the original heading line, producing section name keys that fail exact-match comparison during convention-aware task enrichment.

**Fix location**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- the convention heading extraction logic.

**Required change**: Strip trailing whitespace from the extracted heading, e.g., `line[3:].strip()` or `line[3:].rstrip()`.

**Verification approach**: Create a reproducer test with a `CONVENTIONS.md` fixture that includes trailing whitespace on heading lines, and assert that the convention is still matched and included in the generated task's Implementation Notes.
