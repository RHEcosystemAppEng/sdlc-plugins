<!-- Jira API Metadata Block
jira.create_issue parameters:
  project: ACME
  issuetype: Task
  labels:
    - ai-generated-jira
  summary: "Fix convention heading parser to strip trailing whitespace in plan-feature skill"
  link:
    type: Blocks
    inward_issue: <created-task-key>
    outward_issue: ACME-500
-->

## Repository
acme-backend

## Target Branch
main

## Description
The plan-feature skill's convention conformance analysis silently drops CONVENTIONS.md sections
whose headings contain trailing whitespace. The heading extraction logic uses `line[3:]` without
stripping whitespace, causing exact-match lookups to fail when stored keys have trailing spaces.
This fix normalizes heading text by stripping whitespace during extraction. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to convention heading extraction to normalize section names

## Implementation Notes
The defect is in the convention heading extraction logic in
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code:

```python
section_name = line[3:]
```

must be changed to:

```python
section_name = line[3:].strip()
```

This normalizes headings like `## Migration Patterns  ` (with trailing spaces) to
`"Migration Patterns"`, allowing the exact-match lookup in the task enrichment step to
succeed:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not cover
this edge case. The reproducer test should create a variant fixture with trailing whitespace
on headings.

Consider also adding a warning log when the raw heading text differs from the stripped
version, to surface formatting issues in CONVENTIONS.md files early.

Fixes [ACME-500](https://mock-jira.example.com/browse/ACME-500).

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing convention fixture that can be used as a reference for creating the reproducer test variant with trailing whitespace

## Acceptance Criteria
- [ ] Reproducer test: a test with a CONVENTIONS.md fixture containing trailing whitespace on a heading (e.g., `## Migration Patterns  `) demonstrates that the convention is correctly matched and included in the generated task's Implementation Notes (fails before fix, passes after)
- [ ] Convention heading extraction applies `.strip()` to normalize section names
- [ ] Conventions with trailing whitespace on headings are included in generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on at least one heading line (e.g., `## Migration Patterns  ` with two trailing spaces). Run the plan-feature convention conformance analysis against a feature matching that convention. Assert the generated task's Implementation Notes contain `Per CONVENTIONS.md Migration Patterns:` reference. This test must fail before the fix and pass after.
- [ ] Verify existing plan-feature eval tests continue to pass with the `.strip()` change (no regression from headings without trailing whitespace)

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction logic `line[3:]` does not strip trailing whitespace, causing the stored section name to include trailing spaces. The subsequent exact-match lookup fails silently because the query key has no trailing spaces while the stored key does.
