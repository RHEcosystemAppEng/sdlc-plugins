## Repository
acme-backend

## Target Branch
main

## Description
Fix convention heading extraction in plan-feature skill to strip trailing whitespace,
preventing silent match failures when CONVENTIONS.md headings contain trailing spaces.
Fixes ACME-511.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to heading extraction at `line[3:]` to normalize section names

## Files to Create
- `evals/plan-feature/files/conventions-whitespace-mock.md` -- eval fixture with trailing whitespace on headings for reproducer test

## Implementation Notes
The defect is in the convention heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code:

```python
section_name = line[3:]
```

must be changed to:

```python
section_name = line[3:].strip()
```

This ensures that heading text like `## Migration Patterns  ` is extracted as `"Migration Patterns"` rather than `"Migration Patterns  "`, allowing the downstream exact-match comparison in the convention-aware task enrichment step to succeed:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md SS{convention_name}: {action}")
```

**Existing patterns to follow:**
- The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` provides the pattern for convention mock files -- follow the same format but include trailing whitespace on headings.
- The convention extraction and enrichment logic are co-located in the same file.

**Reproducer test guidance:**
- Input: a CONVENTIONS.md mock with headings containing trailing spaces (e.g., `## Migration Patterns  `)
- Before fix: extracted section name is `"Migration Patterns  "`, convention match fails
- After fix: extracted section name is `"Migration Patterns"`, convention match succeeds

The repository does not have a `CONVENTIONS.md` at its root, so no convention-specific implementation patterns apply.

Fixes ACME-511.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing convention mock fixture; reuse its structure for the whitespace-variant fixture

## Acceptance Criteria
- [ ] A reproducer test demonstrates the trailing whitespace bug: a convention heading with trailing spaces is extracted and matched successfully (test fails before fix, passes after fix)
- [ ] The heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` strips trailing whitespace from extracted section names using `.strip()`
- [ ] Convention-aware task enrichment matches convention sections whose source headings contain trailing whitespace
- [ ] No regression in existing plan-feature evals and tests

## Test Requirements
- [ ] Reproducer test: create an eval fixture (`evals/plan-feature/files/conventions-whitespace-mock.md`) with at least one heading containing trailing whitespace (e.g., `## Migration Patterns  `), run convention extraction, and assert that the extracted section name equals `"Migration Patterns"` (no trailing spaces) and that the convention-aware enrichment step produces the expected notes
- [ ] Verify that the existing eval fixture (`evals/plan-feature/files/conventions-mock.md`) continues to pass with the fix applied (no regression)

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: 1. Open the application in a browser. 2. Navigate to Settings > Appearance. 3. Toggle "Dark Mode" to ON. 4. Close the browser completely. 5. Reopen the browser and navigate back to the application.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: Convention heading extraction in `plan-feature/SKILL.md` uses `line[3:]` without `.strip()`, causing trailing whitespace in CONVENTIONS.md headings to produce section names that fail exact-match comparison in task enrichment, silently dropping convention-aware notes.
