## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from CONVENTIONS.md headings during extraction. Currently, headings with trailing spaces (e.g., `## Migration Patterns  `) produce dictionary keys that fail exact-match lookups during task enrichment, causing conventions to be silently dropped from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the convention heading extraction line (`section_name = line[3:]`) to normalize trailing whitespace

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- eval fixture with trailing whitespace on convention headings to reproduce the bug

## Implementation Notes
The defect is in the convention conformance analysis section of plan-feature. The heading extraction logic at `line[3:]` must be changed to `line[3:].strip()` to normalize trailing whitespace.

The convention heading extraction currently works as follows:
```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

The fix is:
```python
        section_name = line[3:].strip()  # Strip trailing whitespace from heading
```

The downstream exact-match lookup in convention-aware task enrichment (`if convention_name in discovered_conventions`) will then work correctly because both the stored key and lookup key will be normalized.

The new eval fixture should contain at least one convention heading with trailing spaces (2+ spaces after the heading text) to verify the fix handles this edge case. Reference the existing fixture at `evals/plan-feature/files/conventions-mock.md` for the expected format -- the new fixture should follow the same structure but add trailing whitespace.

No CONVENTIONS.md exists at the repository root, so no additional conventions apply.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing convention fixture to use as a template for the new trailing-whitespace fixture

## Acceptance Criteria
- [ ] A reproducer test (eval fixture with trailing-whitespace convention headings) demonstrates the bug fails before the fix and passes after
- [ ] Convention headings with trailing whitespace in CONVENTIONS.md are correctly matched and included in generated task Implementation Notes
- [ ] Convention headings WITHOUT trailing whitespace continue to work correctly (no regression)
- [ ] No existing tests are broken by the change

## Test Requirements
- [ ] Reproducer test: create an eval fixture `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` with a convention heading containing trailing whitespace (e.g., `## Migration Patterns  `). Run plan-feature convention analysis against it and assert that the generated task's Implementation Notes include the convention reference in the format `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.` The test should fail before the fix (convention missing) and pass after (convention present).
- [ ] Regression test: verify that the existing `evals/plan-feature/files/conventions-mock.md` fixture (without trailing whitespace) still produces correct convention references after the fix.

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring database migrations, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The convention heading extraction uses `line[3:]` without stripping trailing whitespace, causing exact-match lookup failures in the task enrichment step when CONVENTIONS.md headings have trailing spaces.
