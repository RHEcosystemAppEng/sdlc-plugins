<!-- Jira API Metadata Block
jira.create_issue parameters:
  project_key: ACME
  issue_type: Task
  labels:
    - ai-generated-jira
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix trailing whitespace handling in plan-feature convention extraction so that CONVENTIONS.md
headings with trailing spaces are correctly matched during task enrichment. Currently, `line[3:]`
does not strip trailing whitespace when extracting headings, causing exact-match lookups to fail
silently and omit conventions from generated tasks. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the heading extraction at `line[3:]` to remove trailing whitespace from section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- test fixture with trailing whitespace on heading lines for reproducer test

## Implementation Notes
The defect is in the convention extraction loop in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
The current code:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

Must be changed to:

```python
        section_name = line[3:].strip()
```

This ensures that a heading like `## Migration Patterns  ` (with trailing spaces) produces the
key `"Migration Patterns"` rather than `"Migration Patterns  "`, allowing the downstream
exact-match lookup in the convention-aware task enrichment to succeed:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The reproducer test should create a `CONVENTIONS.md` fixture with trailing whitespace on a heading
(e.g., `## Migration Patterns  ` with two trailing spaces after "Patterns"), run the convention
extraction, and assert that the extracted section name matches `"Migration Patterns"` exactly.
Then verify that the convention-aware task enrichment includes the convention in the generated
task's Implementation Notes.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT include
trailing whitespace on headings, so a new fixture is needed for this edge case.

Fixes ACME-500.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: extraction of a heading with trailing whitespace from CONVENTIONS.md yields a key that matches the expected convention name (fails before fix, passes after)
- [ ] `line[3:]` is replaced with `line[3:].strip()` in the convention extraction loop so that trailing whitespace on headings is removed
- [ ] Convention-aware task enrichment correctly includes conventions whose CONVENTIONS.md headings have trailing whitespace
- [ ] No regression in existing plan-feature evals and tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  `), run the convention extraction logic, and assert that (a) the extracted section name equals `"Migration Patterns"` without trailing spaces, and (b) the convention-aware task enrichment includes the convention in the generated task's Implementation Notes
- [ ] Verify that headings without trailing whitespace continue to work correctly (no regression)
- [ ] Verify that headings with mixed whitespace (tabs, multiple spaces) are also handled by `.strip()`

## Verification Commands
- `pytest evals/plan-feature/ -v` -- all plan-feature evals pass, including the new trailing-whitespace reproducer

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include the convention reference: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The convention extraction logic uses `line[3:]` to extract heading text from CONVENTIONS.md but does not call `.strip()`, so trailing whitespace on heading lines causes exact-match lookup failures in the downstream task enrichment step.
