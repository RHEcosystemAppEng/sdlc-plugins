<!-- Jira API Metadata
jira.create_issue parameters:
  project: ACME
  issue_type: Task
  labels:
    - ai-generated-jira
  summary: "Fix trailing-whitespace heading extraction in plan-feature convention lookup"
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to handle trailing whitespace on CONVENTIONS.md heading lines. Currently, `line[3:]` extracts heading text without stripping whitespace, causing convention matches to fail silently when headings contain trailing spaces. This results in conventions being omitted from generated task descriptions with no warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — fix heading extraction to strip trailing whitespace from `line[3:]`, and add a warning when an expected convention is not matched

## Files to Create
- `evals/plan-feature/files/conventions-trailing-ws-mock.md` — eval fixture with trailing whitespace on heading lines to cover this edge case

## Implementation Notes
The root cause is in the convention lookup section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction logic uses `line[3:]` to get the heading text after `## `, but does not normalize whitespace. Change:

```python
section_name = line[3:]
```

to:

```python
section_name = line[3:].strip()
```

This ensures that headings like `## Migration Patterns  ` are extracted as `"Migration Patterns"` rather than `"Migration Patterns  "`, allowing the exact-match comparison in the task enrichment step to succeed.

Additionally, in the convention-aware task enrichment section, consider adding a diagnostic log when a convention name is expected but not found in `discovered_conventions`. This prevents future silent failures.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings. Create a new fixture (`conventions-trailing-ws-mock.md`) that includes trailing whitespace to cover this edge case.

The reproducer test should:
1. Use a CONVENTIONS.md fixture where a heading has trailing whitespace (e.g., `## Migration Patterns  ` with two trailing spaces).
2. Run the convention extraction logic against this fixture.
3. Assert that the section name is normalized (no trailing whitespace).
4. Assert that the convention match succeeds and the generated task includes `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test: a test using a CONVENTIONS.md fixture with trailing whitespace on headings demonstrates that conventions are correctly extracted and matched (test fails before fix, passes after fix)
- [ ] Heading extraction in convention lookup applies `.strip()` to `line[3:]` so trailing whitespace on CONVENTIONS.md headings does not prevent convention matching
- [ ] Conventions with trailing whitespace on headings are included in generated task Implementation Notes, matching the expected format (`Per CONVENTIONS.md §<section>: <action>`)
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run convention extraction, and assert the section name is `"Migration Patterns"` (not `"Migration Patterns  "`); assert the generated task includes the convention reference `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- [ ] Edge case test: verify headings with mixed whitespace (tabs, multiple spaces) are also normalized correctly
- [ ] Regression test: confirm existing conventions without trailing whitespace continue to be extracted and matched correctly

## Verification Commands
- `python3 -m pytest evals/plan-feature/ -v` — all plan-feature eval tests pass, including the new trailing-whitespace test case

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The convention is silently dropped from the generated task's Implementation Notes. No warning or error is shown.
- **Root Cause**: The heading extraction `line[3:]` in the plan-feature convention lookup does not strip trailing whitespace, causing exact-match comparison to fail when headings have trailing spaces.
