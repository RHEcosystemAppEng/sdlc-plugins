## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading parser to strip trailing whitespace from
CONVENTIONS.md section headings, preventing silent convention drops during task generation.
Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the heading extraction at `section_name = line[3:]` to normalize trailing whitespace

## Implementation Notes
The bug is in the convention conformance analysis section of the plan-feature skill. The
heading extraction logic at `line[3:]` preserves trailing whitespace from CONVENTIONS.md
headings. When a heading like `## Migration Patterns  ` (with trailing spaces) is parsed,
the extracted key becomes `"Migration Patterns  "`, which fails the exact-match lookup
against the clean name `"Migration Patterns"` in the convention-aware task enrichment step.

**Fix location**: In the convention heading parser loop:
```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
```

Change to:
```python
        section_name = line[3:].strip()
```

This ensures consistent dictionary keys regardless of trailing whitespace in the source file.

**Reproducer test guidance**: The Steps to Reproduce from ACME-500 translate directly to a
test scenario:
- **Input**: A CONVENTIONS.md fixture with `## Migration Patterns  ` (trailing spaces on heading)
- **Trigger**: Run the convention extraction and lookup logic
- **Incorrect behavior (before fix)**: The convention name `"Migration Patterns"` is not found
  in `discovered_conventions`, and the generated task's Implementation Notes omit the convention
  reference entirely. No warning is logged.
- **Correct behavior (after fix)**: The convention name `"Migration Patterns"` is found in
  `discovered_conventions`, and the generated task's Implementation Notes include:
  `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

**Existing test patterns**: The eval fixture at `evals/plan-feature/files/conventions-mock.md`
provides the pattern for convention test fixtures but does not include trailing whitespace
on headings. The reproducer test should create a parallel fixture with trailing whitespace
to cover this edge case.

Fixes ACME-500.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing convention fixture pattern to follow when creating the trailing-whitespace variant

## Acceptance Criteria
- [ ] A reproducer test exists that creates a CONVENTIONS.md with trailing whitespace on a heading, runs the convention extraction, and asserts the convention is correctly matched by its clean name (fails before fix, passes after)
- [ ] The heading extraction in the convention conformance analysis strips trailing whitespace from extracted section names
- [ ] Conventions with trailing whitespace on headings are included in generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with `## Migration Patterns  ` (trailing spaces), run the convention parser, and assert that looking up `"Migration Patterns"` in the resulting dictionary succeeds and returns the correct section content (`Add Index::create() for all FK columns.`)
- [ ] Verify that clean headings (no trailing whitespace) continue to work correctly
- [ ] Verify that headings with mixed whitespace types (tabs, multiple spaces) are also normalized

## Verification Commands
- Run plan-feature evals to verify no regression: `cd evals/plan-feature && ./run.sh`

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction at `line[3:]` does not strip trailing whitespace, producing dictionary keys like `"Migration Patterns  "` that fail exact-match lookups against the expected clean name `"Migration Patterns"`.
