# Jira API Metadata (jira.create_issue — not executed)

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueTypeName: "Task",
  summary: "Fix plan-feature silently dropping CONVENTIONS.md sections with trailing whitespace in headings",
  description: <task description below>,
  additional_fields: {
    "labels": ["ai-generated-jira"]
  }
)
```

- Project key: `ACME`
- Issue type: `Task`
- Labels: `ai-generated-jira`

Follow-up calls:
- Step 5b: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-500")`. The Task blocks the Bug.
- Step 5c: re-fetch `<created-task-key>`, run `python3 scripts/sha256-digest.py` on the persisted description, then post the standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote).

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. When a `CONVENTIONS.md` heading line has trailing whitespace
(e.g., `## Migration Patterns  `), plan-feature's convention conformance analysis stores the
section under a name that keeps the whitespace (`"Migration Patterns  "`). The task enrichment
step uses an exact-match lookup on the normalized name, so the lookup misses and the convention
is left out of generated task Implementation Notes with no warning. This task normalizes the
section-name extraction and lookup, and adds a warning on unmatched conventions, so that
repository conventions are applied reliably.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — normalize CONVENTIONS.md heading extraction in the convention conformance analysis, normalize the lookup key in convention-aware task enrichment, and warn on unmatched conventions

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — reproducer fixture: a CONVENTIONS.md whose `## Migration Patterns  ` heading has trailing whitespace

## Implementation Notes
Fixes ACME-500.

**Reproducer first.** Before changing the skill, add a plan-feature eval that reproduces the bug:
- **Triggering input:** a CONVENTIONS.md fixture containing
  ```
  ## Migration Patterns  
  Add Index::create() for all FK columns.
  ```
  The heading has two trailing spaces. Pair it with a feature that requires a database
  migration with foreign keys (as with `/plan-feature ACME-100` in the bug).
- **Behavior before the fix (Actual Result):** the generated task's Implementation Notes contain no
  reference to Migration Patterns, and no warning is emitted.
- **Behavior after the fix (Expected Result):** the generated task's Implementation Notes contain
  `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- Model the fixture on `evals/plan-feature/files/conventions-mock.md`, the existing conventions
  fixture, which has no trailing whitespace. Register the new eval case in
  `evals/plan-feature/evals.json` with an assertion on the expected Implementation Notes line.

**Fix: convention conformance analysis** in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.
The current extraction logic is equivalent to:
```python
if line.startswith('## '):
    section_name = line[3:]
```
Update the instructions so that the extracted section name is normalized by stripping leading and
trailing whitespace, including tabs and the `\r` left by CRLF line endings (equivalent to
`line[3:].strip()`). The stored key for `## Migration Patterns  ` must be exactly
`"Migration Patterns"`.

**Fix: convention-aware task enrichment** in the same file. The lookup
`if convention_name in discovered_conventions:` must compare normalized names on both sides.
When an expected convention does not match any discovered section, emit a visible warning
(e.g., "Convention '<name>' not found in CONVENTIONS.md") instead of skipping it silently.

**Scope notes**
- There is one root cause. Do not refactor unrelated parts of plan-feature.
- The repository has no CONVENTIONS.md at its root, so there are no extra repo conventions to apply.
- No data migration is required. The affected output is computed per plan-feature run and is not persisted.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing conventions fixture. Copy its structure for the trailing-whitespace reproducer fixture
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md::Convention-aware task enrichment` — existing `Per CONVENTIONS.md §<name>: <action>` note format. Reuse it unchanged so the expected output matches

## Acceptance Criteria
- [ ] A reproducer eval exists using a CONVENTIONS.md fixture with heading `## Migration Patterns  ` (trailing whitespace). It fails before the fix (the convention is missing from Implementation Notes) and passes after the fix
- [ ] CONVENTIONS.md section names are normalized during extraction (leading/trailing whitespace, tabs, and `\r` stripped), so `## Migration Patterns  ` is stored as `Migration Patterns`
- [ ] The convention-aware task enrichment lookup matches on normalized names, and the generated Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- [ ] A warning is emitted when an expected convention is not matched, instead of the convention being dropped silently
- [ ] No regression: existing plan-feature evals (including `conventions-mock.md`-based cases) still pass

## Test Requirements
- [ ] Reproducer test: plan-feature eval using a CONVENTIONS.md with heading `## Migration Patterns  ` (two trailing spaces) and body `Add Index::create() for all FK columns.`, run on a feature that requires an FK migration. Assert that the generated task's Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` (absent before the fix, present after)
- [ ] Variant: a heading with a trailing tab and/or CRLF line ending (`## Migration Patterns\t\r`) also matches `Migration Patterns`
- [ ] Negative case: when an expected convention is not present in CONVENTIONS.md, a warning is emitted
- [ ] Existing plan-feature evals continue to pass unchanged

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with a heading that has trailing whitespace (`## Migration Patterns  ` followed by `Add Index::create() for all FK columns.`), run `/plan-feature ACME-100` on a feature requiring an FK migration, and inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention, and no warning or error is shown. The convention is dropped silently.
- **Root Cause**: plan-feature extracts CONVENTIONS.md section names with `line[3:]` without stripping whitespace, so `## Migration Patterns  ` becomes `"Migration Patterns  "`. The exact-match lookup in convention-aware task enrichment (`if convention_name in discovered_conventions`) then fails, with no warning on the miss.
