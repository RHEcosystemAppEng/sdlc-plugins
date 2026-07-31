<!-- Jira API metadata block -->
<!-- jira.create_issue parameters:
  project_key: ACME
  issue_type: Task
  labels: ["ai-generated-jira"]
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix trailing whitespace handling in the plan-feature skill's CONVENTIONS.md heading
extraction so that convention sections with trailing whitespace on heading lines are
correctly matched and included in generated task descriptions. Currently, the heading
extraction preserves trailing whitespace, causing exact-match lookups to silently fail.
Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- strip trailing whitespace from heading extraction (`line[3:]` to `line[3:].strip()`)

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- test fixture with trailing whitespace on convention headings

## Implementation Notes
The defect is in the convention conformance analysis section of the plan-feature skill.
The heading extraction logic reads CONVENTIONS.md and builds a dictionary keyed by
section name:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

When a heading line has trailing whitespace (e.g., `## Migration Patterns  `), the key
becomes `"Migration Patterns  "` and fails exact-match against `"Migration Patterns"`.

**Fix approach:**
1. Change `section_name = line[3:]` to `section_name = line[3:].strip()` to normalize
   heading names during extraction.
2. Consider also stripping the lookup key in the convention-aware task enrichment section
   for defense-in-depth.
3. Add a warning when a referenced convention is not found in the parsed conventions
   dictionary, to prevent silent failures in the future.

**Existing patterns to follow:**
- The existing convention parsing logic is in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
  in the convention conformance analysis section.
- The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` shows the
  test fixture format -- the new fixture should follow the same structure but include
  trailing whitespace on heading lines.

Fixes ACME-500.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing conventions test fixture; use as the base for the new trailing-whitespace fixture

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a CONVENTIONS.md fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  `) is parsed, and the convention is correctly matched and included in the generated task's Implementation Notes. The test fails before the fix and passes after.
- [ ] The heading extraction in the convention conformance analysis strips trailing whitespace from section names (using `.strip()` or equivalent).
- [ ] Convention matching succeeds regardless of trailing whitespace on CONVENTIONS.md heading lines.
- [ ] A warning is emitted when a convention referenced during task enrichment is not found in the parsed conventions, preventing silent failures.
- [ ] No regression in existing plan-feature evals and tests.

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on a heading line (`## Migration Patterns  `). Run the convention conformance analysis. Assert that the generated task's Implementation Notes include the convention reference (`Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`). This test must fail before the fix (convention silently dropped) and pass after (convention correctly included).
- [ ] Test that headings without trailing whitespace continue to work correctly (no regression).
- [ ] Test that headings with various whitespace patterns (tabs, mixed spaces) are handled correctly.
- [ ] Test that the warning is emitted when a referenced convention is not found.

## Verification Commands
- `pytest evals/plan-feature/` -- all plan-feature evals pass, including the new trailing-whitespace case

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md file with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring database migration with FKs, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction at `line[3:]` does not strip trailing whitespace. When CONVENTIONS.md headings have trailing spaces, the extracted key (e.g., `"Migration Patterns  "`) fails exact-match comparison against the clean lookup key (`"Migration Patterns"`), silently dropping the convention.
