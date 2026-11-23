# Step 5 – Generated Task (would be created via `jira.create_issue`)

**Jira create parameters**
- Project: `ACME`
- Issue type: `Task`
- Summary: `Fix plan-feature dropping CONVENTIONS.md sections with trailing whitespace in headings`
- Labels: `["ai-generated-jira"]`

**Step 5b link**: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<new-task-key>, outward_issue_key="ACME-500")`. The Task blocks the Bug.

**Step 5c**: re-fetch the created description, then run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, then post the standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote).

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. plan-feature's convention conformance analysis extracts `CONVENTIONS.md`
section names with `line[3:]` and does not strip whitespace. A heading with trailing
whitespace (e.g., `## Migration Patterns  `) gives a section name that fails the exact-match
lookup during convention-aware task enrichment, so the convention is silently left out of
generated task Implementation Notes. This task normalizes heading names, warns on unmatched
conventions, and adds a reproducer eval so the fix stays in place.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — normalize extracted `CONVENTIONS.md` heading names (strip whitespace) in convention conformance analysis, and add a visible warning when an expected convention cannot be matched during convention-aware task enrichment
- `evals/plan-feature/evals.json` — add an eval case covering a `CONVENTIONS.md` heading with trailing whitespace

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — fixture based on `evals/plan-feature/files/conventions-mock.md`, with `## Migration Patterns  ` (trailing spaces) followed by `Add Index::create() for all FK columns.`

## Implementation Notes
Fixes ACME-500.

**Reproducer (write first):**
- Trigger scenario: a `CONVENTIONS.md` containing
  ```
  ## Migration Patterns  
  Add Index::create() for all FK columns.
  ```
  (two trailing spaces after the heading), plus a feature (e.g., ACME-100) that needs a
  database migration with foreign keys.
- Before the fix, the reproducer should show the Actual Result: the generated task's
  Implementation Notes contain **no** reference to Migration Patterns, and no warning is shown.
- After the fix, the reproducer should assert the Expected Result: the Implementation Notes
  contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- Follow the existing eval fixture pattern in `evals/plan-feature/files/conventions-mock.md`
  (synthetic-data header comment, same structure) and register the case in
  `evals/plan-feature/evals.json` with assertions in the same style as existing entries.

**Fix:**
- In `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention conformance analysis,
  the heading extraction currently does `section_name = line[3:]`. Change the instruction or
  logic so the section name is whitespace-normalized (equivalent to `line[3:].strip()`). This
  removes trailing spaces, tabs, and a trailing `\r` from CRLF files.
- In convention-aware task enrichment (`if convention_name in discovered_conventions:`),
  compare normalized names. When a convention that applies to the task cannot be matched,
  report a visible warning rather than skipping it silently.
- Keep the change limited to heading normalization and miss reporting. Do not change how
  section content is captured.
- The repository has no `CONVENTIONS.md` at its root, so no repo-specific conventions apply.
- No persistence boundary exists (output is generated per run into task text), so no data
  migration is needed.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing conventions fixture; copy its structure for the trailing-whitespace variant
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md::convention conformance analysis` — existing heading-parse loop to fix in place (use standard `str.strip()` normalization; no new helper needed)

## Acceptance Criteria
- [ ] Reproducer: a plan-feature eval using a `CONVENTIONS.md` with `## Migration Patterns  ` (trailing whitespace) produces Implementation Notes containing "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns." (fails before the fix, passes after)
- [ ] `CONVENTIONS.md` section headings are matched regardless of leading or trailing whitespace (spaces, tabs, `\r`)
- [ ] When an applicable convention cannot be matched, plan-feature reports a visible warning instead of dropping it silently
- [ ] No regression: existing plan-feature evals (including the `conventions-mock.md` case) still pass

## Test Requirements
- [ ] Reproducer eval: fixture `conventions-trailing-whitespace-mock.md` with `## Migration Patterns  ` / `Add Index::create() for all FK columns.`. Assert that the generated task's Implementation Notes include the §Migration Patterns note with `Index::create()` for FK columns (Expected Result), and that the convention is not missing (Actual Result before the fix)
- [ ] Add an assertion or case covering a CRLF (`\r\n`) or tab-trailing heading, if practical in the existing eval format
- [ ] Re-run the existing plan-feature conventions eval to confirm unchanged behavior for clean headings

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with a heading that has trailing whitespace (`## Migration Patterns  ` / `Add Index::create() for all FK columns.`). Run `/plan-feature ACME-100` on a feature that needs an FK migration, then inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention, and no warning or error is shown. The convention is silently dropped.
- **Root Cause**: Heading extraction `section_name = line[3:]` in plan-feature's convention conformance analysis does not strip trailing whitespace. The resulting key (`"Migration Patterns  "`) fails the exact-match lookup in convention-aware task enrichment, and the miss is not reported.
