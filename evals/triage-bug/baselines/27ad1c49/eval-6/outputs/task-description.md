## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's CONVENTIONS.md heading extraction to strip trailing whitespace, preventing silent convention drops when heading lines contain trailing spaces. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Add `.strip()` to heading extraction at `section_name = line[3:]` to normalize whitespace in convention dictionary keys

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace.md` -- Eval fixture with trailing whitespace on headings to test the edge case

## Implementation Notes
The bug is in the convention conformance analysis section of plan-feature. The heading extraction code:

```python
section_name = line[3:]
```

must be changed to:

```python
section_name = line[3:].strip()
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) produce the clean key `"Migration Patterns"`, which matches the lookup in the convention-aware task enrichment step:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT include trailing whitespace on headings, so the bug is not caught by current evals. A new fixture file with trailing whitespace headings must be created to serve as the reproducer test input.

The reproducer test should:
1. Use a CONVENTIONS.md fixture where at least one heading has trailing whitespace (e.g., `## Migration Patterns  `)
2. Run the convention extraction logic against this fixture
3. Assert that the convention is found by its clean name (without trailing whitespace)
4. Assert that the convention content appears in the generated task's Implementation Notes

Fixes [ACME-500](https://mock-jira.example.com/browse/ACME-500).

## Acceptance Criteria
- [ ] Reproducer test: an eval test case with a CONVENTIONS.md fixture containing trailing whitespace on headings demonstrates the bug (fails before fix, passes after fix)
- [ ] Heading extraction in plan-feature convention conformance analysis applies `.strip()` to normalize extracted heading text
- [ ] Conventions with trailing whitespace on headings are correctly matched and included in generated task Implementation Notes
- [ ] No regression in existing plan-feature evals and tests

## Test Requirements
- [ ] Reproducer test: create `evals/plan-feature/files/conventions-trailing-whitespace.md` with headings containing trailing spaces (e.g., `## Migration Patterns  `); run plan-feature convention extraction against it; assert the convention is found by clean name and appears in the generated task output
- [ ] Verify that existing conventions without trailing whitespace continue to work (no regression)
- [ ] Verify that headings with various whitespace patterns are handled: trailing spaces, trailing tabs, mixed trailing whitespace

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` preserves trailing whitespace, causing exact-match convention lookup to silently fail when headings have trailing spaces.
