## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace from `CONVENTIONS.md` headings, preventing silent convention drops during task generation. The heading parser uses `line[3:]` without `.strip()`, causing exact-match lookups to fail when headings have trailing spaces. Additionally, add a warning log when a known convention name is not found in the discovered conventions, to prevent silent failures. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- fix heading extraction to strip trailing whitespace (`line[3:].strip()`) and add a warning when convention lookup fails

## Implementation Notes
The root cause is in the convention heading extraction logic within the plan-feature skill. The current code:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

The fix should change `line[3:]` to `line[3:].strip()` so that trailing whitespace on heading lines is normalized before storing the section name in the `conventions` dictionary.

The convention-aware task enrichment then performs an exact match:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

After fixing the extraction, this lookup will succeed because the dictionary key will match the canonical convention name. Additionally, consider adding a warning when a convention name is expected but not found:

```python
if convention_name not in discovered_conventions:
    log.warning(f"Convention '{convention_name}' not found in CONVENTIONS.md")
```

Reference the existing eval fixture at `evals/plan-feature/files/conventions-mock.md` for the current convention parsing test patterns. The reproducer test should add a new fixture with trailing whitespace on headings.

No CONVENTIONS.md was found in the repository root.

## Acceptance Criteria
- [ ] Reproducer test: a test that creates a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `) and runs the plan-feature convention analysis, asserting that the generated task's Implementation Notes include the convention reference `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` (fails before fix, passes after)
- [ ] The convention heading extraction strips trailing whitespace from heading text so that `## Migration Patterns  ` produces the key `"Migration Patterns"`
- [ ] Convention conformance analysis matches conventions regardless of trailing whitespace on `CONVENTIONS.md` headings
- [ ] A warning is logged when a known convention name is not found in the discovered conventions (preventing future silent failures)
- [ ] No regression in existing plan-feature convention tests
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  ` with two trailing spaces) and a convention body. Run the plan-feature convention conformance analysis on a feature that should trigger the convention. Assert: (1) the convention is included in the generated task's Implementation Notes with the correct section reference, (2) the heading key in the conventions dictionary does not contain trailing whitespace
- [ ] Regression test: verify that conventions with clean headings (no trailing whitespace) continue to be matched correctly -- existing eval fixture at `evals/plan-feature/files/conventions-mock.md` should still pass
- [ ] Edge case: verify conventions with multiple types of whitespace (tabs, mixed spaces/tabs) on heading lines are correctly stripped
- [ ] Edge case: verify that headings with only whitespace after `## ` (e.g., `##    `) are handled gracefully (empty convention name)
- [ ] Warning test: verify that a warning is logged when a convention name is expected but not found in the discovered conventions dictionary

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading (`## Migration Patterns  `). Run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys. Inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The convention heading extraction uses `line[3:]` without `.strip()`, producing keys with trailing whitespace that fail exact-match lookups against canonical convention names. The lookup failure is silent, causing conventions to be dropped without any warning.
