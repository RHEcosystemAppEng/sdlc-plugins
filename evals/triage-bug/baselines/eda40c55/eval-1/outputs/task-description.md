# Task Creation — ACME-500

## Jira API Metadata

```
jira.create_issue(
  project_key: "ACME",
  issue_type: "Task",
  summary: "Fix trailing-whitespace handling in plan-feature convention heading extraction",
  labels: ["ai-generated-jira"],
  description: <see below>
)
```

---

## Task Description

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from `CONVENTIONS.md` heading lines during extraction. Currently, `line[3:]` preserves trailing spaces, causing exact-match lookups against convention names to fail silently. This results in conventions being dropped from generated task Implementation Notes without any warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — fix heading extraction to strip trailing whitespace from `line[3:]`

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — new eval fixture with trailing whitespace on headings for the reproducer test

## Implementation Notes
The root cause is in the convention conformance analysis loop in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction code:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

should be changed to:

```python
        section_name = line[3:].strip()
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) are normalized to `"Migration Patterns"` before being stored in the conventions dictionary. The downstream exact-match lookup in the convention-aware task enrichment step will then succeed:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

**Reproducer test guidance**: The reproducer should create a `CONVENTIONS.md` fixture where at least one heading has trailing whitespace (e.g., `## Migration Patterns  ` with two trailing spaces after "Patterns"). The test should invoke the plan-feature convention extraction against this fixture and assert that the generated task's Implementation Notes include the convention reference `Per CONVENTIONS.md §Migration Patterns:`. Before the fix, this assertion will fail because the trailing whitespace causes a key mismatch. After the fix, the assertion will pass.

**Existing test patterns**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` provides the baseline pattern for conventions mock files — the reproducer fixture should follow the same format but add trailing whitespace to heading lines.

## Acceptance Criteria
- [ ] A reproducer test exists that creates a `CONVENTIONS.md` with trailing whitespace on headings and verifies the convention is correctly extracted and matched (fails before fix, passes after fix)
- [ ] `line[3:]` in the convention heading extraction is replaced with `line[3:].strip()` to normalize section names
- [ ] Conventions with trailing whitespace on headings are no longer silently dropped from generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a conventions fixture with trailing whitespace on the `## Migration Patterns  ` heading (two trailing spaces). Run the convention extraction logic and assert that the extracted section name equals `"Migration Patterns"` (no trailing whitespace). Assert that the convention-aware task enrichment output contains the string `Per CONVENTIONS.md §Migration Patterns:`. Before the fix, the lookup fails silently and the convention is absent from the output. After the fix, the convention is present.
- [ ] Verify that headings without trailing whitespace continue to be extracted correctly (no regression)
- [ ] Verify that headings with mixed whitespace (tabs, multiple spaces) are also handled by `.strip()`

## Verification Commands
- Run plan-feature eval suite to confirm no regression in existing tests
- Run the new reproducer test in isolation to confirm it passes after the fix

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: Heading extraction in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` uses `line[3:]` which preserves trailing whitespace. The subsequent exact-match dictionary lookup fails silently because the key `"Migration Patterns  "` does not match `"Migration Patterns"`.
