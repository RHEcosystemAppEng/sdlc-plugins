# Jira API Metadata

The following parameters would be passed to `jira.create_issue`:

- **Project**: ACME
- **Issue Type**: Task
- **Labels**: `["ai-generated-jira"]`

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the convention heading extraction in plan-feature to strip trailing whitespace. Currently, `line[3:]` preserves trailing whitespace from CONVENTIONS.md headings, causing exact-match lookups to silently fail and drop conventions from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Fix heading extraction to strip trailing whitespace in convention conformance analysis

## Implementation Notes
The convention conformance analysis in plan-feature extracts headings with `section_name = line[3:]`, which preserves trailing whitespace. When a CONVENTIONS.md heading is `## Migration Patterns  ` (with trailing spaces), the extracted key becomes `"Migration Patterns  "` instead of `"Migration Patterns"`. The downstream exact-match lookup `if convention_name in discovered_conventions` then fails silently.

The fix is to add `.strip()` to the heading extraction: `section_name = line[3:].strip()`.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings and should be extended with a trailing-whitespace variant for the reproducer test.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a CONVENTIONS.md heading with trailing whitespace is correctly matched after the fix (the test fails before the fix and passes after)
- [ ] The heading extraction in plan-feature's convention conformance analysis strips trailing whitespace from extracted section names
- [ ] Conventions with trailing whitespace on headings are included in generated task Implementation Notes
- [ ] No regression in existing plan-feature evals or tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on a heading (e.g., `## Migration Patterns  ` with trailing spaces), run the convention extraction and lookup logic, and assert that the convention name `"Migration Patterns"` is found in the extracted conventions dictionary and that the generated Implementation Notes contain the convention reference `Per CONVENTIONS.md`. The test must fail before the fix (convention not found due to trailing whitespace mismatch) and pass after (convention correctly matched).
- [ ] Verify that headings without trailing whitespace continue to work as expected (regression guard)

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature` on a feature requiring that convention, inspect the generated task's Implementation Notes
- **Expected Result**: Implementation Notes should include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: Implementation Notes do NOT reference the Migration Patterns convention — silently dropped
- **Root Cause**: Heading extraction `line[3:]` does not strip trailing whitespace, causing exact-match lookup failure in convention-aware task enrichment
