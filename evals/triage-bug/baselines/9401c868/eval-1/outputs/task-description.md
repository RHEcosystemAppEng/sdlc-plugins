# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: `["ai-generated-jira"]`

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace
from CONVENTIONS.md heading lines during extraction. Currently, headings with trailing
spaces (e.g., `## Migration Patterns  `) are stored with the whitespace intact, causing
exact-match convention lookups to fail silently. This results in conventions being dropped
from generated task descriptions without any warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to heading extraction in convention lookup logic to normalize trailing whitespace

## Implementation Notes
The defect is in the convention lookup logic within
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction code:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

must be changed to:

```python
section_name = line[3:].strip()  # Normalize trailing whitespace
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) are
stored as `"Migration Patterns"` in the `conventions` dictionary, matching the clean
convention names used in the task enrichment lookup:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

Additionally, consider adding a warning when a CONVENTIONS.md heading is parsed but
cannot be matched, to prevent silent failures in the future.

The reproducer test should:
1. Create a CONVENTIONS.md fixture with trailing whitespace on a heading line
   (e.g., `## Migration Patterns  ` with two trailing spaces after "Patterns").
2. Run the convention conformance analysis against this fixture with a feature
   that should trigger the Migration Patterns convention.
3. Assert the generated task's Implementation Notes include the convention reference
   `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

Use the existing eval fixture at `evals/plan-feature/files/conventions-mock.md` as a
reference for the fixture format. Create a variant with trailing whitespace on headings
for the reproducer test.

Fixes ACME-500.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing convention fixture; duplicate and add trailing whitespace on headings to create the reproducer fixture

## Acceptance Criteria
- [ ] Reproducer test: a test with a CONVENTIONS.md fixture containing trailing whitespace on headings demonstrates the convention is correctly matched (fails before fix, passes after)
- [ ] Convention headings with trailing whitespace are stripped during extraction so that exact-match lookups succeed
- [ ] Conventions from headings with trailing whitespace appear in generated task Implementation Notes
- [ ] No regression in existing plan-feature tests and evals

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  `), run convention conformance analysis against it, and assert the convention is included in the generated task output. This test must fail before the fix and pass after.
- [ ] Verify that headings without trailing whitespace continue to work correctly (no regression)
- [ ] Verify that headings with various whitespace patterns (tabs, mixed spaces) are handled

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The convention is silently dropped from Implementation Notes -- no warning or error shown.
- **Root Cause**: The heading extraction `line[3:]` preserves trailing whitespace, causing exact-match convention lookups to fail silently since the key `"Migration Patterns  "` does not match `"Migration Patterns"`.
