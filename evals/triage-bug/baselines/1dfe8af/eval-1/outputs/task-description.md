# Jira API Metadata

```
jira.create_issue(
  project: "ACME",
  issue_type: "Task",
  labels: ["ai-generated-jira"],
  summary: "Fix trailing-whitespace handling in convention heading parser"
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
Fix the plan-feature skill's convention heading parser to strip trailing whitespace from `CONVENTIONS.md` heading lines. Currently, `line[3:]` extracts the heading text without calling `.strip()`, causing headings with trailing spaces to be stored with whitespace-padded keys. This breaks the exact-match lookup in the task enrichment step, silently dropping conventions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — fix heading extraction to strip trailing whitespace from `line[3:]`

## Implementation Notes
The defect is in the convention heading parser within `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code extracts heading text using `line[3:]` without stripping whitespace:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

Change the extraction to:

```python
section_name = line[3:].strip()
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) are normalized to `"Migration Patterns"` before being stored as dictionary keys, allowing the exact-match lookup in the task enrichment step to succeed:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md Section {convention_name}: {action}")
```

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings, so the reproducer test must create a new fixture or modify the existing one to cover this edge case.

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test: a test with a `CONVENTIONS.md` fixture containing trailing whitespace on a heading line (e.g., `## Migration Patterns  `) demonstrates that the convention is correctly parsed and included in the generated task's Implementation Notes (fails before fix, passes after)
- [ ] Convention heading parser strips trailing whitespace from extracted heading names so that headings with trailing spaces match correctly during task enrichment
- [ ] Conventions with trailing whitespace on headings are included in generated task Implementation Notes with the correct section reference
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a test fixture `CONVENTIONS.md` with trailing whitespace on a heading line (`## Migration Patterns  ` with two trailing spaces). Run the convention heading parser and assert the extracted section name equals `"Migration Patterns"` (without trailing whitespace). Verify the task enrichment step includes `Per CONVENTIONS.md Section Migration Patterns: add Index::create() for all FK columns.` in the Implementation Notes
- [ ] Test that headings without trailing whitespace continue to parse correctly (no regression)
- [ ] Test that headings with mixed whitespace (tabs, multiple spaces) are also handled correctly

## Verification Commands
- `python3 -m pytest evals/plan-feature/` — all existing plan-feature eval tests pass
- `python3 -m pytest evals/plan-feature/ -k trailing_whitespace` — reproducer test passes after fix

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with FKs, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: Per CONVENTIONS.md Section Migration Patterns: add `Index::create()` for all FK columns.
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction logic `line[3:]` does not strip trailing whitespace, causing headings with trailing spaces to be stored as whitespace-padded keys that fail exact-match lookup during task enrichment.
