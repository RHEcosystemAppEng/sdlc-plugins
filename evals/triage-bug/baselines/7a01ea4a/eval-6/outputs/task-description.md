## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace, preventing silent convention drops when CONVENTIONS.md headings contain trailing spaces. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Add `.strip()` to the heading extraction logic (`line[3:]`) in the convention conformance analysis section to normalize whitespace on extracted section names.

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- New eval fixture with trailing whitespace on heading lines to exercise the edge case.

## Implementation Notes
The root cause is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction logic:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

must be changed to:

```python
section_name = line[3:].strip()  # Strips trailing whitespace
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) produce the key `"Migration Patterns"` rather than `"Migration Patterns  "`, allowing the downstream exact-match lookup (`convention_name in discovered_conventions`) to succeed.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not cover this edge case. Create a new fixture `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` that includes headings with trailing whitespace (spaces and/or tabs) to serve as the reproducer test input.

The reproducer test should:
1. Use a CONVENTIONS.md with trailing whitespace on the `## Migration Patterns  ` heading.
2. Run convention conformance analysis against a feature requiring database migration with foreign keys.
3. Assert that the generated task's Implementation Notes include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
4. Verify no convention is silently dropped -- all matching conventions must appear in the output.

Fixes ACME-500.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- Existing convention eval fixture; use as a base for creating the trailing-whitespace variant.

## Acceptance Criteria
- [ ] Reproducer test: a test using a CONVENTIONS.md fixture with trailing whitespace on headings demonstrates that conventions are correctly matched and included in the generated task (fails before fix, passes after fix).
- [ ] The heading extraction logic in the convention conformance analysis strips trailing whitespace from extracted section names using `.strip()`.
- [ ] Conventions with trailing whitespace on headings in CONVENTIONS.md are correctly matched and included in generated task Implementation Notes.
- [ ] No regression in existing plan-feature convention conformance tests (existing fixtures without trailing whitespace continue to work).

## Test Requirements
- [ ] Reproducer test: Create a CONVENTIONS.md fixture with trailing whitespace on heading lines (e.g., `## Migration Patterns  ` with trailing spaces). Run convention conformance analysis and assert the convention reference (`Per CONVENTIONS.md Migration Patterns: ...`) appears in the generated task's Implementation Notes. This test must fail before the fix and pass after.
- [ ] Edge case: Test headings with multiple types of trailing whitespace (spaces, tabs, mixed) to ensure `.strip()` handles all variants.
- [ ] Regression: Verify that existing CONVENTIONS.md fixtures without trailing whitespace continue to produce correct convention references.

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: 1. Create CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `). 2. Run `/plan-feature ACME-100` on a feature requiring DB migration with FK columns. 3. Inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes include the convention reference: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction logic `section_name = line[3:]` does not strip trailing whitespace, causing exact-match lookups against the convention dictionary to fail silently when headings have trailing spaces.
