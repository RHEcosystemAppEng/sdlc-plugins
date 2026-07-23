## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from `CONVENTIONS.md` headings during extraction. Currently, headings with trailing spaces (e.g., `## Migration Patterns  `) are stored with whitespace intact, causing exact-match convention lookups to fail silently. This results in conventions being dropped from generated task descriptions with no warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Add `.strip()` to heading extraction line to normalize section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- Test fixture with trailing whitespace on convention headings

## Implementation Notes
The root cause is in the convention conformance analysis section of plan-feature. The heading extraction code:

```python
section_name = line[3:]
```

must be changed to:

```python
section_name = line[3:].strip()
```

This normalizes the extracted heading text by removing leading and trailing whitespace before using it as a dictionary key.

The convention-aware task enrichment step performs an exact-match lookup:

```python
if convention_name in discovered_conventions:
```

This lookup will succeed after the extraction fix because the dictionary keys will no longer contain trailing whitespace.

**Existing patterns to follow**:
- The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` provides the pattern for convention test fixtures. The new fixture should mirror its structure but include trailing whitespace on heading lines.
- The convention conformance analysis code path is in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` under the convention heading extraction section.

**Reproducer test guidance**:
- Create a `CONVENTIONS.md` fixture where at least one heading has trailing spaces: `## Migration Patterns  ` (with 2+ trailing spaces after the heading text).
- Run the convention extraction logic against this fixture.
- Assert that the convention `"Migration Patterns"` (without trailing whitespace) is present in the extracted conventions dictionary.
- Assert that the generated task output includes the expected reference: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

## Acceptance Criteria
- [ ] A reproducer test demonstrates that `CONVENTIONS.md` headings with trailing whitespace are correctly matched: the test fails before the fix (convention silently dropped) and passes after the fix (convention included in output)
- [ ] The heading extraction in convention conformance analysis strips trailing whitespace from extracted section names using `.strip()`
- [ ] Conventions with trailing whitespace on headings are included in generated task Implementation Notes, matching the expected format: `Per CONVENTIONS.md <section>: <action>`
- [ ] No regression in existing plan-feature tests and evals

## Test Requirements
- [ ] Reproducer test: Create a conventions fixture with trailing whitespace on heading lines (e.g., `## Migration Patterns  `). Run convention conformance analysis and assert the convention is extracted with the canonical name `"Migration Patterns"` (no trailing whitespace). Assert the generated task includes `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- [ ] Edge case test: Verify headings with mixed whitespace (tabs, multiple spaces) are also normalized correctly
- [ ] Regression test: Verify that headings without trailing whitespace continue to work correctly (existing fixture `evals/plan-feature/files/conventions-mock.md` should still pass)

## Verification Commands
- `python3 -m pytest evals/plan-feature/ -v` -- All plan-feature eval tests pass, including the new trailing-whitespace reproducer

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction code `section_name = line[3:]` does not strip trailing whitespace. When the heading line has trailing spaces, the extracted section name includes them, causing exact-match lookups against canonical convention names to fail silently.
