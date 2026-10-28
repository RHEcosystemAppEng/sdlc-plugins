## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from CONVENTIONS.md heading lines during extraction, so that conventions are correctly matched and included in generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- fix heading extraction to strip trailing whitespace from `line[3:]` and add warning logging for unmatched convention lookups

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- test fixture with trailing whitespace on heading lines for reproducer test

## Implementation Notes
The bug is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. Two changes are needed:

1. **Heading extraction fix**: In the convention lookup loop, change `section_name = line[3:]` to `section_name = line[3:].strip()`. This normalizes heading names by removing trailing whitespace so that headings like `## Migration Patterns  ` are stored as `"Migration Patterns"` in the conventions dictionary.

2. **Warning for unmatched conventions**: In the convention-aware task enrichment section, add a warning log when `convention_name` is not found in `discovered_conventions`. This provides a diagnostic signal instead of silently dropping conventions. The current code:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
   ```
   Should add an `else` branch that logs a warning, for example:
   ```python
   else:
       log.warning(f"Convention '{convention_name}' not found in discovered conventions")
   ```

**Existing patterns**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` demonstrates the expected fixture format. The new trailing-whitespace fixture should follow the same structure but include trailing spaces on heading lines.

**Reproducer test input**: Create a `CONVENTIONS.md` fixture containing:
```
## Migration Patterns  
Add Index::create() for all FK columns.
```
(Note the two trailing spaces after "Migration Patterns".)

When run through the heading extraction logic, the lookup for `"Migration Patterns"` must succeed and the generated task's Implementation Notes must include the convention reference.

Fixes ACME-500.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing conventions fixture format to follow when creating the trailing-whitespace test fixture

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a CONVENTIONS.md fixture with trailing whitespace on a heading causes the convention to be silently dropped before the fix, and correctly included after the fix
- [ ] The heading extraction logic in convention conformance analysis strips trailing whitespace from extracted section names (e.g., `line[3:].strip()`)
- [ ] A warning is logged when a convention name lookup fails during task enrichment, instead of silently skipping
- [ ] Conventions with trailing whitespace on headings are correctly matched and included in generated task Implementation Notes
- [ ] No regression in existing plan-feature tests and evals

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  `), run the convention conformance analysis, and assert that (a) the convention is discovered under the clean key `"Migration Patterns"`, and (b) the generated task's Implementation Notes include the expected reference `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- [ ] Edge case test: verify headings with various whitespace patterns (single space, multiple spaces, tab characters) are all normalized correctly
- [ ] Existing eval coverage: verify that the existing plan-feature evals (which use headings without trailing whitespace) continue to pass unchanged

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction uses `line[3:]` which does not strip trailing whitespace. The subsequent exact-match convention lookup (`if convention_name in discovered_conventions`) fails because `"Migration Patterns  "` != `"Migration Patterns"`. The convention is silently dropped with no warning logged.
