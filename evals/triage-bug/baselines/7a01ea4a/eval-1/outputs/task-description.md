# Jira API Metadata

```
jira.create_issue(
  project: "ACME",
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
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from
CONVENTIONS.md section headings during extraction. Currently, headings with trailing spaces
(e.g., `## Migration Patterns  `) produce whitespace-padded dictionary keys that fail exact-match
lookups, causing conventions to be silently dropped from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Apply `.strip()` to heading extraction in convention conformance analysis to normalize section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- Test fixture with trailing whitespace on convention headings for reproducer test

## Implementation Notes
The bug is in the convention heading extraction logic in
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code extracts section names
using `line[3:]` which does not strip trailing whitespace:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: no strip
        conventions[section_name] = current_section_content
```

**Fix**: Change the extraction to `section_name = line[3:].strip()` so that trailing whitespace
on heading lines is normalized before storing the section name in the dictionary.

**Reproducer test guidance**:
- Create a CONVENTIONS.md fixture containing a heading with trailing whitespace:
  `## Migration Patterns  ` (two trailing spaces after "Patterns")
- Include convention content under that heading: `Add Index::create() for all FK columns.`
- Run the convention conformance analysis against this fixture for a feature that requires
  database migration with foreign keys
- Assert that the generated task's Implementation Notes contain:
  `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- Before the fix: the convention is silently dropped (assertion fails)
- After the fix: the convention is included (assertion passes)

**Silent failure mitigation**: Consider adding a warning log when a convention name from the
feature analysis does not match any discovered convention, so that future mismatches are
surfaced rather than silently dropped.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` provides the pattern
for convention fixture files -- follow the same structure but add trailing whitespace to headings.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- Existing convention fixture file; follow its structure for the new trailing-whitespace test fixture

## Acceptance Criteria
- [ ] Reproducer test: a test with a CONVENTIONS.md fixture containing trailing whitespace on a heading line demonstrates the bug is fixed (fails before fix, passes after)
- [ ] Convention headings with trailing whitespace are correctly matched during plan-feature convention conformance analysis
- [ ] Conventions matched from headings with trailing whitespace are included in the generated task's Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on the `## Migration Patterns  ` heading, run convention conformance analysis, and assert the convention is matched and included in the output. The test must fail before the fix (convention silently dropped) and pass after (convention included as `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`)
- [ ] Verify that conventions with clean headings (no trailing whitespace) continue to work correctly (regression guard)
- [ ] Verify that headings with mixed whitespace (tabs, multiple spaces, newlines) are also handled by the strip operation

## Verification Commands
- Run plan-feature evals against the new trailing-whitespace fixture to confirm conventions are matched
- Run existing plan-feature evals to confirm no regression

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction logic uses `line[3:]` without `.strip()`, producing whitespace-padded dictionary keys that fail exact-match lookups in the convention-aware task enrichment step.
