## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace
from CONVENTIONS.md heading lines before using them as dictionary keys. Currently,
headings with trailing spaces (e.g., `## Migration Patterns  `) produce keys like
`"Migration Patterns  "` that fail exact-match lookups, causing conventions to be
silently dropped from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Add `.strip()` to heading extraction (`section_name = line[3:].strip()`) and optionally add warning log for whitespace-padded headings

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- Test fixture with trailing whitespace on convention headings to cover the edge case

## Implementation Notes
The root cause is in the convention heading extraction logic in
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

Must be changed to:

```python
section_name = line[3:].strip()  # Strips trailing whitespace from headings
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces)
produce clean keys (`"Migration Patterns"`) that match the enrichment step's lookups.

For defense in depth, also consider stripping the lookup key in the convention-aware
task enrichment section:

```python
if convention_name.strip() in discovered_conventions:
```

The existing test fixture at `evals/plan-feature/files/conventions-mock.md` does NOT
include trailing whitespace on headings, so a new fixture is needed to cover this
edge case. The new fixture should mirror the existing one but add trailing whitespace
(2+ spaces) to at least one heading line.

Fixes ACME-500.

## Acceptance Criteria
- [ ] A reproducer test exists that creates a CONVENTIONS.md with trailing whitespace on a heading, runs the convention conformance analysis, and asserts the convention IS included in the generated task's Implementation Notes (fails before fix, passes after fix)
- [ ] `section_name = line[3:]` is replaced with `section_name = line[3:].strip()` in the convention heading extraction logic
- [ ] Conventions with trailing whitespace on headings are correctly matched and included in generated task descriptions
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: Create a CONVENTIONS.md fixture with trailing whitespace on the heading `## Migration Patterns  ` (two trailing spaces). Run the plan-feature convention conformance analysis against a feature requiring the "Migration Patterns" convention. Assert that the generated task's Implementation Notes contain `Per CONVENTIONS.md "Migration Patterns: add Index::create() for all FK columns.` -- this test must fail before the fix and pass after
- [ ] Existing convention conformance tests continue to pass with clean (no trailing whitespace) headings
- [ ] Edge case: headings with mixed whitespace (tabs, multiple spaces) are handled correctly

## Verification Commands
- Run plan-feature eval suite to confirm no regressions
- Run the new trailing-whitespace eval case to confirm the fix

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md "Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: Convention heading extraction uses `line[3:]` without `.strip()`, causing trailing whitespace in section names to break exact-match lookups in the convention-aware task enrichment step.
