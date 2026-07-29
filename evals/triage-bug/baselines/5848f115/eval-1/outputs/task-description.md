# Jira API Metadata

The following parameters would be passed to `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira
- **Summary**: Fix plan-feature convention heading extraction to strip trailing whitespace

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing
whitespace from CONVENTIONS.md section headings during extraction. Currently,
headings with trailing spaces (e.g., `## Migration Patterns  `) are stored with
those spaces in the conventions dictionary, causing exact-match lookups to fail
silently. This results in conventions being dropped from generated task descriptions
without any warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Fix heading extraction in the convention conformance analysis section to strip trailing whitespace from parsed heading names

## Implementation Notes
The defect is in the convention conformance analysis section of
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction logic
currently uses:

```python
section_name = line[3:]
```

This preserves any trailing whitespace from the heading line. Change to:

```python
section_name = line[3:].strip()
```

This normalizes the section name regardless of trailing whitespace in the source
CONVENTIONS.md file.

The downstream convention-aware task enrichment step performs exact-match comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

After the fix, this match will succeed because both the stored key and the lookup key
will be whitespace-normalized.

**Reproducer test guidance**: Create a test fixture CONVENTIONS.md with trailing
whitespace on a heading line. The specific input that triggers the bug is a heading
like `## Migration Patterns  ` (with trailing spaces). Before the fix, the convention
conformance analysis will fail to match this heading and silently skip it (the Actual
Result). After the fix, the analysis should match the heading and include it in the
generated task's Implementation Notes with a reference like
`Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns`
(the Expected Result).

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not
include trailing whitespace on headings -- use it as a reference for the fixture
format, but add trailing whitespace to at least one heading to cover this edge case.

Optionally, add a warning log when a convention name referenced during task enrichment
is not found in the discovered conventions dictionary, to surface similar matching
failures in the future.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a CONVENTIONS.md fixture with trailing whitespace on a heading causes the convention to be silently dropped (fails before fix, passes after fix)
- [ ] Heading extraction in the convention conformance analysis strips trailing whitespace from section names
- [ ] Conventions with trailing whitespace on headings in CONVENTIONS.md are correctly matched and included in generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  `), run convention conformance analysis, and assert the convention is matched and included in the output. The test should assert the output contains `Per CONVENTIONS.md Migration Patterns:` (or equivalent convention reference). Before the fix this test must fail; after the fix it must pass.
- [ ] Verify that headings without trailing whitespace continue to work correctly (no regression)
- [ ] Verify that headings with mixed whitespace (tabs, multiple spaces) are also handled by the strip

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction uses `line[3:]` which preserves trailing whitespace from the heading line. The downstream exact-match lookup fails because the stored key `"Migration Patterns  "` does not match the clean lookup key `"Migration Patterns"`.
