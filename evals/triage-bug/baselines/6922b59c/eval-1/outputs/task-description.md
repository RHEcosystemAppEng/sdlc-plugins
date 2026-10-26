# Jira API Metadata

```
jira.create_issue parameters:
  project_key: ACME
  issue_type: Task
  labels:
    - ai-generated-jira
  link:
    type: Blocks
    inward_issue: ACME-500
```

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature convention lookup to strip trailing whitespace from `CONVENTIONS.md` heading lines. Currently, `line[3:]` preserves trailing spaces, causing exact-match convention lookups to fail silently when headings have trailing whitespace. The fix is to apply `.strip()` to the extracted heading text so that convention names are normalized before storage and matching.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — fix heading extraction to strip trailing whitespace from `line[3:]`

## Files to Create
- `evals/plan-feature/files/conventions-whitespace-mock.md` — eval fixture with trailing whitespace on headings for reproducer test

## Implementation Notes
The convention heading extraction in plan-feature uses `line[3:]` to extract heading text after `## `. This must be changed to `line[3:].strip()` to normalize whitespace. The downstream exact-match comparison in the convention-aware task enrichment step (`if convention_name in discovered_conventions`) does not need to change — normalizing at extraction time is sufficient.

Reference the existing convention fixture at `evals/plan-feature/files/conventions-mock.md` for the expected format, and create a new fixture that includes trailing whitespace on headings to cover this edge case.

## Acceptance Criteria
- [ ] Reproducer test: a test with trailing whitespace on a CONVENTIONS.md heading (e.g., `## Migration Patterns  `) correctly extracts and matches the convention, producing the expected Implementation Notes reference
- [ ] `line[3:]` in the convention heading extraction is replaced with `line[3:].strip()` (or equivalent) so trailing whitespace is removed
- [ ] Conventions with trailing whitespace on headings are no longer silently dropped
- [ ] Existing conventions without trailing whitespace continue to work correctly (no regression)

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on the heading (`## Migration Patterns  ` with trailing spaces), run the convention lookup, and assert that the section name is `"Migration Patterns"` (without trailing spaces) and that the generated task's Implementation Notes include `Per CONVENTIONS.md §Migration Patterns:`
- [ ] Regression test: verify that existing conventions-mock.md (no trailing whitespace) continues to produce correct convention matches
- [ ] Edge case test: verify headings with mixed whitespace (tabs, multiple spaces) are also normalized

## Verification Commands
- `python -m pytest evals/plan-feature/ -k whitespace` — reproducer test passes

## Bug Context
- **Bug Key**: ACME-500
- **Steps to Reproduce**:
  1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading (e.g., `## Migration Patterns  `)
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys
  3. Inspect the generated task's Implementation Notes
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: The plan-feature convention lookup extracts heading text with `line[3:]`, which does not strip trailing whitespace. This causes exact-match convention lookups to fail silently when `CONVENTIONS.md` headings have trailing spaces.
