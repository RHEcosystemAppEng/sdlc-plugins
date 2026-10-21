<!-- Jira API Metadata Block -->
<!-- jira.create_issue parameters: -->
<!-- project: ACME -->
<!-- issue_type: Task -->
<!-- labels: ["ai-generated-jira"] -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix trailing whitespace handling in plan-feature convention heading extraction.
When `CONVENTIONS.md` contains trailing whitespace on `## ` heading lines, the
plan-feature skill silently drops the convention because `line[3:]` does not strip
whitespace, causing exact-match dictionary lookups to fail. Apply `.strip()` to
the extracted section name so that conventions are matched regardless of trailing
whitespace in the source file. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- fix heading extraction to strip trailing whitespace from `line[3:]`

## Implementation Notes
The bug is in the convention conformance analysis section of the plan-feature skill.
The heading extraction code currently reads:

```python
section_name = line[3:]  # Extracts heading text after "## "
```

This must be changed to:

```python
section_name = line[3:].strip()
```

This single change normalizes the dictionary key at extraction time, so the
downstream exact-match lookup (`convention_name in discovered_conventions`) will
succeed regardless of trailing whitespace in the CONVENTIONS.md source file.

The downstream matching code does not need modification:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Existing test patterns**: The eval fixture at `evals/plan-feature/files/conventions-mock.md`
currently does NOT include trailing whitespace on headings. The reproducer test should
create a new fixture (or extend the existing one) that includes trailing whitespace
on at least one heading to cover this edge case.

**Reproducer test guidance** (derived from Steps to Reproduce):
- **Input**: A CONVENTIONS.md with `## Migration Patterns  ` (trailing spaces on heading)
- **Incorrect behavior** (before fix): The extracted section name is `"Migration Patterns  "`,
  and the convention is silently dropped from the generated task's Implementation Notes
- **Correct behavior** (after fix): The extracted section name is `"Migration Patterns"`,
  and the generated task's Implementation Notes include
  `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

## Acceptance Criteria
- [ ] Reproducer test: a test with a CONVENTIONS.md fixture containing trailing whitespace on a `## ` heading demonstrates that the convention is correctly matched and included in the generated task output (test fails before fix, passes after)
- [ ] The heading extraction code applies `.strip()` to the section name extracted from `line[3:]`
- [ ] Conventions with trailing whitespace on headings are no longer silently dropped
- [ ] Conventions without trailing whitespace continue to work correctly (no regression)
- [ ] No regression in existing plan-feature evals

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on at least one `## ` heading (e.g., `## Migration Patterns  `), run the convention extraction logic, and assert that (a) the extracted section name equals `"Migration Patterns"` without trailing whitespace, and (b) the convention-aware task enrichment includes the expected `Per CONVENTIONS.md` reference in Implementation Notes
- [ ] Regression test: verify that headings without trailing whitespace continue to be extracted and matched correctly
- [ ] Edge case test: verify handling of headings with mixed whitespace (tabs, multiple spaces)

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction code `line[3:]` does not strip trailing whitespace, producing a dictionary key like `"Migration Patterns  "` that fails exact-match lookup against the expected `"Migration Patterns"`.
