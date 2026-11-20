# Jira API Metadata (jira.create_issue parameters)

```json
{
  "cloudId": "mock-cloud-id-for-eval",
  "projectKey": "ACME",
  "issueTypeName": "Task",
  "summary": "Fix plan-feature dropping CONVENTIONS.md sections whose headings have trailing whitespace",
  "description": "<task description body below>",
  "additional_fields": {
    "labels": ["ai-generated-jira"]
  }
}
```

Follow-up operations:
- Step 5b: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-500")` — the Task blocks the Bug.
- Step 5c: re-fetch the created Task, compute digest with `python3 scripts/sha256-digest.py`, and post standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote).

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. plan-feature's convention conformance analysis extracts CONVENTIONS.md section
names with `line[3:]`, which preserves trailing whitespace. A heading such as
`## Migration Patterns  ` is stored as `"Migration Patterns  "`, so the exact-match lookup in
convention-aware task enrichment fails and the convention is silently omitted from generated
task Implementation Notes. This task normalizes heading names at extraction time, makes the
lookup whitespace-robust, surfaces a warning when a convention cannot be matched, and adds a
reproducer eval covering headings with trailing whitespace.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — normalize CONVENTIONS.md heading extraction (strip trailing whitespace, tabs, `\r`) in the convention conformance analysis; compare normalized names in convention-aware task enrichment; warn instead of silently skipping unmatched conventions
- `evals/plan-feature/evals.json` — add an eval case for the trailing-whitespace reproducer

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — reproducer fixture: CONVENTIONS.md content with `## Migration Patterns  ` (trailing spaces) and `Add Index::create() for all FK columns.`

## Implementation Notes
Fixes ACME-500.

**Reproducer (write first):**
- Trigger input: a CONVENTIONS.md whose heading line has trailing whitespace —
  `## Migration Patterns  ` followed by `Add Index::create() for all FK columns.` — combined with
  a feature that requires a database migration with foreign keys (as in `/plan-feature ACME-100`).
- Buggy behavior (Actual Result) to observe before the fix: the generated task's Implementation
  Notes contain no reference to the Migration Patterns convention, and no warning is emitted.
- Correct behavior (Expected Result) to assert after the fix: the Implementation Notes contain
  `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` — note the
  section name has no trailing whitespace.
- Model the fixture on `evals/plan-feature/files/conventions-mock.md` (same structure, only the
  heading whitespace differs) and add a matching entry in `evals/plan-feature/evals.json` with
  assertions in the existing style.

**Fix:**
- In `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention conformance analysis, the
  heading extraction currently does:
  ```python
  if line.startswith('## '):
      section_name = line[3:]
  ```
  Change the guidance so the section name is normalized — e.g. `line[3:].strip()` — removing
  trailing spaces, tabs, and `\r` (CRLF files). Normalize at extraction so every downstream
  consumer receives clean keys.
- In convention-aware task enrichment (`if convention_name in discovered_conventions:` →
  `notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")`), compare normalized names
  so the `§<name>` reference never carries stray whitespace.
- Replace the silent miss with an explicit warning (e.g. "Convention '<name>' referenced but not
  found in CONVENTIONS.md") so future mismatches are visible rather than silently dropped.
- Keep the change scoped to heading normalization and the miss warning; do not alter how section
  content is captured.

**Conventions:** the target repository has no CONVENTIONS.md at its root; follow the existing
SKILL.md and eval fixture style.

**Persistence:** none — the convention map is computed in-memory per plan-feature run; no data
migration required.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md::convention conformance analysis` — existing heading extraction loop; fix in place rather than adding a new parser
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md::convention-aware task enrichment` — existing `Per CONVENTIONS.md §<name>: <action>` note format to preserve
- `evals/plan-feature/files/conventions-mock.md` — existing fixture to copy as the basis of the reproducer fixture

## Acceptance Criteria
- [ ] Reproducer: a plan-feature eval using a CONVENTIONS.md with `## Migration Patterns  ` (trailing whitespace) asserts that the generated task's Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` — this fails before the fix and passes after
- [ ] CONVENTIONS.md heading extraction in plan-feature strips trailing whitespace (spaces, tabs, `\r`) from section names
- [ ] Convention-aware task enrichment matches conventions regardless of trailing whitespace on the source heading, and emitted `§<name>` references contain no trailing whitespace
- [ ] When a convention cannot be matched, plan-feature emits a visible warning instead of silently dropping it
- [ ] No regression: all existing plan-feature evals (including the `conventions-mock.md` scenario) continue to pass

## Test Requirements
- [ ] Reproducer test: new fixture `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` containing `## Migration Patterns  ` (two trailing spaces) followed by `Add Index::create() for all FK columns.`, run against a feature requiring a migration with foreign keys. Assert the generated task's Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` Before the fix: the convention reference is absent (Actual Result). After the fix: it is present with the clean section name (Expected Result)
- [ ] Additional case: heading with a trailing tab and/or CRLF line ending (`## Migration Patterns\r`) is also matched
- [ ] Re-run the existing `conventions-mock.md` plan-feature eval to confirm headings without trailing whitespace still match

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with heading `## Migration Patterns  ` (trailing whitespace) and body `Add Index::create() for all FK columns.`; run `/plan-feature ACME-100` on a feature requiring a DB migration with foreign keys; inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention; no warning or error is shown — the convention is silently dropped.
- **Root Cause**: plan-feature extracts CONVENTIONS.md heading names with `line[3:]` without stripping whitespace, so `## Migration Patterns  ` becomes the key `"Migration Patterns  "`; the exact-match lookup in convention-aware task enrichment then fails and the miss is not reported.
