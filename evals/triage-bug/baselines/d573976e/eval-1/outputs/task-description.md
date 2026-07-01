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
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace before
storing section names, so that conventions in `CONVENTIONS.md` files with trailing whitespace on
headings are no longer silently dropped. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — add `.strip()` to heading extraction to normalize trailing whitespace

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — eval fixture with trailing whitespace on convention headings for reproducer test

## Implementation Notes
The defect is in the convention conformance analysis logic within
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction code currently reads:

```python
section_name = line[3:]
```

This should be changed to:

```python
section_name = line[3:].strip()
```

This ensures trailing whitespace (spaces, tabs) on convention heading lines is normalized before
the section name is stored as a dictionary key. The downstream lookup in the convention-aware
task enrichment step uses exact string matching (`if convention_name in discovered_conventions`),
which will then match correctly regardless of trailing whitespace in the source file.

**Reproducer test guidance:**
- Create a `CONVENTIONS.md` fixture with a heading containing trailing spaces, e.g., `## Migration Patterns  ` (two trailing spaces after "Patterns").
- Include convention content under that heading (e.g., `Add Index::create() for all FK columns.`).
- Run the convention conformance analysis against this fixture.
- Assert that the convention name `"Migration Patterns"` (without trailing spaces) is present in the extracted conventions dictionary.
- Assert that the generated task's Implementation Notes include the convention reference (e.g., `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`).

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include
trailing whitespace on headings — use it as a reference for the fixture format, then add trailing
whitespace to create the new reproducer fixture.

Consider also adding a logged warning when trailing whitespace is stripped from a convention heading,
to surface formatting issues to users.

Fixes ACME-500.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing convention fixture format to base the reproducer fixture on

## Acceptance Criteria
- [ ] Reproducer test: a test with a `CONVENTIONS.md` fixture containing trailing whitespace on a heading demonstrates the bug is fixed (fails before fix, passes after)
- [ ] Convention headings with trailing whitespace are correctly matched during convention conformance analysis
- [ ] Conventions with trailing whitespace on headings appear in the generated task's Implementation Notes
- [ ] No regression in existing plan-feature eval tests (conventions without trailing whitespace continue to work)

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with `## Migration Patterns  ` (trailing spaces) and convention content; run convention extraction; assert `"Migration Patterns"` is found as a key and its content is included in the generated output
- [ ] Verify that existing convention headings without trailing whitespace continue to be extracted and matched correctly (no regression)

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: The heading extraction logic uses `line[3:]` without stripping trailing whitespace, causing exact-match convention lookups to fail silently when headings have trailing spaces.
