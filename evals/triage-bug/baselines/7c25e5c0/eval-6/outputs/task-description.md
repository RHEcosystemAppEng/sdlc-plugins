## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading parser to strip trailing whitespace, preventing silent convention drops when CONVENTIONS.md headings contain trailing spaces. Also add a warning log for unmatched convention names to prevent silent failures in the future.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Fix heading extraction to strip trailing whitespace and add warning log for unmatched convention names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- Eval fixture with trailing whitespace on headings to cover this edge case

## Implementation Notes
The heading extraction in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` uses `line[3:]` to extract the section name after `## `. Change this to `line[3:].strip()` to normalize heading names regardless of trailing whitespace.

In the task enrichment section of the same file, add a warning when `convention_name not in discovered_conventions` so that future mismatches are surfaced rather than silently dropped.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings. Create a new fixture that includes trailing whitespace to ensure this edge case is tested.

## Acceptance Criteria
- [ ] Convention headings with trailing whitespace are matched correctly by the plan-feature skill
- [ ] A warning is logged when an expected convention name is not found in discovered conventions
- [ ] Existing conventions without trailing whitespace continue to match correctly (no regression)
- [ ] New eval fixture covers the trailing-whitespace edge case

## Test Requirements
- [ ] Add eval case using a CONVENTIONS.md fixture with trailing whitespace on headings; verify the convention is included in the generated task's Implementation Notes
- [ ] Verify existing plan-feature evals still pass with the `.strip()` change
- [ ] Verify warning log is emitted when a convention name is not found

## Bug Context
- **Bug Key**: ACME-500
- **Steps to Reproduce**:
  1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading (e.g., `## Migration Patterns  `)
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys
  3. Inspect the generated task's Implementation Notes
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace. When a heading has trailing spaces, the extracted key (e.g., `"Migration Patterns  "`) fails exact-match against the clean lookup key (`"Migration Patterns"`), and the match failure is not logged.
