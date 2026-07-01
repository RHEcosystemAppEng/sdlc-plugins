# Steps 2-3: Codebase Investigation

## Tracing the Code Path from Steps to Reproduce

The bug report describes the following reproduction flow:

1. A `CONVENTIONS.md` file exists with trailing whitespace on a heading line: `## Migration Patterns  \n`
2. The `/plan-feature` skill is invoked on a feature issue
3. The plan-feature skill reads `CONVENTIONS.md` and attempts to extract convention sections
4. The generated task's Implementation Notes should reference the matched convention but do not

### Step 1: Convention Heading Extraction

**File:** `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Convention conformance analysis

The plan-feature skill parses `CONVENTIONS.md` headings using the following logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

When the heading line is `## Migration Patterns  \n`:
- `line.split('\n')` strips the newline, producing `"## Migration Patterns  "` (with two trailing spaces)
- `line.startswith('## ')` evaluates to `True`
- `line[3:]` extracts `"Migration Patterns  "` (with two trailing spaces preserved)
- The key stored in `conventions` dict is `"Migration Patterns  "` (trailing spaces included)

**Root issue identified:** `line[3:]` does NOT call `.strip()` or `.rstrip()` on the extracted heading text. Trailing whitespace from the source file is preserved in the dictionary key.

### Step 2: Convention-Aware Task Enrichment

**File:** `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Convention-aware task enrichment

The task enrichment step looks up conventions by a clean section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

Here, `convention_name` is `"Migration Patterns"` (without trailing whitespace) -- this is the canonical, clean name expected by the matching logic.

The lookup `"Migration Patterns" in discovered_conventions` fails because the dictionary key is `"Migration Patterns  "` (with trailing spaces). Python dict key lookup uses exact string equality, so `"Migration Patterns" != "Migration Patterns  "`.

### Step 3: Silent Failure

The condition `if convention_name in discovered_conventions` simply evaluates to `False`. There is no `else` branch that logs a warning or raises an error. The convention is silently skipped, and no note is appended to the task's Implementation Notes.

This explains both symptoms described in the bug:
- The generated task's Implementation Notes omit the convention reference
- No warning or error is shown

## Test Coverage Gap

**File:** `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. All headings in the mock fixture are clean (no trailing spaces), which means this edge case is not covered by current evals. The bug is invisible to the existing test suite.

## Summary of Affected Code Paths

| File | Section | Issue |
|------|---------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis | `line[3:]` preserves trailing whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment | Exact-match lookup fails on whitespace mismatch |
| `evals/plan-feature/files/conventions-mock.md` | Test fixture | Missing trailing-whitespace edge case |
