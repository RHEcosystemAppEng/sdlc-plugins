# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira

Link operation (`jira.create_issue_link`):
- **Link type**: Blocks
- **Inward issue (blocker)**: ACME-<created-task-key>
- **Outward issue (blocked)**: ACME-500

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from `CONVENTIONS.md` section headings during extraction. Currently, headings with trailing spaces (e.g., `## Migration Patterns  `) are stored with the whitespace intact, causing exact-match lookups to silently fail and drop the convention from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Fix heading extraction in convention conformance analysis to strip trailing whitespace from extracted section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — Test fixture with trailing whitespace on convention headings to cover this edge case

## Implementation Notes
The defect is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction logic currently uses:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

This must be changed to:

```python
section_name = line[3:].strip()  # Strips trailing whitespace from heading names
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) are normalized to `"Migration Patterns"` before being stored in the conventions dictionary. The downstream exact-match lookup in the convention-aware task enrichment section (`if convention_name in discovered_conventions`) will then succeed regardless of trailing whitespace in the source file.

**Reproducer test guidance:**

The reproducer test should create a `CONVENTIONS.md` fixture with trailing whitespace on a heading line, such as:
```
## Migration Patterns  
Add Index::create() for all FK columns.
```

The test should verify that:
- The convention IS matched despite trailing whitespace on the heading
- The generated task's Implementation Notes include the expected reference: `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`

**Existing test patterns:**
- The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` can be used as a template for the new trailing-whitespace fixture. Copy it and add trailing spaces to heading lines.

**Additional consideration:**
- Consider adding a warning log when whitespace is stripped from a heading, to surface `CONVENTIONS.md` formatting issues to users.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — Existing convention fixture that can serve as a template for the trailing-whitespace variant

## Acceptance Criteria
- [ ] A reproducer test exists that creates a `CONVENTIONS.md` with trailing whitespace on headings, runs convention lookup, and asserts that the convention is correctly matched (fails before fix, passes after fix)
- [ ] The heading extraction in the convention conformance analysis applies `.strip()` to normalize section names, so that `## Migration Patterns  ` is stored as `"Migration Patterns"`
- [ ] Conventions with trailing whitespace on headings are included in generated task descriptions with the correct `Per CONVENTIONS.md §<section>: ...` format
- [ ] No regression in existing plan-feature evals and tests

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on at least one section heading (e.g., `## Migration Patterns  `), run the plan-feature convention conformance analysis against it, and assert that the convention appears in the generated task's Implementation Notes as `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- [ ] Verify that conventions WITHOUT trailing whitespace continue to work correctly (no regression)
- [ ] Edge case: heading with only spaces after the section name (e.g., `##    `) should be handled gracefully

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: The convention heading extraction uses `line[3:]` without `.strip()`, storing keys with trailing whitespace that fail exact-match lookups against clean convention names.
