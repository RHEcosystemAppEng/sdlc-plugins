# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from CONVENTIONS.md heading lines before storing them in the conventions dictionary. Currently, headings with trailing whitespace (e.g., `## Migration Patterns  `) are stored with the whitespace intact, causing exact-match lookups to silently fail and drop the convention from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- strip trailing whitespace in heading extraction logic (`line[3:]` to `line[3:].strip()`)

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- eval fixture with trailing whitespace on convention headings for reproducer test

## Implementation Notes
The defect is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction logic currently reads:

```python
section_name = line[3:]
```

This must be changed to:

```python
section_name = line[3:].strip()
```

This ensures that trailing whitespace on CONVENTIONS.md heading lines is normalized before the section name is stored in the `conventions` dictionary. The downstream exact-match lookup (`convention_name in discovered_conventions`) will then match correctly regardless of trailing whitespace in the source file.

Additionally, consider adding a warning when a convention name referenced during task enrichment is not found in `discovered_conventions`, to prevent silent failures in the future.

The reproducer test should use a CONVENTIONS.md fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  `) and verify that the convention is included in the generated task's Implementation Notes. The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` can be used as a reference for the fixture format.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing conventions eval fixture; use as a base for the trailing-whitespace variant

## Acceptance Criteria
- [ ] A reproducer test exists that uses a CONVENTIONS.md fixture with trailing whitespace on heading lines, demonstrates the convention is silently dropped before the fix, and passes after the fix
- [ ] Heading extraction in the convention conformance analysis strips trailing whitespace (e.g., `line[3:].strip()`)
- [ ] Conventions with trailing whitespace on headings are correctly included in generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create an eval fixture `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` with `## Migration Patterns  ` (trailing spaces on heading). Run the convention conformance analysis against it and assert the generated task's Implementation Notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.` The test must fail before the fix and pass after.
- [ ] Verify existing conventions eval (without trailing whitespace) still passes unchanged
- [ ] Verify that a CONVENTIONS.md with mixed headings (some with trailing whitespace, some without) correctly includes all conventions

## Verification Commands
- Run plan-feature evals against the new trailing-whitespace fixture and verify the convention appears in the output

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a DB migration with foreign keys, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: Heading extraction uses `line[3:]` without `.strip()`, preserving trailing whitespace. The subsequent exact-match convention lookup fails silently because the stored key `"Migration Patterns  "` does not match the lookup key `"Migration Patterns"`.
