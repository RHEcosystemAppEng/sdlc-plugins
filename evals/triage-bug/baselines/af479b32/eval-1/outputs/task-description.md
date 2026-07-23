<!-- Jira API Metadata: jira.create_issue parameters -->
<!-- project: ACME -->
<!-- issue_type: Task -->
<!-- labels: ["ai-generated-jira"] -->
<!-- summary: Fix plan-feature convention heading extraction to strip trailing whitespace -->
<!-- link: Blocks ACME-500 -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to handle trailing whitespace on CONVENTIONS.md section headings. Currently, headings extracted with `line[3:]` retain trailing spaces, causing exact-match convention lookups to silently fail. This results in valid conventions being omitted from generated task descriptions without any warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- update convention heading extraction logic to strip trailing whitespace from extracted section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- eval fixture with trailing whitespace on headings for reproducer test

## Implementation Notes
The root cause is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction logic:

```python
section_name = line[3:]  # Extracts heading text after "## "
```

must be changed to strip trailing whitespace:

```python
section_name = line[3:].strip()
```

This ensures that headings like `## Migration Patterns  ` are stored as `"Migration Patterns"` in the `conventions` dictionary, matching the expected lookup keys in the convention-aware task enrichment step.

The convention-aware task enrichment performs:
```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md ...{convention_name}: {action}")
```

After stripping on the extraction side, this match will succeed regardless of trailing whitespace in the source file.

Consider also normalizing the lookup key (`convention_name.strip()`) as a defensive measure, so both sides of the comparison are whitespace-tolerant.

Optionally, add a diagnostic warning when a heading is parsed from CONVENTIONS.md but does not match any expected convention, to prevent future silent failures.

The existing eval fixture `evals/plan-feature/files/conventions-mock.md` can serve as a reference for the format of the new trailing-whitespace fixture.

Fixes ACME-500.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing conventions fixture without trailing whitespace; use as the base for creating the trailing-whitespace variant

## Acceptance Criteria
- [ ] A reproducer test exists that creates a CONVENTIONS.md with trailing whitespace on headings, runs the convention extraction logic, and verifies the convention is correctly matched and included in the task output (fails before fix, passes after)
- [ ] The convention heading extraction logic strips trailing whitespace from extracted section names
- [ ] Conventions with trailing whitespace on headings are included in generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on a `## Migration Patterns  ` heading, run convention extraction, and assert the convention is found under key `"Migration Patterns"` (without trailing spaces) and appears in the generated task's Implementation Notes as `Per CONVENTIONS.md "Migration Patterns: ...`
- [ ] Verify that clean headings (no trailing whitespace) continue to work correctly (no regression)
- [ ] Verify that headings with mixed whitespace types (tabs, multiple spaces) are also handled

## Verification Commands
- Run plan-feature eval suite to confirm no regressions
- Run the new trailing-whitespace eval case to confirm the fix

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include the convention reference (e.g., `Per CONVENTIONS.md "Migration Patterns: add Index::create() for all FK columns.`).
- **Actual Result**: The convention is silently dropped from Implementation Notes. No warning is shown.
- **Root Cause**: Heading extraction uses `line[3:]` without stripping trailing whitespace. The resulting key `"Migration Patterns  "` fails exact-match lookup against `"Migration Patterns"`, silently skipping the convention.
