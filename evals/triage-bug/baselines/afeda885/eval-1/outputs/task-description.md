<!-- Jira API: jira.create_issue -->
<!-- project: ACME -->
<!-- issue_type: Task -->
<!-- labels: ["ai-generated-jira"] -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace, so that conventions in `CONVENTIONS.md` with trailing spaces on heading lines are correctly matched and included in generated task descriptions. Currently, `line[3:]` preserves trailing whitespace, causing exact-match lookups to fail silently.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- fix heading extraction to use `line[3:].strip()` instead of `line[3:]` in the convention conformance analysis section

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- eval fixture with trailing whitespace on convention headings for regression testing

## Implementation Notes
The bug is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction loop:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

must be changed to:

```python
        section_name = line[3:].strip()  # Strip trailing whitespace from heading
```

The convention-aware task enrichment step performs an exact match:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This match fails when the key has trailing whitespace. The `.strip()` fix normalizes the key at extraction time so the lookup succeeds.

As a secondary improvement, consider adding a warning when a referenced convention is not found in `discovered_conventions`, to prevent silent failures for other edge cases in the future.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings -- the new fixture should add trailing spaces to at least one heading to cover this edge case.

## Acceptance Criteria
- [ ] Reproducer test: a `CONVENTIONS.md` fixture with trailing whitespace on heading `## Migration Patterns  ` is correctly parsed, and the extracted section name equals `"Migration Patterns"` (no trailing spaces)
- [ ] Convention heading extraction uses `line[3:].strip()` instead of `line[3:]`
- [ ] Conventions with trailing whitespace on headings are included in generated task Implementation Notes
- [ ] No silent dropping of conventions -- all matched conventions appear in output
- [ ] Existing conventions without trailing whitespace continue to work correctly (no regression)

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on the heading `## Migration Patterns  ` and verify the convention is extracted with key `"Migration Patterns"` (stripped)
- [ ] Verify that the generated task's Implementation Notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.` when using the trailing-whitespace fixture
- [ ] Regression test: verify that conventions without trailing whitespace continue to be extracted and matched correctly
- [ ] Edge case: verify headings with mixed whitespace (tabs, multiple spaces) are also handled by `.strip()`

## Verification Commands
- `grep -n 'line\[3:\]' plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- should show `.strip()` call on the extraction line
- Run plan-feature eval with trailing-whitespace fixture -- convention should appear in generated task output

## Bug Context

- **Bug Key**: ACME-500
- **Steps to Reproduce**:
  1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
     ```
     ## Migration Patterns  
     Add Index::create() for all FK columns.
     ```
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
  3. Inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: Heading extraction uses `line[3:]` without `.strip()`, preserving trailing whitespace in the dictionary key. The subsequent exact-match lookup against the normalized convention name fails silently.
