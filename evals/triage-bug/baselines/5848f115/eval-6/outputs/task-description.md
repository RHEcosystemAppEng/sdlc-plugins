## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature convention heading parser to strip trailing whitespace from CONVENTIONS.md section headings. Currently, `line[3:]` preserves trailing spaces, causing exact-match convention lookups to fail silently when headings contain trailing whitespace. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Add `.strip()` to the heading extraction expression `section_name = line[3:]` so that trailing whitespace is normalized before storing the convention key

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- Eval fixture with trailing whitespace on heading lines to cover this edge case

## Implementation Notes
The defect is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction loop currently reads:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]
        conventions[section_name] = current_section_content
```

Change `line[3:]` to `line[3:].strip()` to normalize trailing whitespace on extracted heading text.

The convention-aware task enrichment performs an exact-match lookup:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

After the heading extraction fix, this lookup will succeed for headings with trailing whitespace. Optionally, add a warning log when a convention name is expected but not found in `discovered_conventions`, to surface future mismatches rather than failing silently.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT include trailing whitespace on headings. Create a new fixture file that includes headings with trailing spaces to cover this edge case.

Reproducer test guidance:
- **Input:** A CONVENTIONS.md with `## Migration Patterns  ` (note trailing spaces) followed by `Add Index::create() for all FK columns.`
- **Before fix:** Looking up `"Migration Patterns"` in the conventions dictionary returns no match -- the key is `"Migration Patterns  "` with trailing spaces
- **After fix:** Looking up `"Migration Patterns"` returns the correct section content, and the generated task notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

## Acceptance Criteria
- [ ] Reproducer test: a test using a CONVENTIONS.md fixture with trailing whitespace on headings demonstrates that the convention is correctly matched and included in generated task output (fails before fix, passes after)
- [ ] The heading extraction in plan-feature's convention conformance analysis strips trailing whitespace from section names via `.strip()`
- [ ] Previously passing plan-feature eval tests continue to pass (no regression)

## Test Requirements
- [ ] Reproducer test: create a test that uses a CONVENTIONS.md fixture containing `## Migration Patterns  ` (with trailing spaces) and asserts that the generated task's Implementation Notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.` -- this test must fail before the fix and pass after
- [ ] Verify that headings without trailing whitespace continue to match correctly (regression guard)
- [ ] Verify that headings with various whitespace patterns (tabs, multiple spaces, mixed) are handled

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `section_name = line[3:]` does not strip trailing whitespace, producing dictionary keys like `"Migration Patterns  "` that fail exact-match lookups against the expected `"Migration Patterns"`.
