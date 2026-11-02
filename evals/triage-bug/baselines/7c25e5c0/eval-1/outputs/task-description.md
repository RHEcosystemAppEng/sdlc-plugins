<!-- Jira API metadata -->
<!-- jira.create_issue parameters: -->
<!-- project: ACME -->
<!-- issueType: Task -->
<!-- labels: ["ai-generated-jira"] -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature convention lookup to strip trailing whitespace from `CONVENTIONS.md` heading lines during extraction. Currently, `line[3:]` retains trailing spaces, causing exact-match lookups against canonical section names to fail silently. Apply `.strip()` to the extracted heading text so that conventions are matched regardless of trailing whitespace in the source file.

## Bug Context

- **Bug**: ACME-500 -- plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Steps to Reproduce**:
  1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading (e.g., `## Migration Patterns  `).
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
  3. Inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Section Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: Heading extraction uses `line[3:]` without stripping trailing whitespace. The extracted key `"Migration Patterns  "` does not match the canonical lookup key `"Migration Patterns"`, so the convention is silently skipped.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- fix heading extraction in convention conformance analysis to strip trailing whitespace

## Implementation Notes
The convention lookup in the plan-feature skill extracts headings with `section_name = line[3:]`. Change this to `section_name = line[3:].strip()` to normalize whitespace. The fix is in the convention conformance analysis section of the skill. The convention matching code (`if convention_name in discovered_conventions`) does not need changes -- it will work correctly once the keys are properly stripped. Consider adding a warning log when the raw heading text differs from the stripped version, to help users identify formatting issues in their `CONVENTIONS.md`.

## Acceptance Criteria
- [ ] Reproducer test: a test with trailing whitespace on a `CONVENTIONS.md` heading confirms the convention is matched and included in the generated task description
- [ ] `line[3:]` is replaced with `line[3:].strip()` in the convention heading extraction
- [ ] Conventions with trailing whitespace on headings are correctly included in generated task Implementation Notes
- [ ] No regression in existing convention matching for headings without trailing whitespace

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  `) and assert the convention is discovered and matched correctly
- [ ] Test that generated task description includes the expected Implementation Notes reference for a convention with trailing-whitespace heading
- [ ] Test that existing conventions without trailing whitespace continue to match correctly (regression guard)

## Verification Commands
- `python -m pytest evals/plan-feature/ -v` -- all plan-feature eval tests pass including the new reproducer test
