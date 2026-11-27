# Step 5 – Generated Task (would be created via `jira.create_issue`)

- **Project:** ACME
- **Issue type:** Task
- **Summary:** Fix plan-feature dropping CONVENTIONS.md sections whose headings have trailing whitespace
- **Labels:** `ai-generated-jira`
- **Link (Step 5b):** `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-500")` (Task blocks Bug)
- **Digest (Step 5c):** re-fetch the created task's description -> `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt` -> post standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote)

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. When a CONVENTIONS.md heading line has trailing whitespace (e.g., `## Migration Patterns  `), plan-feature's convention conformance analysis stores the section name with the trailing spaces. The later exact-match lookup in task enrichment then misses it, and the convention is silently left out of the generated task's Implementation Notes. This task normalises extracted heading names and adds a visible warning when an expected convention cannot be matched. It also adds a reproducer eval that covers the trailing-whitespace case.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — strip whitespace from extracted CONVENTIONS.md section names in convention conformance analysis, and warn instead of silently skipping when a convention lookup misses in convention-aware task enrichment
- `evals/plan-feature/evals.json` — add a reproducer eval case for headings with trailing whitespace

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — CONVENTIONS.md fixture variant whose headings contain trailing whitespace (e.g., `## Migration Patterns  ` followed by `Add Index::create() for all FK columns.`)

## Implementation Notes
- Fixes ACME-500.
- **Defect location 1 — heading extraction** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention conformance analysis): the current logic is `section_name = line[3:]`. Change it to normalise the heading text, i.e. `line[3:].strip()`. `.strip()` also covers stray leading spaces and `\r` from CRLF files. Then `## Migration Patterns  ` maps to the key `"Migration Patterns"`.
- **Defect location 2 — lookup** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention-aware task enrichment): `if convention_name in discovered_conventions:` is an exact match. Once keys are normalised at extraction, the match succeeds. Also normalise `convention_name` the same way for symmetry. Add an explicit warning path for an expected convention that is not found (e.g., "Convention '<name>' expected but not found in CONVENTIONS.md"), so the miss is no longer silent.
- **Reproducer test guidance** (from the ACME-500 Steps to Reproduce):
  - Input/scenario: a CONVENTIONS.md containing `## Migration Patterns  ` (two trailing spaces) followed by `Add Index::create() for all FK columns.`, and a plan-feature run on a feature that needs a database migration with foreign keys (as for ACME-100).
  - Current (buggy) behaviour the test exposes: the generated Implementation Notes do NOT reference the Migration Patterns convention, and no warning is shown.
  - Correct behaviour after the fix: the generated Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- Follow the existing fixture pattern in `evals/plan-feature/files/conventions-mock.md`. Copy its structure and add trailing whitespace to the heading lines. Add the eval entry to `evals/plan-feature/evals.json` alongside the existing conventions eval, using the same assertion style.
- The repository has no CONVENTIONS.md at its root, so there are no repo-specific conventions to apply.
- No persistence impact: convention names are in-memory only during plan-feature runs, so no data migration is needed.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing conventions fixture. Use it as the template for the trailing-whitespace variant.
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (convention conformance analysis heading extraction) — the single normalisation point. Fix it here rather than adding fuzzy matching at each lookup site.

## Acceptance Criteria
- [ ] A reproducer eval with a CONVENTIONS.md heading `## Migration Patterns  ` (trailing whitespace) asserts that the generated Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` It fails before the fix and passes after.
- [ ] CONVENTIONS.md section names are extracted with leading and trailing whitespace stripped, so headings with and without trailing whitespace resolve to the same convention name
- [ ] When an expected convention cannot be matched, plan-feature emits a visible warning instead of silently dropping it
- [ ] No regression: existing plan-feature evals (including the `conventions-mock.md` scenario) still pass

## Test Requirements
- [ ] Reproducer: new eval using `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` that runs plan-feature on a feature needing an FK migration. Assert the Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` Before the fix this assertion fails because the convention is missing (ACME-500 Actual Result). After the fix it passes (ACME-500 Expected Result).
- [ ] Assert the referenced section name has no trailing whitespace (`§Migration Patterns:`, not `§Migration Patterns  :`)
- [ ] Assert a warning is produced when an expected convention section is absent from CONVENTIONS.md
- [ ] Re-run the existing plan-feature conventions eval and confirm the output is unchanged

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with heading `## Migration Patterns  ` (trailing whitespace) followed by `Add Index::create() for all FK columns.` Run `/plan-feature ACME-100` on a feature needing a DB migration with foreign keys, then inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention, and no warning or error is shown (the convention is silently dropped).
- **Root Cause**: Heading extraction in plan-feature (`section_name = line[3:]`) does not strip trailing whitespace, so the stored key is `"Migration Patterns  "`. The exact-match lookup `convention_name in discovered_conventions` fails for `"Migration Patterns"`, and there is no warning on a miss.
