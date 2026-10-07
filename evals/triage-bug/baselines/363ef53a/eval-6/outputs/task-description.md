## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading parser to strip trailing whitespace from CONVENTIONS.md headings, preventing silent convention drops during task enrichment. Currently, headings with trailing spaces (e.g., `## Migration Patterns  `) are stored with those spaces in the conventions dictionary, causing exact-match lookups to fail silently.

## Bug Context
- **Bug**: ACME-500 -- plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature` on a feature that should match that convention, and observe that the generated task omits the convention reference.
- **Expected Result**: The generated task's Implementation Notes should include the convention reference (e.g., "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.").
- **Actual Result**: The convention is silently dropped from the generated task with no warning or error.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, causing exact-match comparison failures in the task enrichment step.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- fix heading extraction to strip trailing whitespace and add warning log for unmatched conventions

## Files to Create
- `evals/plan-feature/files/conventions-trailing-ws-mock.md` -- eval fixture with trailing whitespace on convention headings for regression testing

## Implementation Notes
- In the convention heading parser, change `section_name = line[3:]` to `section_name = line[3:].strip()` to normalize heading text before storing in the conventions dictionary.
- Add a warning log in the task enrichment step when a convention name that was expected to match is not found in `discovered_conventions`, to prevent future silent failures.
- Follow the existing convention parsing pattern in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.

## Acceptance Criteria
- [ ] Reproducer test: a CONVENTIONS.md fixture with trailing whitespace on heading lines is correctly parsed and matched during plan-feature convention conformance analysis
- [ ] Heading extraction strips trailing whitespace so that `## Migration Patterns  ` produces section name `"Migration Patterns"`
- [ ] Convention-aware task enrichment matches conventions regardless of trailing whitespace in CONVENTIONS.md headings
- [ ] A warning is logged when an expected convention is not found in the discovered conventions dictionary
- [ ] Existing plan-feature evals continue to pass (no regression)

## Test Requirements
- [ ] Reproducer test: eval fixture with trailing whitespace on CONVENTIONS.md headings verifies that conventions are correctly included in generated task descriptions
- [ ] Test that headings with no trailing whitespace continue to work correctly (regression guard)
- [ ] Test that headings with mixed whitespace (tabs, multiple spaces) are also handled

## Verification Commands
- `python -m pytest evals/plan-feature/ -v` -- all plan-feature evals pass including the new trailing-whitespace fixture
