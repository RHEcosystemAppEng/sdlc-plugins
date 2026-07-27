# Generated Task Description for ACME-500 Fix

This is the full Task description that would be created in Jira via `jira.create_issue`.

**Task Summary**: Fix plan-feature convention heading extraction to strip trailing whitespace
**Labels**: ai-generated-jira
**Link**: Task blocks ACME-500 (link type: Blocks)

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's CONVENTIONS.md heading extraction to strip trailing whitespace from section names. Currently, `line[3:]` preserves trailing spaces from heading lines, causing exact-match convention lookups to silently fail. This results in valid conventions being omitted from generated task descriptions with no warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to heading extraction at `line[3:]` to normalize section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- eval fixture with trailing whitespace on convention headings for reproducer test

## Implementation Notes
The defect is in the convention heading extraction loop within the plan-feature skill:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

The fix is to apply `.strip()` to the extracted section name:

```python
section_name = line[3:].strip()
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) produce the key `"Migration Patterns"`, which correctly matches during the task enrichment lookup:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

Additionally, consider adding a warning log when a convention name from the feature analysis is not found in `discovered_conventions`, to prevent silent failures in the future.

**Existing test patterns**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings. The reproducer test should create a new fixture that does.

**Reuse note**: Follow the same fixture pattern used in the existing plan-feature eval (`evals/plan-feature/files/conventions-mock.md`) for consistency.

Fixes ACME-500.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing convention fixture pattern to follow when creating the trailing-whitespace variant

## Acceptance Criteria
- [ ] A reproducer test exists that creates a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), runs the convention extraction, and asserts the convention is correctly matched and included in the generated task output. This test fails before the fix and passes after.
- [ ] The heading extraction in plan-feature applies `.strip()` (or equivalent) to `line[3:]` so that trailing whitespace on CONVENTIONS.md headings does not prevent convention matching.
- [ ] When a CONVENTIONS.md heading has trailing whitespace, the generated task's Implementation Notes correctly includes the convention reference (e.g., "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.").
- [ ] No regression in existing plan-feature eval tests.

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with `## Migration Patterns  ` (two trailing spaces). Run the plan-feature convention analysis against a feature requiring database migration with foreign keys. Assert the generated task's Implementation Notes contains "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns." -- this test must fail before the fix (convention dropped) and pass after (convention included).
- [ ] Edge-case test: verify that headings with tabs, mixed whitespace, and no trailing whitespace all produce correctly trimmed section names.
- [ ] Regression test: confirm existing conventions without trailing whitespace continue to match correctly after the fix.

## Verification Commands
- Run the plan-feature eval suite to confirm no regressions and the new trailing-whitespace test passes.

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring DB migration with FK columns, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, producing a key like `"Migration Patterns  "` that fails exact-match comparison against `"Migration Patterns"` during convention-aware task enrichment.
