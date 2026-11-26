# Jira API Metadata (jira.create_issue parameters)

```json
{
  "cloudId": "mock-cloud-id-for-eval",
  "projectKey": "ACME",
  "issueTypeName": "Task",
  "summary": "Fix plan-feature dropping CONVENTIONS.md sections whose headings have trailing whitespace",
  "contentFormat": "markdown",
  "additional_fields": {
    "labels": ["ai-generated-jira"]
  }
}
```

Follow-up operations:
- Step 5b: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-500")`. The Task blocks the Bug.
- Step 5c: re-fetch the created Task, compute the digest with `python3 scripts/sha256-digest.py`, and post `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment with no footnote.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. The plan-feature skill drops a `CONVENTIONS.md` convention without any warning
when the convention's `##` heading line has trailing whitespace (for example
`## Migration Patterns  `). The heading-extraction step keeps the trailing whitespace in the
section name. The task-enrichment step's exact-match lookup on the clean name then misses.
Generated tasks therefore leave out conventions they should cite. This task normalizes the
extracted heading names, adds a warning for unmatched conventions, and adds a reproducer eval
that covers the edge case.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — strip whitespace from extracted `CONVENTIONS.md` heading names in the convention conformance analysis, and log a warning in convention-aware task enrichment when a convention lookup misses
- `evals/plan-feature/evals.json` — add a reproducer eval case for headings with trailing whitespace

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — CONVENTIONS.md fixture whose `## Migration Patterns  ` heading has trailing whitespace (reproducer input)

## Implementation Notes
Fixes ACME-500.

**Reproducer first.** Before changing the skill, add the reproducer eval:
- Trigger input: a `CONVENTIONS.md` fixture containing
  ```
  ## Migration Patterns  
  Add Index::create() for all FK columns.
  ```
  (two trailing spaces after `Patterns`; consider also a heading with a trailing tab or `\r`).
  Pair it with a feature that needs a database migration with foreign keys, mirroring the bug's
  `/plan-feature ACME-100` scenario.
- Current (buggy) behavior: the generated task's Implementation Notes do not mention the
  Migration Patterns convention, and no warning is printed.
- Correct behavior after the fix: the Implementation Notes contain
  `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` with no
  trailing whitespace in the section name.
- Model the fixture on the existing `evals/plan-feature/files/conventions-mock.md`. Keep its
  structure and add trailing whitespace to the heading under test.

**Fix location.** Edit `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`:
1. Convention conformance analysis: the heading-extraction logic currently does
   `section_name = line[3:]`. Change it to normalize the name, e.g. `section_name = line[3:].strip()`.
   This removes trailing spaces, tabs, and the `\r` left by `split('\n')` on CRLF files. Update
   the prose instructions next to it so the skill explicitly says heading names are compared
   after trimming whitespace.
2. Convention-aware task enrichment: the lookup `if convention_name in discovered_conventions:`
   has no `else`. Add guidance to log a warning when an applicable convention cannot be matched,
   so a mismatch is never silent again.

**Scope.** One root cause in one file. No other skills share this extraction loop. The
conventions map is built in memory on every run and never persisted, so no data migration is
needed. Tasks generated earlier that are missing the convention can be regenerated.

The target repository has no `CONVENTIONS.md`, so no repository-specific conventions apply.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing plan-feature conventions fixture; the template for the new trailing-whitespace fixture
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md::Convention-aware task enrichment` — existing `Per CONVENTIONS.md §<name>: <action>` note format that the reproducer must assert against

## Acceptance Criteria
- [ ] Reproducer: a plan-feature eval with `CONVENTIONS.md` heading `## Migration Patterns  ` (trailing whitespace) fails before the fix (convention missing from Implementation Notes) and passes after the fix (Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`)
- [ ] Heading names extracted from `CONVENTIONS.md` have leading and trailing whitespace (spaces, tabs, `\r`) stripped before they are stored or matched
- [ ] When an applicable convention cannot be matched during task enrichment, plan-feature logs a warning instead of skipping it silently
- [ ] Section names in generated convention references contain no trailing whitespace
- [ ] No regression: all existing plan-feature evals (including the `conventions-mock.md` cases) still pass

## Test Requirements
- [ ] Reproducer eval: fixture `CONVENTIONS.md` contains `## Migration Patterns  ` followed by `Add Index::create() for all FK columns.`; run plan-feature on a feature that needs an FK migration; assert the generated task's Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` exactly (section name `Migration Patterns`, no trailing spaces). Before the fix, this assertion fails because the reference is absent
- [ ] Variant assertion: a heading with a trailing tab or CRLF line ending (`## Migration Patterns\r`) is also matched and cited
- [ ] Warning assertion: when an applicable convention is not found in `CONVENTIONS.md`, the output includes a warning instead of omitting it silently
- [ ] Re-run the existing plan-feature conventions evals to confirm unchanged output for headings without trailing whitespace

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with heading `## Migration Patterns  ` (trailing whitespace) and body `Add Index::create() for all FK columns.`; run `/plan-feature ACME-100` on a feature that needs a DB migration with foreign keys; inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention; no warning or error is shown.
- **Root Cause**: The convention lookup in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` extracts heading names with `line[3:]` and does not strip whitespace, so `"Migration Patterns  "` fails the exact-match lookup for `"Migration Patterns"` in task enrichment. The miss is skipped without a warning.
