# Jira API Metadata (jira.create_issue)

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
- Step 5b: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-500")` — Task blocks Bug.
- Step 5c: re-fetch the created task, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, post standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote).

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. plan-feature's convention conformance analysis extracts `CONVENTIONS.md` section
names with `line[3:]` and does not trim trailing whitespace. A heading such as
`## Migration Patterns  ` is stored as `"Migration Patterns  "`, so the exact-match lookup in the
convention-aware task enrichment step fails and the convention is silently omitted from generated
task Implementation Notes. This task normalizes extracted heading names so conventions match
regardless of trailing whitespace, warns when a convention cannot be matched, and adds a
reproducer eval covering the edge case.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — normalize (trim) heading text in the convention conformance analysis heading extraction; make the convention-aware task enrichment lookup whitespace-tolerant and emit a warning instead of silently dropping unmatched conventions
- `evals/plan-feature/evals.json` — add a reproducer eval case for trailing-whitespace headings

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — CONVENTIONS.md fixture variant with `## Migration Patterns  ` (trailing spaces) followed by `Add Index::create() for all FK columns.`

## Implementation Notes
Fixes ACME-500.

**Reproducer first** (write before changing SKILL.md, confirm it fails):
- Trigger input: a CONVENTIONS.md whose heading line has trailing whitespace —
  `## Migration Patterns  ` / `Add Index::create() for all FK columns.` — and a feature
  (e.g., ACME-100) that requires a database migration with foreign keys.
- Pre-fix (incorrect) behavior to observe: generated task Implementation Notes contain no
  reference to Migration Patterns; no warning is emitted.
- Post-fix (correct) behavior to assert: Implementation Notes include
  `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- Base the fixture on `evals/plan-feature/files/conventions-mock.md` (the existing fixture has no
  trailing whitespace, which is why this case is uncovered) and follow the existing case/assertion
  structure in `evals/plan-feature/evals.json`.

**Fix** in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`:
- Convention conformance analysis: the extraction currently does
  `section_name = line[3:]`. Change the described logic so the heading name is trimmed
  (equivalent of `line[3:].strip()`), covering spaces, tabs, and a trailing `\r` from CRLF files.
  Detecting headings via `line.startswith('## ')` can stay as-is.
- Convention-aware task enrichment: the check `if convention_name in discovered_conventions:`
  should compare normalized names (trim both sides). When a convention relevant to the task cannot
  be matched, record a warning in the skill output rather than silently skipping it.
- Keep the change minimal and in place — fix the existing extraction loop and lookup; do not
  introduce a separate parser.

No CONVENTIONS.md exists at the acme-backend root, so no repository-specific conventions apply.
No persistence impact: the affected values are produced per plan-feature run and written only into
new task descriptions; no data migration is required.

## Reuse Candidates
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md::Convention conformance analysis` — existing heading extraction loop; fix in place by trimming the key
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md::Convention-aware task enrichment` — existing lookup that emits `Per CONVENTIONS.md §{convention_name}: {action}`; reuse its note format unchanged
- `evals/plan-feature/files/conventions-mock.md` — existing conventions fixture to copy as the basis for the trailing-whitespace variant

## Acceptance Criteria
- [ ] Reproducer: a plan-feature eval using a CONVENTIONS.md with `## Migration Patterns  ` (trailing whitespace) asserts the generated task's Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` — fails before the fix, passes after
- [ ] Convention heading names are trimmed at extraction, so headings with trailing spaces, tabs, or `\r` match their canonical names
- [ ] The convention-aware enrichment lookup compares normalized names
- [ ] An unmatched relevant convention produces a visible warning instead of being silently dropped
- [ ] No regression: all existing plan-feature evals (including those using `conventions-mock.md`) still pass

## Test Requirements
- [ ] Reproducer eval: fixture `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` with `## Migration Patterns  ` heading; feature needing a DB migration with FK columns; assert Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` (Actual pre-fix: reference absent, no warning)
- [ ] Assert the existing `conventions-mock.md` (no trailing whitespace) case still produces the same convention notes as before
- [ ] Optional: a fixture variant with tab / CRLF heading endings also matches the convention

## Documentation Updates
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — document that CONVENTIONS.md heading names are whitespace-normalized and that unmatched conventions produce a warning

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with `## Migration Patterns  ` (trailing whitespace) and body `Add Index::create() for all FK columns.`; run `/plan-feature ACME-100` on a feature needing a DB migration with foreign keys; inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention; no warning or error is shown — the convention is silently dropped.
- **Root Cause**: plan-feature extracts CONVENTIONS.md heading names with `line[3:]` without trimming, storing `"Migration Patterns  "`; the enrichment step's exact-match `if convention_name in discovered_conventions:` then fails with no warning.
