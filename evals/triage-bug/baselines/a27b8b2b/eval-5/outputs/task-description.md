## Repository
acme-backend

## Target Branch
main

## Description
Fix the convention heading extraction logic to strip trailing whitespace from section
names, preventing exact-match comparison failures downstream. The current implementation
at `line[3:]` preserves trailing whitespace from heading lines, causing preference and
convention lookups to fail when keys are compared without normalization. Fixes ACME-511.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- apply `.strip()` to heading extraction at `line[3:]` to normalize whitespace

## Implementation Notes
The defect is in the convention heading extraction logic in
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code:

```python
section_name = line[3:]
```

extracts the heading text after `## ` but does NOT strip trailing whitespace. If the
heading line is `## Migration Patterns  \n`, the extracted section name becomes
`"Migration Patterns  "` (with trailing spaces), which fails exact-match comparison
against the expected `"Migration Patterns"`.

The fix is to apply `.strip()`:

```python
section_name = line[3:].strip()
```

The convention-aware task enrichment step in the same file matches conventions by
section name using:

```python
if convention_name in discovered_conventions:
```

This match fails when `convention_name` has trailing whitespace from the extraction step.
After applying `.strip()`, the keys will be normalized and matches will succeed.

**Reproducer test guidance:**

- Create a test fixture `CONVENTIONS.md` with headings containing trailing whitespace
  (e.g., `## Migration Patterns  ` with two trailing spaces after the heading text).
- Run the extraction logic against this fixture.
- The test should initially fail: the extracted key `"Migration Patterns  "` does not
  equal the expected `"Migration Patterns"`.
- After applying `.strip()`, the test should pass: the extracted key is trimmed to
  `"Migration Patterns"`.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT
include trailing whitespace on headings, so this edge case is not covered by current
evals. The reproducer test should add a new fixture specifically for this case.

Fixes ACME-511.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the trailing-whitespace bug: it fails before the fix (extracted heading includes trailing spaces) and passes after the fix (extracted heading is trimmed)
- [ ] Convention heading extraction at `line[3:]` applies `.strip()` to normalize whitespace
- [ ] Convention-aware task enrichment correctly matches sections by their trimmed names
- [ ] No regression in existing tests (`evals/plan-feature/` test suite passes)

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with headings containing trailing whitespace (e.g., `## Migration Patterns  `), run the extraction logic, and assert the extracted section name equals the trimmed heading `"Migration Patterns"` (not `"Migration Patterns  "`)
- [ ] Verify that convention-aware task enrichment matches the trimmed section name against the discovered conventions dictionary
- [ ] Ensure existing eval fixtures in `evals/plan-feature/files/conventions-mock.md` continue to pass without modification

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: 1) Open the application, 2) Navigate to Settings > Appearance, 3) Toggle "Dark Mode" to ON, 4) Close the browser completely, 5) Reopen the browser and navigate back to the application
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: The heading/key extraction logic at `line[3:]` does not strip trailing whitespace, causing exact-match lookups to fail when keys are stored with trailing spaces. On subsequent loads, the clean key does not match the whitespace-padded stored key, and the application defaults to light mode.
