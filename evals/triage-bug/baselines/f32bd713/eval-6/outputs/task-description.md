## Repository
acme-backend

## Target Branch
main

## Description
Fix the convention heading parser in plan-feature to strip trailing whitespace from CONVENTIONS.md section headings, preventing silent convention drops during task enrichment. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the heading extraction at `line[3:]` so trailing whitespace is removed from section names before storing in the conventions dictionary
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add a warning log in the task enrichment step when a convention name lookup fails, so that silent drops are surfaced in the future

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- eval fixture containing convention headings with trailing whitespace to cover this edge case

## Implementation Notes
The defect is in the convention heading extraction loop within the plan-feature skill. The current code:

```python
section_name = line[3:]
```

must be changed to:

```python
section_name = line[3:].strip()
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) are normalized to `"Migration Patterns"` before being stored as dictionary keys.

Additionally, in the task enrichment step, the silent failure path:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

should log a warning when `convention_name` is NOT found in `discovered_conventions`, so that missing conventions are visible during debugging rather than silently omitted.

The reproducer test should create a `CONVENTIONS.md` fixture with trailing whitespace on heading lines and verify that the convention is correctly matched and included in the generated task output. Reference the existing eval fixture at `evals/plan-feature/files/conventions-mock.md` for the baseline pattern -- the new fixture should mirror its structure but include trailing whitespace on at least one heading.

The specific input that triggers the bug: a `CONVENTIONS.md` with `## Migration Patterns  ` (two trailing spaces after "Patterns"). The incorrect behavior: the convention is silently dropped from the generated task's Implementation Notes. The correct behavior: the task's Implementation Notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

## Acceptance Criteria
- [ ] Reproducer test: create a test with a CONVENTIONS.md fixture containing trailing whitespace on heading lines (e.g., `## Migration Patterns  `), run the convention conformance analysis, and assert the convention IS matched and included in the generated task output. This test must fail before the fix and pass after.
- [ ] The heading extraction in the convention parser strips trailing whitespace from section names using `.strip()`
- [ ] A warning is logged when a convention name lookup fails during task enrichment, so silent drops are visible
- [ ] Existing conventions without trailing whitespace continue to be matched correctly (no regression)
- [ ] No regression in existing plan-feature evals

## Test Requirements
- [ ] Reproducer test: create an eval fixture `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` with trailing whitespace on at least one heading (e.g., `## Migration Patterns  `). Run the convention heading extraction against this fixture and assert that the extracted section name equals `"Migration Patterns"` (without trailing whitespace). Then run the full convention conformance analysis and assert the convention appears in the generated task's Implementation Notes.
- [ ] Regression test: verify that the existing eval fixture `evals/plan-feature/files/conventions-mock.md` (without trailing whitespace) continues to produce correct convention matches after the fix.
- [ ] Warning test: verify that when a convention name is not found in the discovered conventions, a warning log message is produced containing the unmatched convention name.

## Verification Commands
- `python3 -m pytest evals/plan-feature/ -v` -- all plan-feature evals pass, including the new trailing-whitespace test

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The convention heading parser extracts section names using `line[3:]` without stripping trailing whitespace. Headings with trailing spaces produce mismatched dictionary keys, causing exact-match lookups to fail silently during task enrichment.

---

**Jira API metadata:**

```
project: ACME
issueType: Task
labels: ["ai-generated-jira"]
link: { type: "Blocks", inward: "<created-task-key>", outward: "ACME-500" }
```
