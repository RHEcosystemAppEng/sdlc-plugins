<!-- Jira API Metadata
jira.create_issue parameters:
  project: ACME
  issue_type: Task
  labels:
    - ai-generated-jira
  summary: "Fix trailing-whitespace heading extraction in plan-feature convention conformance analysis"
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from `CONVENTIONS.md` headings during extraction. Currently, `line[3:]` preserves trailing spaces, causing exact-match convention lookups to fail silently when headings have trailing whitespace. This results in conventions being dropped from generated task Implementation Notes with no warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — fix heading extraction to strip trailing whitespace (`line[3:]` -> `line[3:].strip()`)

## Implementation Notes
The defect is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

When `CONVENTIONS.md` contains a heading like `## Migration Patterns  ` (with trailing spaces), `line[3:]` produces `"Migration Patterns  "`. The convention-aware task enrichment step then looks up `"Migration Patterns"` (without spaces), which fails the exact-match check:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

**Fix**: Change `line[3:]` to `line[3:].strip()` to normalize heading names before storing them as dictionary keys.

**Reproducer test guidance**: Create a test fixture `CONVENTIONS.md` with trailing whitespace on a heading line (e.g., `## Migration Patterns  ` with 2+ trailing spaces). Run the convention extraction logic and verify that the key stored in the dictionary is `"Migration Patterns"` (trimmed). Then verify the convention lookup succeeds and the output includes the convention reference.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT include trailing whitespace on headings, so a new fixture or modification is needed.

## Acceptance Criteria
- [ ] Reproducer test: a test using a `CONVENTIONS.md` fixture with trailing whitespace on a heading (e.g., `## Migration Patterns  `) demonstrates that the convention is correctly matched and included in the generated task's Implementation Notes — this test fails before the fix and passes after
- [ ] The heading extraction logic in plan-feature convention conformance analysis strips trailing whitespace from extracted heading names
- [ ] Conventions with trailing whitespace on headings are included in generated task Implementation Notes (not silently dropped)
- [ ] No regression in existing plan-feature tests and evals

## Test Requirements
- [ ] Reproducer test with trailing-whitespace heading: create a `CONVENTIONS.md` fixture containing `## Migration Patterns  ` (with trailing spaces) and assert that the extracted section name equals `"Migration Patterns"` (without trailing spaces), and that the generated output contains `Per CONVENTIONS.md §Migration Patterns:` — this test must fail before the fix is applied and pass after
- [ ] Test that headings without trailing whitespace continue to work correctly (no regression)
- [ ] Test that multiple headings with varying amounts of trailing whitespace are all normalized correctly

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: The heading extraction logic `line[3:]` does not strip trailing whitespace, causing the convention dictionary key to include trailing spaces. The subsequent exact-match lookup against the untrimmed key fails silently, dropping the convention.
