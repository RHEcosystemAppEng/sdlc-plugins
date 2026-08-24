<!-- Jira API Metadata Block
jira.create_issue parameters:
  project_key: ACME
  issue_type: Task
  labels:
    - ai-generated-jira
  summary: "Fix trailing whitespace handling in plan-feature convention heading extraction"
  link:
    type: Blocks
    inward_issue_key: <created-task-key>
    outward_issue_key: ACME-500
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace
from `CONVENTIONS.md` section headings during extraction. Currently, `section_name = line[3:]`
preserves trailing whitespace, causing exact-match lookups to fail silently when heading lines
contain trailing spaces. This results in conventions being omitted from generated task
descriptions without any warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Add `.strip()` to the heading
  extraction logic in the convention conformance analysis section to normalize section names

## Implementation Notes
The defect is in the convention conformance analysis section of the plan-feature skill.
The heading extraction loop currently reads:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

Change `line[3:]` to `line[3:].strip()` so that trailing whitespace on heading lines
(e.g., `## Migration Patterns  `) is normalized to the canonical name (`Migration Patterns`)
before storing in the `conventions` dictionary.

The downstream convention-aware task enrichment uses exact-match lookups:
```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```
This lookup will succeed once the extraction is fixed, since both sides will use
whitespace-normalized names.

**Existing test fixture**: `evals/plan-feature/files/conventions-mock.md` -- current fixture
does NOT include trailing whitespace on headings. The reproducer test should create a new
fixture (or extend the existing one) with trailing whitespace to cover this edge case.

**Reproducer test guidance**: The reproducer should create a CONVENTIONS.md fixture with
trailing whitespace on at least one heading line. Run the convention extraction logic and
assert that:
- The extracted section name equals `"Migration Patterns"` (no trailing spaces)
- The convention-to-task matching includes the convention in Implementation Notes output

The specific scenario from the bug report:
- **Input**: A `CONVENTIONS.md` with heading `## Migration Patterns  ` (two trailing spaces)
  and body `Add Index::create() for all FK columns.`
- **Incorrect behavior** (before fix): Implementation Notes omit the Migration Patterns
  convention entirely, with no warning
- **Correct behavior** (after fix): Implementation Notes include
  `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

## Acceptance Criteria
- [ ] Reproducer test: a test with trailing whitespace on a `CONVENTIONS.md` section heading demonstrates the bug (fails before fix, passes after fix)
- [ ] Convention heading extraction strips trailing whitespace so that `## Migration Patterns  ` is normalized to `"Migration Patterns"`
- [ ] Convention-aware task enrichment successfully matches and includes conventions from headings that had trailing whitespace
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create an eval fixture `CONVENTIONS.md` with trailing whitespace on at least one section heading (e.g., `## Migration Patterns  `). Assert that the extracted convention name is `"Migration Patterns"` (stripped) and that the generated task Implementation Notes include the expected convention reference `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- [ ] Edge case: verify that headings with no trailing whitespace continue to work correctly (regression guard)
- [ ] Edge case: verify that headings with mixed whitespace (tabs, multiple spaces) are also handled

## Verification Commands
- Run plan-feature eval tests to verify no regressions
- Run the new reproducer test to verify trailing whitespace is handled

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a section heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `section_name = line[3:]` does not strip trailing whitespace, causing exact-match convention lookups to fail silently when `CONVENTIONS.md` headings contain trailing spaces.
