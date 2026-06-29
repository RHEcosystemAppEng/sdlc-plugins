<!-- Jira API Metadata — jira.create_issue parameters -->
<!-- project: ACME -->
<!-- issue_type: Task -->
<!-- labels: ["ai-generated-jira"] -->
<!-- summary: Fix trailing whitespace in CONVENTIONS.md heading extraction (ACME-500) -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace from `CONVENTIONS.md` headings. Currently, `line[3:]` extracts the heading text without calling `.strip()`, causing convention names with trailing spaces to fail exact-match dictionary lookups during task enrichment. This results in conventions being silently dropped from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Fix heading extraction to strip trailing whitespace from section names

## Implementation Notes
The bug is in the convention heading extraction loop in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code:

```python
section_name = line[3:]  # Does not strip trailing whitespace
```

Must be changed to:

```python
section_name = line[3:].strip()  # Strips trailing (and leading) whitespace
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) are stored as `"Migration Patterns"` in the conventions dictionary, matching the clean convention names used during task enrichment lookups.

The convention-to-task matching logic (`if convention_name in discovered_conventions`) does not need modification — the fix is entirely in the extraction step.

**Reproducer test guidance**: Create a test fixture `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  ` with 2+ trailing spaces). Run the convention extraction and verify the section name is `"Migration Patterns"` (stripped). Then verify the task enrichment step includes the expected `Per CONVENTIONS.md §Migration Patterns: ...` reference in the output.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not cover this edge case and should be referenced as a pattern for the new test fixture.

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test: a test with a CONVENTIONS.md fixture containing trailing whitespace on headings (e.g., `## Migration Patterns  `) demonstrates that convention extraction correctly strips whitespace and the convention is included in the generated task output (test fails before fix, passes after)
- [ ] Convention heading extraction uses `.strip()` on `line[3:]` to normalize section names
- [ ] Conventions with trailing whitespace on headings are matched and included in generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on a `## ` heading line; assert that the extracted section name equals the clean heading text (no trailing spaces) and that the convention appears in the generated task output with the correct `Per CONVENTIONS.md §<section>: ...` format
- [ ] Edge case test: verify headings with mixed whitespace (tabs, multiple spaces) are also handled correctly
- [ ] Regression test: verify that headings without trailing whitespace continue to work as before

## Verification Commands
- `pytest evals/plan-feature/` — all existing and new plan-feature eval tests pass

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: The heading extraction code `line[3:]` does not call `.strip()`, so trailing whitespace on CONVENTIONS.md headings causes section names to be stored with trailing spaces, failing exact-match dictionary lookups during convention-to-task enrichment.
