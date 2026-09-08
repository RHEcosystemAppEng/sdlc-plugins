# Jira API Metadata

Parameters for `jira.create_issue`:

| Parameter | Value |
|-----------|-------|
| Project key | ACME |
| Issue type | Task |
| Labels | ai-generated-jira |
| Summary | Fix plan-feature convention parser to strip trailing whitespace from CONVENTIONS.md headings |

```
jira.create_issue(
  project_key="ACME",
  issue_type="Task",
  summary="Fix plan-feature convention parser to strip trailing whitespace from CONVENTIONS.md headings",
  additional_fields={"labels": ["ai-generated-jira"]}
)
```

After creation, link the Task to the Bug:

```
jira.create_issue_link(
  link_type="Blocks",
  inward_issue_key="<created-task-key>",
  outward_issue_key="ACME-500"
)
```

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's CONVENTIONS.md heading parser to strip trailing whitespace from extracted section names. Currently, headings with trailing spaces (e.g., `## Migration Patterns  `) produce dictionary keys that include those spaces, causing exact-match convention lookups to silently fail. This results in conventions being omitted from generated task descriptions without any warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the heading extraction logic in the convention conformance analysis section

## Implementation Notes
The bug is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. Two changes are needed:

1. **Heading extraction fix (primary):** In the convention lookup loop, the line:
   ```python
   section_name = line[3:]
   ```
   must be changed to:
   ```python
   section_name = line[3:].strip()
   ```
   This normalizes trailing (and leading) whitespace from the extracted heading text before storing it as a dictionary key.

2. **Defense-in-depth normalization (recommended):** In the convention-aware task enrichment section, also normalize the lookup key:
   ```python
   if convention_name.strip() in discovered_conventions:
   ```
   This guards against whitespace inconsistencies from either side of the comparison.

3. **Silent failure logging (recommended):** Consider adding a warning when an expected convention name is not found in the parsed conventions dictionary, so that similar issues are surfaced rather than silently dropped.

**Existing test patterns:** The eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings. The reproducer test should create a new fixture (or extend the existing one) that includes trailing whitespace to cover this edge case.

**Reproducer test guidance:**
- Input: A `CONVENTIONS.md` fixture with a heading containing trailing whitespace, e.g., `## Migration Patterns  ` (two trailing spaces)
- Trigger: Run the plan-feature convention conformance analysis against this fixture for a feature requiring migration conventions
- Incorrect behavior (before fix): The convention `Migration Patterns` is absent from the generated task's Implementation Notes
- Correct behavior (after fix): The generated task's Implementation Notes include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

## Acceptance Criteria
- [ ] A reproducer test exists that uses a CONVENTIONS.md fixture with trailing whitespace on a heading line, asserts the convention IS included in the generated task output (fails before fix, passes after fix)
- [ ] The convention heading extraction in plan-feature strips trailing whitespace from extracted section names using `.strip()`
- [ ] Conventions with trailing whitespace on headings in CONVENTIONS.md are correctly matched and included in generated task descriptions
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: Create a CONVENTIONS.md fixture with `## Migration Patterns  ` (trailing whitespace) containing `Add Index::create() for all FK columns.`, run plan-feature convention analysis against it, and assert the output includes the `Migration Patterns` convention reference. This test must fail before the fix is applied and pass after.
- [ ] Verify that headings without trailing whitespace continue to work correctly (no regression)
- [ ] Verify that headings with leading whitespace after `## ` are also handled (defense-in-depth, if `.strip()` is applied)

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, causing the stored key `"Migration Patterns  "` to fail exact-match comparison against the expected key `"Migration Patterns"`. No warning is logged on mismatch.
