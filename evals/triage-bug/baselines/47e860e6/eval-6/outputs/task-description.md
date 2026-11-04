# Step 5 — Generated Task (ACME-500 fix)

**Would be created via `jira.create_issue`:**

- Project: `ACME`
- Issue type: Task
- Summary: `Fix plan-feature dropping CONVENTIONS.md sections whose headings have trailing whitespace`
- Labels: `["ai-generated-jira"]`

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. plan-feature's convention conformance analysis silently drops any CONVENTIONS.md section whose `## ` heading line has trailing whitespace (e.g., `## Migration Patterns  `). Heading extraction keeps the trailing spaces in the section name, so the exact-match lookup during task enrichment fails, and the convention is left out of the generated task's Implementation Notes with no warning. This task normalizes heading names so conventions match whether or not they have trailing whitespace, and makes unmatched conventions visible instead of silently dropping them.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — normalize (strip) CONVENTIONS.md heading text during convention conformance analysis, normalize the lookup key in convention-aware task enrichment, and add a warning when an expected convention cannot be matched

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — reproducer fixture: a CONVENTIONS.md variant whose `## Migration Patterns  ` heading has trailing whitespace, with body `Add Index::create() for all FK columns.`

## Implementation Notes
Fixes ACME-500.

**Defect location:** `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
- *Convention conformance analysis*, which extracts headings with:
  ```python
  if line.startswith('## '):
      section_name = line[3:]
      conventions[section_name] = current_section_content
  ```
  `line[3:]` keeps trailing whitespace, so `## Migration Patterns  ` becomes `"Migration Patterns  "`. Change this to strip whitespace (e.g., `line[3:].strip()`). This also removes a stray `\r` left by `split('\n')` on CRLF files.
- *Convention-aware task enrichment*:
  ```python
  if convention_name in discovered_conventions:
      notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
  ```
  Normalize `convention_name` the same way before the lookup so both sides compare clean names. Add an explicit warning (surfaced to the user and/or noted in the plan output) when a convention that applies to the task cannot be found in `discovered_conventions`. Never drop it silently.

**Reproducer guidance (derived from the Bug's Steps to Reproduce):**
- Trigger input: a CONVENTIONS.md containing
  ```
  ## Migration Patterns  
  Add Index::create() for all FK columns.
  ```
  (two trailing spaces after `Patterns`), used with a feature that needs a database migration with foreign keys (as in `/plan-feature ACME-100`).
- Before the fix (Actual Result): the generated task's Implementation Notes contain **no** reference to Migration Patterns, and no warning is emitted.
- After the fix (Expected Result): Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- Existing fixture pattern: `evals/plan-feature/files/conventions-mock.md` has the same structure but clean headings. Copy it into the new fixture and add the trailing whitespace. Make sure editors or formatters do not strip the trailing spaces from the fixture file (check `.editorconfig` / pre-commit `trailing-whitespace` hooks and exclude the fixture if needed).

**Persistence impact:** none. Convention names are computed in memory on every plan-feature run, so no data migration is required.

**Conventions:** the repository has no CONVENTIONS.md at its root, so no additional repo conventions apply.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing conventions fixture. Use it as the base for the trailing-whitespace reproducer fixture and its eval assertions.

## Acceptance Criteria
- [ ] Reproducer: running plan-feature with a CONVENTIONS.md whose `## Migration Patterns  ` heading has trailing whitespace produces Implementation Notes containing `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` This fails before the fix and passes after.
- [ ] Heading extraction in plan-feature's convention conformance analysis strips leading and trailing whitespace (including `\r`) from section names
- [ ] Convention-aware task enrichment compares normalized names, so headings with and without trailing whitespace match the same convention
- [ ] When an applicable convention cannot be matched, plan-feature emits a visible warning instead of silently dropping it
- [ ] No regression: existing plan-feature evals (including the clean-heading `conventions-mock.md` cases) still pass

## Test Requirements
- [ ] Reproducer eval: add a plan-feature eval case using `conventions-trailing-whitespace-mock.md` with an FK-migration feature. Assert that the generated Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` (Expected Result). Also assert that the Actual Result from before the fix (Migration Patterns reference absent) no longer occurs.
- [ ] Add an eval or assertion for the CRLF variant (`## Migration Patterns\r\n`), checking that the convention is still matched
- [ ] Add an eval or assertion that an unmatched convention produces a visible warning rather than silent omission
- [ ] Re-run the existing plan-feature conventions evals to confirm there is no regression

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with `## Migration Patterns  ` (trailing whitespace) followed by `Add Index::create() for all FK columns.`; run `/plan-feature ACME-100` on a feature requiring a DB migration with foreign keys; inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention, and no warning or error is shown (silently dropped).
- **Root Cause**: plan-feature extracts CONVENTIONS.md section names with `line[3:]` and does not strip trailing whitespace, so `"Migration Patterns  "` never exact-matches `"Migration Patterns"` in the task-enrichment lookup. No warning exists for unmatched conventions.

---

## Step 5b — Link Task to Bug (would be performed)

```
jira.create_issue_link(
  link_type="Blocks",
  inward_issue_key=<created-task-key>,   # Task = blocker
  outward_issue_key="ACME-500"           # Bug = blocked
)
```

## Step 5c — Digest comment (would be performed)

Re-fetch the created task with `jira.get_issue(<created-task-key>)`, write its `description` to `/tmp/desc-<task-key>.txt`, and run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`. Then post a standalone comment `[sdlc-workflow] Description digest: <tagged-digest>`, without the footnote.

## Step 6 — Decomposition Guard

There is a single root cause, so no decomposition prompt is needed.

## Step 7 — Report (would be presented)

- Task: `<created-task-key>` (not created in this eval). It blocks ACME-500.
- Root cause: plan-feature does not strip trailing whitespace from CONVENTIONS.md headings, so the exact-match convention lookup fails silently.
- Planned fix: normalize heading and lookup names, and warn on unmatched conventions.
- Reproducer: a plan-feature eval with a trailing-whitespace heading fixture that asserts the Migration Patterns note is present.
- Affects Version/s: already set to `0.9.0`. Keep / Replace / Augment prompt pending user choice (see version-resolution.md).
- Next step: "Run `/implement-task <created-task-key>` to implement the fix."
