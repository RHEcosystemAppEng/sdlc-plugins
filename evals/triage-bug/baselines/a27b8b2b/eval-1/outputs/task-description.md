<!-- Jira API Metadata Block -->
<!-- jira.create_issue parameters:
  project_key: ACME
  issue_type: Task
  labels: ["ai-generated-jira"]
  summary: "Fix plan-feature convention extraction to strip trailing whitespace from CONVENTIONS.md headings"
  link: { type: "Blocks", inward_issue: "<created-task-key>", outward_issue: "ACME-500" }
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace
from `CONVENTIONS.md` headings. Currently, `line[3:]` preserves trailing whitespace, causing
downstream convention lookups to fail silently when heading lines contain trailing spaces.
This results in conventions being omitted from generated task descriptions with no warning.
Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- strip trailing whitespace in the convention heading extraction logic (`section_name = line[3:]` -> `section_name = line[3:].strip()`)

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- test fixture with trailing whitespace on headings for reproducer test

## Implementation Notes
The defect is in the convention heading extraction loop within
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Does NOT strip trailing whitespace
        conventions[section_name] = current_section_content
```

Should be changed to:

```python
        section_name = line[3:].strip()
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces)
are extracted as `"Migration Patterns"`, matching the downstream lookup in the
convention-aware task enrichment:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does
NOT include trailing whitespace on headings, so the reproducer test requires a
new fixture file with trailing whitespace to exercise this edge case.

Consider also adding a defensive `.strip()` on the lookup side for defense in
depth.

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test: a test using a CONVENTIONS.md fixture with trailing whitespace on headings demonstrates the bug (fails before fix, passes after fix) -- the extracted section name must equal the heading text without trailing whitespace, and the convention must appear in the generated task's Implementation Notes
- [ ] Convention heading extraction strips trailing whitespace from extracted heading text (e.g., `## Migration Patterns  ` produces key `"Migration Patterns"`)
- [ ] Convention-aware task enrichment correctly matches and includes conventions from headings that originally had trailing whitespace
- [ ] No regression in existing plan-feature convention tests (existing `evals/plan-feature/files/conventions-mock.md` scenarios continue to pass)

## Test Requirements
- [ ] Reproducer test: create a test fixture `CONVENTIONS.md` with trailing whitespace on at least one `## ` heading (e.g., `## Migration Patterns  ` with two trailing spaces followed by convention content `Add Index::create() for all FK columns.`). Run the convention extraction logic and assert: (a) the extracted key equals `"Migration Patterns"` without trailing spaces, and (b) the generated task Implementation Notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- [ ] Edge case: headings with mixed whitespace (tabs, multiple spaces) are also stripped correctly
- [ ] Edge case: headings with no trailing whitespace continue to work as before (regression guard)

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The convention heading extraction uses `line[3:]` without stripping trailing whitespace, producing dictionary keys like `"Migration Patterns  "` that fail exact-match lookup against the clean name `"Migration Patterns"`.
