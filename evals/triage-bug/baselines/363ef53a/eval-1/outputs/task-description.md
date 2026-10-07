<!-- Jira API metadata — jira.create_issue parameters -->
<!-- project: ACME -->
<!-- issuetype: 10142 -->
<!-- labels: ["ai-generated-jira", "bug-fix"] -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention extraction to strip trailing whitespace from CONVENTIONS.md heading lines. Currently, `line[3:]` preserves trailing whitespace, causing the extracted section name to include trailing spaces (e.g., `"Migration Patterns  "`). This causes exact-match lookups during task enrichment to fail silently, omitting the convention from generated task descriptions.

## Bug Context

- **Bug**: ACME-500 -- plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Steps to Reproduce**:
  1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading (e.g., `## Migration Patterns  `).
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
  3. Inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include the convention reference (e.g., `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`).
- **Actual Result**: The generated task's Implementation Notes do NOT reference the convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` extracts convention headings with `section_name = line[3:]` without calling `.strip()`. Trailing whitespace in the heading line produces a dictionary key that does not match the clean lookup key used during task enrichment.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the heading extraction: change `section_name = line[3:]` to `section_name = line[3:].strip()`

## Implementation Notes
The fix is a single-character change in the convention extraction loop within `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The relevant code block is:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

Change `line[3:]` to `line[3:].strip()` to normalize the extracted section name. This ensures the dictionary key matches the downstream lookup key regardless of trailing whitespace in the source file.

No other call sites need changes -- stripping at extraction time normalizes the key at the source.

## Acceptance Criteria
- [ ] Reproducer test: a test with a CONVENTIONS.md heading containing trailing whitespace confirms the convention is correctly extracted and matched
- [ ] `section_name = line[3:].strip()` is applied in the convention extraction loop
- [ ] Conventions with trailing whitespace on headings are included in generated task descriptions
- [ ] Existing plan-feature evals continue to pass with no regressions

## Test Requirements
- [ ] Reproducer test: add a plan-feature eval case with a CONVENTIONS.md fixture that has trailing whitespace on at least one heading line; verify the generated task's Implementation Notes includes the convention reference
- [ ] Edge case test: headings with mixed whitespace (tabs, multiple spaces) are correctly normalized
- [ ] Regression test: existing conventions without trailing whitespace continue to be extracted and matched correctly

## Verification Commands
- `python -m pytest evals/plan-feature/ -v` -- all plan-feature evals pass, including the new trailing-whitespace case
