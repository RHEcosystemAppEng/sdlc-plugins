## Repository
acme-backend

## Target Branch
main

## Description
Fix convention heading extraction in the plan-feature skill to strip trailing whitespace from parsed section names. Currently, `line[3:]` retains trailing spaces from CONVENTIONS.md headings, causing exact-match lookups in the task enrichment step to silently fail. This fix ensures convention-aware notes are reliably included in generated tasks. Fixes ACME-511.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the heading extraction line to normalize section names

## Implementation Notes
The defect is in the convention heading extraction logic within plan-feature:

```python
section_name = line[3:]  # current: retains trailing whitespace
```

Change to:

```python
section_name = line[3:].strip()  # fixed: strips trailing whitespace
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) are stored as `"Migration Patterns"` in the `conventions` dictionary, so the downstream lookup:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md section {convention_name}: {action}")
```

succeeds regardless of trailing whitespace in the source CONVENTIONS.md file.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings, so a new reproducer test fixture must be created to cover this edge case.

Fixes ACME-511.

## Acceptance Criteria
- [ ] A reproducer test exists that creates a CONVENTIONS.md fixture with trailing whitespace on headings (e.g., `## Migration Patterns  `) and asserts that convention matching succeeds -- this test must fail before the fix and pass after
- [ ] The heading extraction logic in plan-feature strips trailing whitespace from parsed section names using `.strip()`
- [ ] Convention-aware task enrichment correctly matches conventions when CONVENTIONS.md headings contain trailing whitespace
- [ ] No regression in existing plan-feature evals and tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md eval fixture with at least one heading that has trailing whitespace (e.g., `## Migration Patterns  `), run the convention extraction logic, and assert (a) the extracted key equals `"Migration Patterns"` (no trailing spaces), and (b) the downstream convention lookup succeeds for that section name
- [ ] Verify existing evals in `evals/plan-feature/` continue to pass with the `.strip()` change
- [ ] Edge case: heading with multiple trailing spaces and tabs is correctly stripped
- [ ] Edge case: heading with no trailing whitespace is unaffected by the change

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: (1) Open the application, (2) navigate to Settings > Appearance, (3) toggle Dark Mode to ON, (4) close browser completely, (5) reopen browser and navigate back to the application
- **Expected Result**: The application should load in dark mode, matching the user's last preference
- **Actual Result**: The application loads in light mode; the dark mode toggle is reset to OFF
- **Root Cause**: Convention heading extraction in plan-feature uses `line[3:]` without stripping trailing whitespace, causing exact-match lookups in task enrichment to fail when CONVENTIONS.md headings contain trailing spaces
