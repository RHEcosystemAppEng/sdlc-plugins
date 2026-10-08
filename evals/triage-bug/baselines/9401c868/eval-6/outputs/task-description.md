## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace before storing section names, so that conventions in CONVENTIONS.md with trailing spaces on headings are correctly matched and included in generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the heading extraction expression `line[3:]` so trailing whitespace is normalized before dictionary storage

## Files to Create
- `evals/plan-feature/files/conventions-trailing-ws-mock.md` -- eval fixture with trailing whitespace on convention headings to cover this edge case

## Implementation Notes
The defect is in the convention heading extraction logic within the plan-feature skill. The current code:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
conventions[section_name] = current_section_content
```

must be changed to:

```python
section_name = line[3:].strip()
conventions[section_name] = current_section_content
```

This ensures that a heading like `## Migration Patterns  ` (with trailing spaces) is stored as `"Migration Patterns"` and correctly matched during the convention-aware task enrichment step:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT include trailing whitespace on headings, so this edge case is not covered. Create a new fixture `evals/plan-feature/files/conventions-trailing-ws-mock.md` with headings that include trailing spaces to validate the fix.

Optionally, add a warning log when a convention match fails to aid debugging of similar issues in the future. This improves observability for cases where conventions are expected but not found.

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test: a test using a CONVENTIONS.md fixture with trailing whitespace on headings demonstrates that the convention is correctly extracted and included in the generated task description (fails before fix, passes after)
- [ ] The heading extraction in the plan-feature convention lookup strips trailing whitespace from section names using `.strip()`
- [ ] Conventions with trailing whitespace on headings in CONVENTIONS.md are correctly matched and included in generated task Implementation Notes
- [ ] No regression in existing plan-feature tests and evals

## Test Requirements
- [ ] Reproducer test: create an eval fixture `evals/plan-feature/files/conventions-trailing-ws-mock.md` with convention headings that have trailing whitespace (e.g., `## Migration Patterns  ` with two trailing spaces). Run the convention extraction and enrichment pipeline against this fixture and assert that the generated task's Implementation Notes include `Per CONVENTIONS.md "Migration Patterns": add Index::create() for all FK columns.` -- this test must fail before the fix and pass after
- [ ] Verify that the existing eval fixture (without trailing whitespace) continues to work correctly after the change
- [ ] Verify that headings with various whitespace patterns (tabs, multiple spaces, mixed) are all correctly normalized

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include the convention reference: `Per CONVENTIONS.md "Migration Patterns": add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction uses `line[3:]` without `.strip()`, so trailing whitespace is preserved in the dictionary key. The exact-match lookup then fails to match the whitespace-padded key against the expected clean convention name, silently dropping the convention from the output.
