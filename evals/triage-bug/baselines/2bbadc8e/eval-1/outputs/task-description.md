# Jira API Metadata

Parameters for `jira.create_issue`:

| Parameter | Value |
|---|---|
| Project key | ACME |
| Issue type | Task |
| Labels | ai-generated-jira |

```
jira.create_issue(
  project_key="ACME",
  summary="Fix trailing whitespace handling in CONVENTIONS.md heading extraction",
  issue_type="Task",
  additional_fields={
    "labels": ["ai-generated-jira"]
  },
  description=<below>
)
```

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace
from CONVENTIONS.md headings. Currently, `line[3:]` preserves trailing whitespace,
causing convention lookups to silently fail when headings have trailing spaces. This
results in generated task descriptions omitting conventions that should have been included.

Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Fix heading extraction to strip trailing whitespace from `line[3:]`

## Implementation Notes
The defect is in the convention heading extraction logic within the plan-feature skill.
The current code:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

must be changed to:

```python
section_name = line[3:].strip()  # Strips trailing whitespace from heading name
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) are
normalized to `"Migration Patterns"` before being stored in the `conventions` dictionary.

The downstream convention-aware task enrichment uses exact string matching:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

After the extraction fix, the lookup will succeed because both the stored key and the
query key will be normalized. Optionally, add defensive `.strip()` on the lookup side
as well for robustness.

**Existing test patterns**: The eval fixture at `evals/plan-feature/files/conventions-mock.md`
tests convention extraction but does NOT include trailing whitespace edge cases. The
reproducer test should add a fixture with trailing whitespace on headings to cover this gap.

No CONVENTIONS.md exists at the repository root, so no repository-level conventions apply.

No data migration is needed -- convention references are computed at task-generation time,
not persisted to a database.

## Acceptance Criteria
- [ ] A reproducer test exists that creates a CONVENTIONS.md fixture with trailing whitespace on headings (e.g., `## Migration Patterns  `), runs the convention extraction, and asserts the heading name is trimmed -- this test must fail before the fix and pass after
- [ ] The heading extraction logic uses `line[3:].strip()` (or equivalent) to normalize extracted section names
- [ ] Conventions with trailing whitespace on headings are correctly matched during task enrichment and appear in generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create an eval fixture `CONVENTIONS.md` with trailing whitespace on at least one `## ` heading (e.g., `## Migration Patterns  ` with two trailing spaces); run the convention extraction logic against this fixture; assert that the extracted section name equals `"Migration Patterns"` (trimmed, no trailing spaces); assert that the generated task's Implementation Notes include the expected convention reference `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns`
- [ ] Edge case test: verify headings with various whitespace patterns (tabs, mixed spaces, newlines) are all normalized correctly
- [ ] Regression test: verify that headings without trailing whitespace continue to work correctly after the fix

## Verification Commands
- Run plan-feature eval suite to confirm no regressions
- Run the new reproducer test to confirm the fix resolves the trailing whitespace issue

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction uses `line[3:]` which preserves trailing whitespace from CONVENTIONS.md headings. The downstream convention lookup performs an exact string match, which fails because the stored key includes trailing spaces that the query key does not have.
