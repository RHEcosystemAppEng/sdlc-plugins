<!-- Jira API Metadata
jira.create_issue parameters:
  project: ACME
  issue_type: Task
  labels:
    - ai-generated-jira
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace, so that conventions in `CONVENTIONS.md` with trailing whitespace on heading lines are correctly matched and included in generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the convention heading extraction logic to normalize section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- eval fixture with trailing whitespace on convention headings for reproducer test

## Implementation Notes
The bug is in the convention heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code extracts heading text with `section_name = line[3:]`, which preserves any trailing whitespace from the heading line. This causes exact-match lookups to fail silently when headings have trailing spaces.

**Fix**: Change `section_name = line[3:]` to `section_name = line[3:].strip()` to normalize whitespace.

**Reproducer test guidance**: Create a `CONVENTIONS.md` fixture containing:
```
## Migration Patterns  
Add Index::create() for all FK columns.
```
(Note the trailing spaces after "Migration Patterns".)

The reproducer should invoke the convention conformance analysis with this fixture and assert that the "Migration Patterns" convention IS included in the generated task's Implementation Notes. Before the fix, the convention will be silently dropped; after the fix, it will appear as expected.

**Existing test pattern**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` provides the pattern for convention mock files. The reproducer fixture should follow the same format but include trailing whitespace on at least one heading.

Fixes ACME-500.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a `CONVENTIONS.md` fixture with trailing whitespace on a heading triggers the convention to be silently dropped before the fix, and correctly included after the fix
- [ ] The convention heading extraction in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` strips trailing whitespace from extracted section names
- [ ] Conventions with trailing whitespace on headings are correctly matched and included in generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create an eval fixture `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run the convention conformance analysis, and assert that the convention appears in the generated task's Implementation Notes. This test must fail before the fix and pass after
- [ ] Verify that conventions without trailing whitespace continue to work correctly (no regression)
- [ ] Verify that headings with mixed whitespace patterns (tabs, multiple spaces, leading+trailing) are handled correctly

## Verification Commands
- `python3 -m pytest evals/plan-feature/` -- all plan-feature eval tests pass, including the new reproducer test

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include the Migration Patterns convention reference.
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The convention heading extraction uses `line[3:]` without stripping trailing whitespace, causing exact-match lookups against the extracted section names to fail silently when headings have trailing spaces.
