## Repository
acme-backend

## Target Branch
main

## Description
Fix trailing whitespace handling in plan-feature convention heading extraction. When `CONVENTIONS.md` headings have trailing whitespace (e.g., `## Migration Patterns  `), the plan-feature skill silently drops the convention because the extracted section name retains trailing spaces, causing exact-match lookups to fail. Apply `.strip()` to normalize heading text during extraction. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the heading extraction logic (`section_name = line[3:]` becomes `section_name = line[3:].strip()`)

## Files to Create
- `evals/plan-feature/files/conventions-trailing-ws-mock.md` -- eval fixture with trailing whitespace on convention headings for the reproducer test

## Implementation Notes
The defect is in the convention heading extraction loop in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

The fix is to apply `.strip()` to normalize the extracted section name:

```python
section_name = line[3:].strip()
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) are stored under the key `"Migration Patterns"`, matching the expected lookup key in the convention-aware task enrichment step.

The downstream matching logic (`convention_name in discovered_conventions`) does not need changes -- once the keys are normalized at extraction time, exact matching works correctly.

**Reproducer test guidance:**

Create a test fixture `evals/plan-feature/files/conventions-trailing-ws-mock.md` with content:
```
## Migration Patterns  
Add Index::create() for all FK columns.
```
(Note: the heading has two trailing spaces after "Patterns")

The reproducer test should:
1. Feed this fixture through the convention extraction logic
2. Assert that looking up `"Migration Patterns"` (without trailing whitespace) finds the convention
3. Assert that the generated task's Implementation Notes include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

**Existing test reference:** The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not cover trailing whitespace -- it serves as a baseline for normal (clean) heading behavior.

No CONVENTIONS.md exists at the repository root, so no repository-specific conventions apply to this task.

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test: a test with a `CONVENTIONS.md` fixture containing trailing whitespace on headings demonstrates the bug (fails before fix, passes after fix)
- [ ] Convention heading extraction strips trailing whitespace from section names so that `## Migration Patterns  ` is stored as `"Migration Patterns"`
- [ ] Convention-aware task enrichment correctly includes conventions whose headings had trailing whitespace in the source file
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create `evals/plan-feature/files/conventions-trailing-ws-mock.md` with trailing whitespace on headings; assert that the convention extraction returns the section under its trimmed name and that the generated task references the convention correctly
- [ ] Verify that existing eval fixtures without trailing whitespace continue to work correctly (no regression)

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes
- **Expected Result**: The generated task's Implementation Notes should include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The convention is silently dropped -- no reference appears in Implementation Notes, no warning or error is shown
- **Root Cause**: The heading extraction logic uses `line[3:]` without stripping trailing whitespace, causing exact-match lookup to fail silently when the stored key has trailing spaces
