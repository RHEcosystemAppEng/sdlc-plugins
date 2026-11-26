# Step 5 – Generated Task for ACME-500

## Jira create_issue parameters

- Project key: ACME
- Issue type: Task
- Summary: Fix plan-feature dropping CONVENTIONS.md sections with trailing whitespace in headings
- Labels: `ai-generated-jira`
- Link (Step 5b): link type `Blocks`, inward = <created-task-key> (blocks), outward = ACME-500 (is blocked by)
- Digest (Step 5c): re-fetch the created task, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, then post `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment with no footnote

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. plan-feature's convention conformance analysis drops a `CONVENTIONS.md` section without any warning when its heading line has trailing whitespace (e.g., `## Migration Patterns  `). The heading is extracted with `line[3:]` and never trimmed, so the stored key (`"Migration Patterns  "`) never matches the exact-name lookup (`"Migration Patterns"`) in task enrichment. The convention is then left out of generated Implementation Notes. This task normalises extracted heading names, surfaces a warning when a convention cannot be matched, and adds a reproducer eval so the regression stays covered.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — trim whitespace (including `\r`) from extracted CONVENTIONS.md heading names in the convention conformance analysis, and add a warning instead of silently skipping when a convention lookup misses in convention-aware task enrichment
- `evals/plan-feature/evals.json` — add a reproducer eval case for headings with trailing whitespace

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — CONVENTIONS.md fixture whose `## Migration Patterns  ` heading has trailing whitespace, with the body `Add Index::create() for all FK columns.`

## Implementation Notes
Fixes ACME-500.

**Reproducer (write first):**
- Trigger scenario: a `CONVENTIONS.md` containing
  ```
  ## Migration Patterns  
  Add Index::create() for all FK columns.
  ```
  (note the two trailing spaces after `Patterns`), used with a plan-feature run on a feature that needs a database migration with foreign keys (as in `/plan-feature ACME-100`).
- Incorrect behaviour (before the fix): the generated task's Implementation Notes do not mention the Migration Patterns convention, and no warning appears.
- Correct behaviour (after the fix): the Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- Model the fixture on the existing `evals/plan-feature/files/conventions-mock.md`, which has the same structure without trailing whitespace. Add the eval case to `evals/plan-feature/evals.json` using the same `prompt` / `files` / `assertions` structure as the existing cases.

**Fix:**
- In `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention conformance analysis: the heading extraction currently behaves like `section_name = line[3:]`. Change the instructions so heading text is trimmed (equivalent to `line[3:].strip()`), removing trailing spaces, tabs and the `\r` from CRLF line endings. Section keys should then always be canonical names such as `Migration Patterns`.
- In the same file, convention-aware task enrichment (`if convention_name in discovered_conventions: notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")`): make sure the lookup uses the normalised name. When a convention relevant to the task cannot be matched, emit a visible warning instead of dropping it silently.
- No persistence impact: the conventions map lives only in memory during plan-feature execution, so no data migration is needed.
- The target repository has no `CONVENTIONS.md` at its root, so no repo-specific conventions apply.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing conventions fixture; copy its structure for the trailing-whitespace reproducer fixture
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md::Convention-aware task enrichment` — existing `Per CONVENTIONS.md §<name>: <action>` note format; keep it unchanged so the expected output matches

## Acceptance Criteria
- [ ] Reproducer: a plan-feature eval with a `CONVENTIONS.md` heading `## Migration Patterns  ` (trailing whitespace) produces Implementation Notes containing `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` This fails before the fix and passes after it.
- [ ] Extracted CONVENTIONS.md heading names are trimmed of leading/trailing whitespace, including `\r` from CRLF line endings, before being used for matching
- [ ] When a relevant convention cannot be matched, plan-feature shows a warning instead of dropping it silently
- [ ] Existing plan-feature evals (including the `conventions-mock.md` case) still pass with no regression

## Test Requirements
- [ ] Reproducer eval: add a fixture `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` with `## Migration Patterns  ` (two trailing spaces) and the body `Add Index::create() for all FK columns.`, plus an eval case in `evals/plan-feature/evals.json`. Assert that the generated task's Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` (Expected Result). Also assert that the convention is not missing from the notes (the Actual Result being guarded against).
- [ ] Add an assertion, or a second fixture variant, covering a CRLF-terminated heading so that a trailing `\r` is also handled
- [ ] Re-run the existing plan-feature conventions eval to confirm no regression

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with the heading `## Migration Patterns  ` (trailing whitespace) and the body `Add Index::create() for all FK columns.`, run `/plan-feature ACME-100` on a feature that needs an FK database migration, then inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention, and no warning or error is shown.
- **Root Cause**: plan-feature extracts CONVENTIONS.md heading names with `line[3:]` and does not strip trailing whitespace, so `"Migration Patterns  "` fails the exact-match lookup for `"Migration Patterns"` in task enrichment. The miss is skipped without any warning.
