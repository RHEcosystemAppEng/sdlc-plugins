## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature convention parser to strip trailing whitespace from CONVENTIONS.md
section headings, preventing silent convention drops when heading lines contain trailing
spaces. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- strip trailing whitespace from heading extraction (`line[3:]` -> `line[3:].strip()`) and optionally normalize the lookup key at the matching site

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- eval fixture with trailing whitespace on headings to cover this edge case

## Implementation Notes
The bug is in the convention heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.

**Current buggy code (heading extraction):**
```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Does NOT strip trailing whitespace
        conventions[section_name] = current_section_content
```

**Fix:** Change `line[3:]` to `line[3:].strip()` to normalize heading text.

**Current buggy code (convention matching):**
```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Defense in depth (optional):** Also strip the lookup key: `convention_name.strip()`.

**Warning for silent failures:** Consider adding a log or warning when an expected convention
name is not found in `discovered_conventions`, to prevent future silent drops.

**Existing test pattern:** The existing eval fixture at `evals/plan-feature/files/conventions-mock.md`
does not include trailing whitespace on headings. Create a new fixture that includes trailing
whitespace to test this edge case.

**Reproducer test guidance:**
- Input: a CONVENTIONS.md with `## Migration Patterns  ` (trailing spaces on the heading)
- Trigger: convention parsing and matching for a feature referencing Migration Patterns
- Expected (before fix): the convention is silently dropped, no reference in Implementation Notes
- Expected (after fix): Implementation Notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test: a test using a CONVENTIONS.md fixture with trailing whitespace on heading lines demonstrates the convention is correctly matched and included in the generated task's Implementation Notes (test fails before fix, passes after fix)
- [ ] Heading extraction strips trailing whitespace from CONVENTIONS.md section headings so that `## Migration Patterns  ` is parsed as `"Migration Patterns"`
- [ ] Convention matching succeeds for headings with trailing whitespace, and the generated task's Implementation Notes include the convention reference (e.g., `Per CONVENTIONS.md Migration Patterns: ...`)
- [ ] Headings without trailing whitespace continue to work correctly (no regression)
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  `), run the convention parsing logic, and assert the convention is discovered and matched correctly. The test should assert the generated Implementation Notes include the expected convention reference. This test must fail before the fix and pass after.
- [ ] Regression test: verify that headings without trailing whitespace (the normal case) continue to be parsed and matched correctly using the existing `evals/plan-feature/files/conventions-mock.md` fixture
- [ ] Edge case test: verify handling of headings with mixed whitespace (tabs, multiple spaces, leading/trailing)

## Verification Commands
- Run plan-feature eval suite to confirm no regressions and new trailing-whitespace test passes

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, causing the exact-match convention lookup to fail silently when CONVENTIONS.md headings have trailing spaces.
