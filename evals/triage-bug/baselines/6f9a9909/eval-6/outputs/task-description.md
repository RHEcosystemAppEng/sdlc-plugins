## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to handle trailing whitespace in CONVENTIONS.md heading lines. Currently, headings with trailing spaces (e.g., `## Migration Patterns  `) are extracted with the whitespace intact, causing exact-match lookups to fail and silently dropping the convention from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to heading extraction (`line[3:]` becomes `line[3:].strip()`) and add a warning log when convention matching fails

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- test fixture with trailing whitespace on heading lines to cover this edge case

## Implementation Notes
The bug is in the convention lookup loop in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction code:

```python
section_name = line[3:]
```

must be changed to:

```python
section_name = line[3:].strip()
```

This ensures that trailing whitespace on `CONVENTIONS.md` headings is normalized before storing in the conventions dictionary. The downstream exact-match lookup:

```python
if convention_name in discovered_conventions:
```

will then succeed regardless of trailing whitespace in the source file.

Additionally, add a warning log at the enrichment site when a convention name is not found in `discovered_conventions`, so future mismatches are observable rather than silent:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
else:
    log.warning(f"Convention '{convention_name}' not found in CONVENTIONS.md")
```

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace, so a new fixture is needed for the reproducer test.

No CONVENTIONS.md exists at the repository root, so no repository conventions apply to this fix.

## Acceptance Criteria
- [ ] Reproducer test: a test using a CONVENTIONS.md fixture with trailing whitespace on headings (e.g., `## Migration Patterns  `) demonstrates that the convention IS matched and included in the generated task's Implementation Notes. This test must fail before the fix and pass after.
- [ ] The heading extraction in the convention lookup loop uses `.strip()` to normalize trailing whitespace.
- [ ] A warning is logged when a convention name is not found during task enrichment.
- [ ] No regression in existing plan-feature evals (standard conventions without trailing whitespace continue to work).

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on at least one heading (`## Migration Patterns  ` with trailing spaces). Run the plan-feature convention lookup against this fixture and assert the convention appears in the generated task's Implementation Notes as `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- [ ] Regression test: verify existing conventions-mock.md fixture continues to produce correct convention references in task output.
- [ ] Warning log test: verify that when a convention name is not found in `discovered_conventions`, a warning message is logged.

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, causing exact-match dictionary lookup to fail silently when CONVENTIONS.md headings have trailing spaces.
