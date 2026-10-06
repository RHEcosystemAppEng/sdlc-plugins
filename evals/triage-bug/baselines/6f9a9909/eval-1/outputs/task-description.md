<!-- Jira API metadata: jira.create_issue -->
<!-- project: ACME -->
<!-- issue_type: Task -->
<!-- labels: ["ai-generated-jira", "bug-fix"] -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature convention lookup to strip trailing whitespace from `CONVENTIONS.md` heading lines, so that conventions are correctly matched and included in generated task descriptions regardless of trailing whitespace in the source file.

Currently, the heading extraction expression `line[3:]` preserves trailing whitespace, causing exact-match lookups to silently fail when headings have trailing spaces. This results in conventions being dropped from generated tasks without any warning.

## Bug Context
- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500) -- plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Steps to Reproduce**:
  1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading (e.g., `## Migration Patterns  ` with trailing spaces).
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
  3. Inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction in plan-feature convention lookup uses `line[3:]` which does not strip trailing whitespace. Headings like `## Migration Patterns  ` are stored as `"Migration Patterns  "` (with trailing spaces), causing exact-match comparison to fail during convention-aware task enrichment.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- fix heading extraction to strip trailing whitespace from convention section names

## Acceptance Criteria
- [ ] Reproducer test: a test with a `CONVENTIONS.md` fixture containing trailing whitespace on heading lines confirms the convention is correctly matched and included in the generated task output
- [ ] Heading extraction strips trailing whitespace from `CONVENTIONS.md` section names (e.g., `line[3:].strip()` or equivalent)
- [ ] Conventions with trailing whitespace on headings are no longer silently dropped
- [ ] Existing convention lookups (headings without trailing whitespace) continue to work correctly

## Test Requirements
- [ ] Reproducer test: create or extend a plan-feature eval with a `CONVENTIONS.md` fixture that includes trailing whitespace on at least one heading (e.g., `## Migration Patterns  ` with trailing spaces); assert that the generated task's Implementation Notes contain the expected convention reference (`Per CONVENTIONS.md Migration Patterns:`)
- [ ] Regression test: verify that convention headings without trailing whitespace continue to match correctly
- [ ] Edge case test: verify headings with mixed trailing whitespace (spaces, tabs) are handled

## Implementation Notes
The fix is in the convention heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. Change:

```python
section_name = line[3:]
```

to:

```python
section_name = line[3:].strip()
```

This ensures that any trailing whitespace (spaces, tabs) is removed from the extracted heading name before it is used as a dictionary key, making the exact-match comparison in the convention-aware task enrichment step resilient to whitespace variations in `CONVENTIONS.md`.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not cover this edge case and should be augmented with a fixture that includes trailing whitespace on headings.

## Verification Commands
- `python -m pytest evals/plan-feature/ -k "trailing_whitespace"` -- reproducer test passes, confirming the fix
