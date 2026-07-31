# Generated Task: Fix plan-feature convention heading extraction to strip trailing whitespace

**Jira Issue Type**: Task
**Labels**: ai-generated-jira
**Link**: Blocks ACME-500 (Bug-to-Task link type: Blocks)

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from CONVENTIONS.md heading lines during extraction. Currently, `line[3:]` preserves trailing spaces, causing exact-match lookups to fail silently and drop conventions from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Add `.strip()` to heading extraction in convention conformance analysis to normalize whitespace on parsed section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- Test fixture with trailing whitespace on heading lines for reproducer test

## Implementation Notes
The bug is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction logic:

```python
section_name = line[3:]  # BUG: does not strip trailing whitespace
```

must be changed to:

```python
section_name = line[3:].strip()  # FIX: normalize trailing whitespace
```

This single change ensures that heading lines with trailing spaces (e.g., `## Migration Patterns  `) produce clean dictionary keys (`"Migration Patterns"`) that match the downstream lookup in the convention-aware task enrichment step:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT cover trailing whitespace. Create a new fixture (`conventions-trailing-whitespace-mock.md`) with trailing spaces on at least one heading to serve as the reproducer test input.

Optionally, add a diagnostic warning when the stripped name differs from the raw extraction, to surface malformed CONVENTIONS.md files to users.

Fixes ACME-500.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- Existing conventions fixture; use as a reference for the new trailing-whitespace fixture format

## Acceptance Criteria
- [ ] Reproducer test: A test using a CONVENTIONS.md fixture with trailing whitespace on headings (e.g., `## Migration Patterns  `) demonstrates that the convention is silently dropped before the fix (test fails) and correctly included after the fix (test passes)
- [ ] The heading extraction in convention conformance analysis strips trailing whitespace from section names using `.strip()`
- [ ] Conventions without trailing whitespace continue to be matched correctly (no regression)
- [ ] No existing tests are broken by the change

## Test Requirements
- [ ] Reproducer test: Create a CONVENTIONS.md fixture with trailing whitespace on heading lines (at least 2 trailing spaces on `## Migration Patterns  `). Run the convention conformance analysis against this fixture and assert that the generated task's Implementation Notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.` -- this assertion must fail before the fix and pass after
- [ ] Regression test: Verify that the existing `evals/plan-feature/files/conventions-mock.md` fixture (without trailing whitespace) continues to produce correct convention matches after the fix
- [ ] Edge case test: Verify that headings with only whitespace after `## ` (e.g., `##    `) are handled gracefully (empty section name should be skipped or flagged)

## Verification Commands
- Run plan-feature eval suite to confirm no regressions in convention matching

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes
- **Expected Result**: The generated task's Implementation Notes should include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` in the convention conformance analysis does not strip trailing whitespace, causing exact-match lookups against clean convention names to fail silently
