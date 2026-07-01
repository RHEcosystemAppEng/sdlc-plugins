<!-- Jira API: jira.create_issue -->
<!-- project: ACME -->
<!-- issuetype: Task -->
<!-- labels: ["ai-generated-jira", "bug-fix"] -->
<!-- link: { "type": "Blocks", "outwardIssue": "ACME-500" } -->

# Fix plan-feature silent convention drop when CONVENTIONS.md headings have trailing whitespace

## Repository

acme-backend

## Target Branch

main

## Description

The plan-feature skill's convention conformance analysis silently drops conventions when `CONVENTIONS.md` heading lines contain trailing whitespace. The heading extraction logic uses `line[3:]` without stripping whitespace, causing downstream exact-match lookups to fail. This results in generated tasks missing convention references with no warning to the user.

This task fixes the heading extraction to normalize whitespace, adds a defensive warning for unmatched conventions, and adds a reproducer test to prevent regression.

## Files to Modify

- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Convention conformance analysis: add `.strip()` to heading extraction
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Convention-aware task enrichment: add warning log on unmatched convention name (defensive)
- `evals/plan-feature/files/conventions-mock.md` -- Add trailing-whitespace variant for the reproducer test fixture

## Implementation Notes

- **Bug reference:** This task addresses [ACME-500](https://mock-jira.example.com/browse/ACME-500) -- plan-feature silently drops conventions when `CONVENTIONS.md` has trailing whitespace.
- **Root cause:** In the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, the heading extraction `section_name = line[3:]` does not strip trailing whitespace. When a heading line is `## Migration Patterns  \n`, the extracted key becomes `"Migration Patterns  "` (with trailing spaces), which fails the exact-match lookup `if convention_name in discovered_conventions` in the task enrichment step.
- **Fix pattern:** Change `section_name = line[3:]` to `section_name = line[3:].strip()` to normalize the dictionary key. This is a minimal, targeted fix that handles trailing whitespace (spaces, tabs) on heading lines.
- **Defensive logging:** In the convention-aware task enrichment block, add an `else` branch to log a warning when an expected convention name is not found in `discovered_conventions`. This prevents future silent-drop scenarios.
- **Existing test gap:** The current eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on any headings, so this edge case was invisible to CI.

## Acceptance Criteria

1. **Reproducer test passes:** A test using a `CONVENTIONS.md` fixture with trailing whitespace on the heading `## Migration Patterns  ` (two trailing spaces) produces a task whose Implementation Notes include the convention reference `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
2. **Whitespace normalization:** The convention heading extraction in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` strips trailing whitespace from extracted section names using `.strip()`.
3. **Warning on unmatched convention:** When a convention name expected by the task enrichment step is not found in the discovered conventions dictionary, a warning is logged (not silently skipped).
4. **No regression:** All existing plan-feature evals continue to pass. Clean headings (without trailing whitespace) are unaffected by the `.strip()` addition.

## Test Requirements

1. **Reproducer test (required first):** Create or update the eval fixture at `evals/plan-feature/files/conventions-mock.md` to include a convention section with trailing whitespace on the heading line (e.g., `## Migration Patterns  ` with two trailing spaces). Run the plan-feature skill against a feature that triggers the "Migration Patterns" convention and assert that the generated task's Implementation Notes contain: `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` This test must fail before the fix and pass after.
2. **Existing eval regression:** Run the full plan-feature eval suite (`evals/plan-feature/`) and confirm all existing test cases continue to pass.
3. **Warning log verification:** When a convention heading does not match (simulated by a missing key), confirm a warning message is emitted rather than a silent skip.

## Bug Context

- **Bug key:** [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce:**
  1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading: `## Migration Patterns  ` (two trailing spaces) followed by `Add Index::create() for all FK columns.`
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
  3. Inspect the generated task's Implementation Notes.
- **Expected Result:** The generated task's Implementation Notes should include: `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result:** The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause:** Heading extraction `line[3:]` in convention conformance analysis does not strip trailing whitespace, causing exact-match dictionary lookup to fail silently in the task enrichment step.
