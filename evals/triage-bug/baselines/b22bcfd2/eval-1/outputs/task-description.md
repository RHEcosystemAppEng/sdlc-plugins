# Jira API Metadata

The following parameters would be passed to `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: `["ai-generated-jira"]`

```
jira.create_issue(
  project_key="ACME",
  issue_type="Task",
  summary="Fix trailing-whitespace handling in plan-feature convention heading extraction",
  labels=["ai-generated-jira"],
  description=<below>
)
```

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from `CONVENTIONS.md` heading lines during extraction. Currently, `line[3:]` preserves trailing spaces, causing exact-match convention lookups to fail silently when headings have trailing whitespace. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Update heading extraction logic to strip trailing whitespace from `line[3:]`

## Files to Create
- `evals/plan-feature/files/conventions-whitespace-mock.md` — Test fixture with trailing whitespace on convention headings

## Implementation Notes
The root cause is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction logic:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

must be changed to:

```python
section_name = line[3:].strip()  # Strips trailing (and leading) whitespace
```

This ensures that a heading like `## Migration Patterns  ` is normalized to `"Migration Patterns"` before being stored in the `conventions` dictionary. The downstream exact-match lookup in the convention-aware task enrichment will then match correctly.

**Reproducer test guidance** (derived from Steps to Reproduce):
- Create a `CONVENTIONS.md` fixture containing a heading with trailing whitespace: `## Migration Patterns  ` (two trailing spaces)
- The fixture should include convention content below the heading (e.g., `Add Index::create() for all FK columns.`)
- Run the convention lookup logic against this fixture
- Assert that the convention IS matched and included in the generated task's Implementation Notes
- Before the fix: the test should FAIL because `"Migration Patterns  "` does not match `"Migration Patterns"`
- After the fix: the test should PASS because `.strip()` normalizes the heading

**Existing test reference**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings. The new fixture should be modeled after this file but with trailing whitespace added to at least one heading.

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test: add a test with a `CONVENTIONS.md` fixture containing trailing whitespace on a heading line (e.g., `## Migration Patterns  `). The test must assert that the convention is matched and included in the generated task output. This test should fail before the fix and pass after.
- [ ] Fix heading extraction: update `line[3:]` to `line[3:].strip()` in the convention conformance analysis to strip trailing whitespace from extracted heading names.
- [ ] No regression in existing tests: all existing plan-feature evals continue to pass.

## Test Requirements
- [ ] Reproducer test for trailing-whitespace heading extraction: create a conventions fixture with trailing whitespace on the `## Migration Patterns  ` heading. Run the plan-feature convention lookup and assert that the convention name `"Migration Patterns"` is found in the extracted conventions dictionary AND that the generated task's Implementation Notes contain `Per CONVENTIONS.md` with the convention reference. The test must fail before the fix (convention silently dropped) and pass after (convention correctly matched).
- [ ] Verify that headings without trailing whitespace continue to be extracted correctly (no regression from adding `.strip()`).
- [ ] Verify that headings with mixed whitespace (tabs, multiple spaces) are also handled correctly.

## Verification Commands
- `python3 -m pytest evals/plan-feature/` — all plan-feature evals pass, including the new trailing-whitespace reproducer

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include the convention reference (e.g., `Per CONVENTIONS.md "Migration Patterns": add Index::create() for all FK columns.`).
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: The heading extraction logic `line[3:]` in the plan-feature convention conformance analysis does not strip trailing whitespace. This causes exact-match convention lookups to fail silently when `CONVENTIONS.md` headings have trailing spaces.
