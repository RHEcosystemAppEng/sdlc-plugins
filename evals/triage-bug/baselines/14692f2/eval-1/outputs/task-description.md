<!-- Jira API metadata
project: ACME
issueType: Task
labels: ["ai-generated-jira"]
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix trailing whitespace handling in plan-feature convention heading extraction. The `line[3:]` slice preserves trailing whitespace from `CONVENTIONS.md` headings, causing exact-match convention lookups to fail silently. Apply `.strip()` to normalize extracted heading names. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — fix heading extraction to strip trailing whitespace from convention section names

## Implementation Notes
The plan-feature skill's convention conformance analysis parses `CONVENTIONS.md` headings with `section_name = line[3:]`. This does not strip trailing whitespace, so a heading like `## Migration Patterns  ` produces the key `"Migration Patterns  "` instead of `"Migration Patterns"`. The downstream exact-match lookup `convention_name in discovered_conventions` then fails silently.

**Fix**: Change the heading extraction to `section_name = line[3:].strip()` so that trailing whitespace (spaces, tabs, carriage returns) is removed at the point of extraction.

**Reproducer test guidance**: Create a `CONVENTIONS.md` fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  ` with two trailing spaces after "Patterns"). Run the plan-feature convention lookup against this fixture. The test should:
- Assert that the convention name `"Migration Patterns"` is found in the extracted conventions dictionary
- Assert that the generated task's Implementation Notes contain a reference matching `Per CONVENTIONS.md §Migration Patterns:`

Before the fix, these assertions will fail (the key will be `"Migration Patterns  "` and the convention will be silently dropped). After the fix, both assertions will pass.

**Existing test reference**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings. The reproducer should create a new fixture or modify the existing one to include trailing whitespace variants.

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test demonstrates the bug: creates a CONVENTIONS.md fixture with trailing whitespace on headings, runs plan-feature convention lookup, and fails before the fix is applied (convention silently dropped)
- [ ] Convention heading extraction applies `.strip()` to `line[3:]` so trailing whitespace is removed
- [ ] Conventions with trailing whitespace on headings are correctly matched and included in generated task Implementation Notes
- [ ] No regression in existing plan-feature evals and tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  `), run the convention lookup, and assert: (1) convention name `"Migration Patterns"` is found in extracted conventions, (2) generated Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns:` reference
- [ ] Regression tests: verify that existing conventions without trailing whitespace continue to be parsed and matched correctly
- [ ] Edge cases: test headings with tabs, mixed whitespace, and carriage returns as trailing characters

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create CONVENTIONS.md with trailing whitespace on heading (`## Migration Patterns  `), run `/plan-feature ACME-100` on a migration feature, inspect generated task Implementation Notes
- **Expected Result**: Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: Implementation Notes do NOT reference the Migration Patterns convention; convention silently dropped with no warning
- **Root Cause**: Heading extraction uses `line[3:]` without stripping trailing whitespace, causing exact-match convention lookups to fail silently
