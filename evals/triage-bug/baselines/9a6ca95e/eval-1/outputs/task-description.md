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
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace, preventing silent convention drops when `CONVENTIONS.md` headings have trailing spaces. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to convention heading extraction to normalize trailing whitespace

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- test fixture with trailing whitespace on convention headings

## Implementation Notes
The bug is in the convention heading extraction logic within the plan-feature skill. The current code extracts section names with:

```python
section_name = line[3:]
```

This preserves any trailing whitespace from the heading line. Change to:

```python
section_name = line[3:].strip()
```

The reproducer test should create a `CONVENTIONS.md` fixture with trailing whitespace on headings and verify the conventions are still matched. Specifically:

- **Triggering input**: A `CONVENTIONS.md` file where at least one heading has trailing spaces, e.g., `## Migration Patterns  ` (two trailing spaces after "Patterns").
- **Incorrect behavior (before fix)**: The convention is silently dropped -- the generated task's Implementation Notes do NOT include a reference to the Migration Patterns convention.
- **Correct behavior (after fix)**: The convention is matched and included -- the generated task's Implementation Notes include: `Per CONVENTIONS.md "Migration Patterns": add Index::create() for all FK columns.`

Relevant existing code and patterns:
- Convention extraction: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (the `for line in conventions_content.split('\n')` loop)
- Convention matching: same file, the `if convention_name in discovered_conventions` check
- Existing test fixture (without trailing whitespace): `evals/plan-feature/files/conventions-mock.md`

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing convention fixture to use as a base for the trailing-whitespace variant

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a `CONVENTIONS.md` with trailing whitespace on a heading causes the convention to be silently dropped (fails before fix, passes after fix)
- [ ] Convention heading extraction strips trailing whitespace so that headings with trailing spaces are matched correctly
- [ ] No warning is silently swallowed -- if a convention referenced during enrichment is not found, consider logging a diagnostic warning
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  `), run convention extraction and matching, and assert the convention is included in the generated task output. This test must fail before the fix and pass after
- [ ] Verify that existing conventions without trailing whitespace continue to be matched correctly (no regression)
- [ ] Edge case: headings with mixed whitespace (tabs, multiple spaces) are also handled

## Verification Commands
- `pytest evals/plan-feature/` -- all plan-feature evals pass, including the new trailing-whitespace reproducer

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring database migration with foreign keys, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include the Migration Patterns convention reference.
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: Convention heading extraction uses `line[3:]` without `.strip()`, preserving trailing whitespace in the dictionary key. Downstream exact-match lookup against the clean convention name fails silently.
