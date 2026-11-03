# Jira API Metadata (jira.create_issue parameters)

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueTypeName: "Task",
  summary: "Fix plan-feature dropping CONVENTIONS.md sections whose headings have trailing whitespace",
  description: <task description body below>,
  additional_fields: {
    "labels": ["ai-generated-jira"]
  }
)
```

| Parameter | Value |
|---|---|
| Project key | ACME |
| Issue type | Task |
| Labels | `ai-generated-jira` |
| Summary | Fix plan-feature dropping CONVENTIONS.md sections whose headings have trailing whitespace |

Follow-up operations:
- **Step 5b – Link:** `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-500")`, so the Task blocks the Bug.
- **Step 5c – Digest:** re-fetch `<created-task-key>`, write the description to `/tmp/desc-<task-key>.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, and post `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment with no footnote.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. plan-feature's convention conformance analysis silently drops `CONVENTIONS.md`
sections whose `##` heading line has trailing whitespace (e.g., `## Migration Patterns  `). The
heading is extracted with `line[3:]` and never stripped, so it is stored as `"Migration Patterns  "`.
The exact-match lookup in convention-aware task enrichment then fails, and the convention is left
out of generated tasks' Implementation Notes with no warning. This task normalizes heading names
on extraction and lookup, makes failed matches visible, and adds a reproducer eval for the case.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`: normalize (strip) extracted `CONVENTIONS.md` heading names in the convention conformance analysis, normalize the lookup name in convention-aware task enrichment, and warn when an expected convention cannot be matched

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md`: reproducer fixture, a CONVENTIONS.md whose `## Migration Patterns  ` heading has trailing whitespace and whose body is `Add Index::create() for all FK columns.`

## Implementation Notes
Fixes ACME-500.

**Defect location:** `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention conformance
analysis. The heading extraction is currently:
```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```
`line[3:]` keeps trailing spaces, tabs, and any CRLF `\r`. Change the extraction to normalize the
name, i.e. `section_name = line[3:].strip()`. If the logic is written as natural-language
instructions in SKILL.md, add an explicit instruction to trim leading and trailing whitespace from
heading text before using it as a convention name.

**Manifestation site:** same file, convention-aware task enrichment:
```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```
Normalize `convention_name` the same way before the membership check, so both sides of the
comparison are whitespace-insensitive. Do not add an `else` that silently continues. When a
convention that applies to the task cannot be found in `discovered_conventions`, emit a visible
warning (e.g., "Convention '<name>' expected but not found in CONVENTIONS.md"). This prevents the
silent-drop behavior the bug reports.

**Reproducer guidance (from the Bug's Steps to Reproduce):**
- **Triggering input:** a `CONVENTIONS.md` containing the heading line `## Migration Patterns  `
  (two trailing spaces), followed by `Add Index::create() for all FK columns.`, plus a feature
  (modelled on `/plan-feature ACME-100`) that needs a database migration with foreign keys.
- **Before the fix (Actual Result):** the generated task's Implementation Notes contain no
  reference to the Migration Patterns convention, and no warning is shown.
- **After the fix (Expected Result):** the generated task's Implementation Notes contain
  `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- Make sure the trailing whitespace in the fixture survives editors and formatters. Check that
  `.editorconfig` or pre-commit `trailing-whitespace` hooks do not strip it, and add an exclusion
  for the fixture file if they would.

**Existing test patterns:** base the new fixture on `evals/plan-feature/files/conventions-mock.md`.
It uses the same structure but has clean headings, which is why current evals miss this case. Wire
the new fixture into the plan-feature eval definitions the same way the existing fixture is wired.

**No data migration needed:** the conventions map is computed on each plan-feature run and is never
written to a database (no persistence boundary found during triage).

**Conventions:** the acme-backend repository has no `CONVENTIONS.md` at its root, so no
repo-specific conventions apply.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md::convention conformance analysis`: the existing heading-extraction loop; fix it in place rather than adding a parallel parser
- `evals/plan-feature/files/conventions-mock.md`: the existing conventions eval fixture; reuse its structure for the trailing-whitespace reproducer fixture

## Acceptance Criteria
- [ ] Reproducer: a plan-feature eval using a CONVENTIONS.md whose `## Migration Patterns  ` heading has trailing whitespace produces a task whose Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` The eval fails before the fix and passes after it.
- [ ] Extracted CONVENTIONS.md heading names are stripped of leading and trailing whitespace (spaces, tabs, `\r`) before being stored as convention keys
- [ ] The convention-aware task enrichment lookup normalizes the convention name before matching, so the match is whitespace-insensitive
- [ ] When an applicable convention cannot be matched, plan-feature emits a visible warning instead of silently dropping it
- [ ] No regression: existing plan-feature evals, including the clean-heading `conventions-mock.md` fixture, still produce the same convention references

## Test Requirements
- [ ] Reproducer eval: run plan-feature with the `conventions-trailing-whitespace-mock.md` fixture (heading `## Migration Patterns  `, body `Add Index::create() for all FK columns.`) on a feature that needs a migration with foreign keys. Assert that the generated task's Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns`. Before the fix this assertion fails (the convention is silently absent, as in the Actual Result). After the fix it passes (as in the Expected Result).
- [ ] Cover the other whitespace variants: a heading with a trailing tab and a heading with a CRLF line ending both resolve to the clean convention name
- [ ] Assert that a warning is produced when an applicable convention is not found in CONVENTIONS.md
- [ ] Re-run the existing plan-feature eval suite and confirm that the results for the clean-heading fixture do not change

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with the heading `## Migration Patterns  ` (trailing whitespace) followed by `Add Index::create() for all FK columns.`, run `/plan-feature ACME-100` on a feature that needs a database migration with foreign keys, then inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention, and no warning or error is shown. The convention is silently dropped.
- **Root Cause**: plan-feature extracts CONVENTIONS.md heading names with `line[3:]` and does not strip whitespace, so `## Migration Patterns  ` is stored as `"Migration Patterns  "`. The exact-match lookup `if convention_name in discovered_conventions` in task enrichment then fails against `"Migration Patterns"`, and there is no warning path, so the convention is omitted silently.
