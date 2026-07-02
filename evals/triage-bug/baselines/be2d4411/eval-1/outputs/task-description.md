# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix trailing whitespace handling in plan-feature's CONVENTIONS.md heading extraction so that conventions are not silently dropped when heading lines contain trailing spaces. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Add `.strip()` to the heading extraction logic (`section_name = line[3:]`) to normalize trailing whitespace before storing in the conventions dictionary

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — New eval fixture with trailing whitespace on convention headings to cover this edge case

## Implementation Notes
The defect is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction loop currently uses:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

Change this to:

```python
section_name = line[3:].strip()  # Normalize whitespace
```

This ensures that a heading like `## Migration Patterns  ` (with trailing spaces) is stored as `"Migration Patterns"` in the conventions dictionary, matching the downstream exact-match lookup in the convention-aware task enrichment step:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

**Reproducer test guidance**: The reproducer should use a CONVENTIONS.md fixture containing at least one heading with trailing whitespace. The specific scenario from the bug report is:
- **Input**: A `CONVENTIONS.md` with `## Migration Patterns  ` (two trailing spaces on the heading)
- **Trigger**: Running plan-feature convention conformance analysis on a feature that references the "Migration Patterns" convention
- **Incorrect behavior (before fix)**: The generated task's Implementation Notes do NOT include `Per CONVENTIONS.md §Migration Patterns: ...` — the convention is silently dropped
- **Correct behavior (after fix)**: The generated task's Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`

**Existing test reference**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings. Use this file as a pattern reference for creating the new fixture.

Consider also adding a warning log when a convention section name contains leading or trailing whitespace after stripping, to surface similar data quality issues in the future.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — Existing conventions eval fixture; use as a pattern reference for the new trailing-whitespace fixture

## Acceptance Criteria
- [ ] A reproducer test exists that uses a CONVENTIONS.md fixture with trailing whitespace on headings and asserts that the convention is correctly included in generated task output (fails before fix, passes after)
- [ ] The heading extraction logic in plan-feature convention conformance analysis strips trailing whitespace from extracted section names
- [ ] Conventions with trailing whitespace on headings are correctly matched and included in generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create an eval fixture `conventions-trailing-whitespace-mock.md` with a heading like `## Migration Patterns  ` (trailing spaces) and verify that the convention conformance analysis correctly extracts and matches the section name, including the convention in the generated task output
- [ ] Verify that headings without trailing whitespace continue to work as before (no regression)
- [ ] Verify that headings with various whitespace patterns (tabs, multiple spaces, mixed) are handled correctly

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: The heading extraction logic uses `line[3:]` without stripping trailing whitespace, causing exact-match lookups against clean convention names to fail silently.
