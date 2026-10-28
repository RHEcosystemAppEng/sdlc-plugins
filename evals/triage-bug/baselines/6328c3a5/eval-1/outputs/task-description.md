# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: `["ai-generated-jira"]`

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace, preventing silent convention drops when `CONVENTIONS.md` headings contain trailing spaces. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- fix heading extraction to strip trailing whitespace from section names

## Implementation Notes
The defect is in the convention heading extraction logic within `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code extracts heading text with:

```python
section_name = line[3:]
```

This does not strip trailing whitespace. When a `CONVENTIONS.md` heading line is `## Migration Patterns  \n`, the extracted key is `"Migration Patterns  "` (with trailing spaces), which fails the exact-match lookup in the convention-aware task enrichment step:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Fix**: Change the extraction to:

```python
section_name = line[3:].strip()
```

This normalizes heading names at extraction time, so downstream exact-match comparisons succeed regardless of trailing whitespace in the source file.

Consider also adding a debug log or warning when trailing whitespace is detected on a heading line, to aid future troubleshooting.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` provides the pattern for convention test data. Use this as a reference when creating the reproducer test fixture.

Fixes ACME-500.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing convention fixture; extend or create a variant with trailing whitespace on headings for the reproducer test

## Acceptance Criteria
- [ ] A reproducer test exists that creates a `CONVENTIONS.md` fixture with trailing whitespace on a section heading (e.g., `## Migration Patterns  `), runs the convention extraction, and asserts the convention is correctly matched and included in the generated task output. The test fails before the fix and passes after.
- [ ] The heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` strips trailing whitespace from extracted section names (e.g., using `.strip()`).
- [ ] Conventions with trailing whitespace on headings are no longer silently dropped -- they appear in generated task Implementation Notes as expected.
- [ ] No regression in existing plan-feature eval tests.

## Test Requirements
- [ ] Reproducer test: create a convention fixture file with trailing whitespace on a heading line (e.g., `## Migration Patterns  ` with two trailing spaces). Run the convention extraction and task enrichment logic against this fixture. Assert that the generated task's Implementation Notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.` The test must fail before the fix is applied and pass after.
- [ ] Verify that headings without trailing whitespace continue to be extracted and matched correctly (no regression).
- [ ] Verify that headings with various whitespace patterns (tabs, mixed spaces, leading whitespace) are handled correctly.

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, causing exact-match lookups against convention names to fail silently.
