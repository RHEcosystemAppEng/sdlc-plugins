## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace, preventing silent convention drops when `CONVENTIONS.md` headings have trailing spaces. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- strip trailing whitespace from extracted heading text in the convention parsing loop

## Implementation Notes
The convention heading extraction loop in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` parses `CONVENTIONS.md` headings using `section_name = line[3:]`. This raw slice preserves any trailing whitespace on the heading line. When a heading is written as `## Migration Patterns  ` (with trailing spaces), the dictionary key becomes `"Migration Patterns  "`, which fails the downstream exact match `if convention_name in discovered_conventions` against the expected key `"Migration Patterns"`.

**Fix approach:**

1. Apply `.strip()` to the heading extraction: change `section_name = line[3:]` to `section_name = line[3:].strip()`.
2. Add a warning log when the stripped value differs from the raw value, to surface whitespace issues in convention files for authors.
3. Consider also stripping the lookup key in the task enrichment step for defense in depth.

**Reproducer test guidance:**

- Create a test fixture `CONVENTIONS.md` with at least one heading that has trailing whitespace: `## Migration Patterns  ` (two trailing spaces).
- Include a convention body under the heading (e.g., `Add Index::create() for all FK columns.`).
- Run the convention extraction function against this fixture.
- Assert that the extracted convention key is `"Migration Patterns"` (no trailing whitespace).
- Assert that the task enrichment step successfully matches and includes the convention in Implementation Notes.
- Before the fix, the assertion on the extracted key will fail (it will be `"Migration Patterns  "`). After the fix, it will pass.

**Existing test patterns:** The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace. The new reproducer test should add a separate fixture or extend the existing one.

Fixes [ACME-500](https://mock-jira.example.com/browse/ACME-500).

## Acceptance Criteria
- [ ] Reproducer test: a test with a `CONVENTIONS.md` fixture containing trailing whitespace on headings demonstrates the bug (fails before fix, passes after fix)
- [ ] Convention heading extraction strips trailing whitespace from heading text so that conventions with trailing spaces are matched correctly
- [ ] A warning is logged when whitespace normalization is applied to a heading
- [ ] No regression in existing plan-feature tests and evals

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with heading `## Migration Patterns  ` (trailing whitespace). Run convention extraction and assert the key is `"Migration Patterns"` (stripped). Assert task enrichment includes the convention reference in Implementation Notes. This test must fail before the fix and pass after.
- [ ] Test that headings without trailing whitespace continue to work correctly (no regression)
- [ ] Test that headings with various whitespace patterns (tabs, mixed spaces, leading whitespace after `## `) are handled gracefully

## Verification Commands
- `python -m pytest evals/plan-feature/ -v` -- existing plan-feature evals should pass (no regression)

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring the convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include the convention reference: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, producing a key like `"Migration Patterns  "` that fails exact-match lookup against `"Migration Patterns"`. The failure is silent with no warning logged.
