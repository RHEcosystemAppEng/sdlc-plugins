# Jira API Metadata

```
jira.create_issue(
  project_key: "ACME",
  issue_type: "Task",
  labels: ["ai-generated-jira"],
  summary: "Fix plan-feature convention heading extraction to strip trailing whitespace"
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
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace
from CONVENTIONS.md heading lines during extraction. Currently, `line[3:]` preserves
trailing whitespace, causing convention names to include extra spaces. This produces a
silent mismatch during convention-aware task enrichment, where exact-match lookups against
clean convention names fail. Conventions are silently dropped from generated task
descriptions with no warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to convention heading extraction at `section_name = line[3:]`

## Implementation Notes
The defect is in the convention conformance analysis section of plan-feature. The heading
extraction logic iterates over lines in CONVENTIONS.md and extracts section names:

```python
section_name = line[3:]  # Current: preserves trailing whitespace
```

Change to:

```python
section_name = line[3:].strip()  # Fixed: normalizes heading text
```

This ensures that `conventions[section_name]` stores keys without trailing whitespace,
so the downstream lookup `if convention_name in discovered_conventions` matches correctly.

**Reproducer test guidance:**

The Steps to Reproduce specify creating a CONVENTIONS.md with trailing whitespace on a heading
line (`## Migration Patterns  `), running plan-feature, and checking that the convention
appears in the generated task's Implementation Notes.

- **Input that triggers the bug**: a CONVENTIONS.md fixture with trailing whitespace on heading
  lines, e.g.:
  ```
  ## Migration Patterns  
  Add Index::create() for all FK columns.
  ```
- **Incorrect behavior** (before fix): the convention `Migration Patterns` is NOT matched --
  it is silently dropped from the generated task's Implementation Notes.
- **Correct behavior** (after fix): the convention IS matched and the task's Implementation
  Notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

**Existing test patterns**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md`
tests convention matching but does NOT include trailing whitespace on headings. Create a new
fixture or augment the existing one to cover this edge case.

## Acceptance Criteria
- [ ] A reproducer test exists that creates a CONVENTIONS.md fixture with trailing whitespace on heading lines, runs convention extraction, and asserts the convention is matched and included in generated task output (fails before fix, passes after)
- [ ] The convention heading extraction in plan-feature strips trailing whitespace from extracted section names using `.strip()` or `.rstrip()`
- [ ] Conventions with trailing whitespace on headings in CONVENTIONS.md are correctly matched during task enrichment
- [ ] No regression in existing plan-feature evals and tests

## Test Requirements
- [ ] Reproducer test: create an eval fixture CONVENTIONS.md with trailing whitespace on one or more `##` heading lines (e.g., `## Migration Patterns  ` with trailing spaces). Run plan-feature convention extraction against the fixture. Assert that the convention IS matched by name and included in the generated task's Implementation Notes. This test must fail before the fix and pass after.
- [ ] Verify that conventions WITHOUT trailing whitespace continue to be matched correctly (no regression).
- [ ] Verify that headings with mixed whitespace patterns (tabs, multiple spaces, leading-and-trailing) are handled correctly.

## Verification Commands
- `cd /home/dev/repos/acme-backend && python3 -m pytest evals/plan-feature/ -v` -- all plan-feature evals pass, including the new trailing-whitespace reproducer

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The convention is silently dropped -- no reference to the Migration Patterns convention appears in the task's Implementation Notes, and no warning is shown.
- **Root Cause**: The heading extraction `section_name = line[3:]` does not strip trailing whitespace, producing keys like `"Migration Patterns  "` that fail exact-match lookups against clean convention names in the task enrichment step.
