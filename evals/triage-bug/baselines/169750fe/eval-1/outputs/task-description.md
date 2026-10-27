# Jira API Metadata

```
jira.create_issue(
  project_key: "ACME",
  issue_type: "Task",
  labels: ["ai-generated-jira"],
  summary: "Fix convention heading extraction to strip trailing whitespace"
)
```

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace from `CONVENTIONS.md` headings. Currently, `line[3:]` preserves trailing spaces, causing exact-match lookups against convention names to fail silently. This results in conventions being dropped from generated task descriptions without any warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the heading extraction at `line[3:]` in the convention lookup loop

## Implementation Notes
The defect is in the convention lookup loop within the plan-feature skill. The heading extraction currently reads:

```python
section_name = line[3:]
```

This must be changed to:

```python
section_name = line[3:].strip()
```

This normalizes trailing whitespace from `CONVENTIONS.md` heading lines so that the dictionary key matches the exact convention name used in the task enrichment lookup:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The enrichment lookup code does not need modification -- once the keys are properly stripped, the exact-match `in` check will succeed.

Reference the existing eval fixture at `evals/plan-feature/files/conventions-mock.md` for the pattern used in convention test files. The reproducer test should create a similar fixture but with trailing whitespace on heading lines.

Fixes ACME-500.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a `CONVENTIONS.md` fixture with trailing whitespace on a heading (e.g., `## Migration Patterns  `) is parsed correctly, and the convention is included in the generated task output. The test fails before the fix and passes after.
- [ ] The convention heading extraction uses `line[3:].strip()` instead of `line[3:]` to normalize trailing whitespace.
- [ ] Conventions with trailing whitespace on headings are no longer silently dropped from generated task descriptions.
- [ ] No regression in existing plan-feature eval tests -- conventions without trailing whitespace continue to work correctly.

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  ` with trailing spaces). Run the convention lookup logic against it and assert that (a) the extracted section name equals `"Migration Patterns"` without trailing spaces, and (b) the convention-aware task enrichment includes the expected note `Per CONVENTIONS.md Migration Patterns: ...` in the generated output. This test must fail before the fix and pass after.
- [ ] Regression test: verify that existing `CONVENTIONS.md` fixtures without trailing whitespace continue to parse correctly and produce the expected task enrichment notes.
- [ ] Edge case test: verify handling of headings with mixed whitespace (tabs, multiple spaces, newline characters) to ensure `.strip()` handles all whitespace variants.

## Verification Commands
- Run the plan-feature eval suite to confirm no regressions.

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The convention heading extraction uses `line[3:]` which does not strip trailing whitespace, causing exact-match dictionary lookups to fail silently when `CONVENTIONS.md` headings have trailing spaces.
