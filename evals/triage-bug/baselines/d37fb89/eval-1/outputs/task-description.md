<!-- Jira API Metadata
jira.create_issue parameters:
  project: ACME
  issue_type: Task
  labels:
    - ai-generated-jira
  summary: "Fix trailing whitespace in CONVENTIONS.md heading extraction in plan-feature convention lookup"
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from `CONVENTIONS.md` heading lines during extraction. Currently, headings with trailing spaces (e.g., `## Migration Patterns  `) are stored with whitespace intact, causing silent match failures during convention-aware task enrichment. This results in conventions being silently dropped from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — add `.strip()` to the heading extraction in the convention conformance analysis section to normalize section names

## Implementation Notes
The defect is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction loop currently uses:

```python
section_name = line[3:]
```

This must be changed to:

```python
section_name = line[3:].strip()
```

This ensures that trailing whitespace on `CONVENTIONS.md` heading lines (e.g., `## Migration Patterns  `) is removed before the section name is stored in the conventions dictionary. The convention-aware task enrichment step performs exact-match lookups against these keys, so they must be clean.

**Reproducer guidance**: Create a test fixture `CONVENTIONS.md` with trailing whitespace on a heading line. The reproducer test should:
1. Parse the fixture using the convention heading extraction logic
2. Assert the extracted key is `"Migration Patterns"` (without trailing spaces)
3. Verify the convention-aware task enrichment includes the expected reference `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`

**Existing test patterns**: The `evals/plan-feature/` directory contains existing eval fixtures and patterns. Use `evals/plan-feature/files/conventions-mock.md` as a model for the new fixture, adding trailing whitespace to at least one heading.

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test: a test with a `CONVENTIONS.md` fixture containing trailing whitespace on headings (e.g., `## Migration Patterns  `) demonstrates the bug fails before the fix and passes after the fix
- [ ] Convention headings with trailing whitespace are correctly extracted and matched during plan-feature convention conformance analysis
- [ ] Generated task Implementation Notes include the expected convention reference when `CONVENTIONS.md` headings have trailing whitespace
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  `), run the convention heading extraction, and assert the key is `"Migration Patterns"` (no trailing spaces) and the enrichment output includes `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- [ ] Verify that headings without trailing whitespace continue to work correctly (no regression)
- [ ] Verify that headings with mixed whitespace (tabs, multiple spaces) are also handled correctly

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: The heading extraction uses `line[3:]` without `.strip()`, preserving trailing whitespace in the convention dictionary key. The exact-match lookup then fails because the query key has no trailing whitespace while the stored key does.
