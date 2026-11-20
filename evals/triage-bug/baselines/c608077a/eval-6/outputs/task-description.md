# Step 5 – Generated Task (for ACME project)

- **Summary:** Fix plan-feature dropping CONVENTIONS.md sections with trailing whitespace in headings
- **Issue type:** Task
- **Labels:** `ai-generated-jira`
- **Link (Step 5b):** link type `Blocks` — inward: <created-task-key> (blocks), outward: ACME-500 (is blocked by)
- **Digest (Step 5c):** after creation, re-fetch description, run `python3 scripts/sha256-digest.py`, post `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote)

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. plan-feature's convention conformance analysis extracts CONVENTIONS.md section
names with `line[3:]` and does not strip whitespace. A heading such as `## Migration Patterns  `
is stored as `"Migration Patterns  "`, so the exact-match lookup in convention-aware task
enrichment fails and the convention is silently omitted from generated tasks' Implementation
Notes. Normalize heading names so trailing whitespace (spaces, tabs, `\r`) no longer prevents
matching, and stop silently dropping unmatched conventions.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — strip whitespace from extracted heading names in the convention conformance analysis; normalize names in the convention-aware task enrichment lookup; warn instead of silently skipping on a miss

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — reproducer fixture: CONVENTIONS.md content with `## Migration Patterns  ` (trailing spaces) and body `Add Index::create() for all FK columns.`

## Implementation Notes
Fixes ACME-500.

**Reproducer (write first):**
- Trigger: CONVENTIONS.md heading with trailing whitespace —
  ```
  ## Migration Patterns  
  Add Index::create() for all FK columns.
  ```
  combined with a feature (e.g., ACME-100) requiring a database migration with foreign keys.
- Current (buggy) behaviour to observe before the fix: generated task Implementation Notes do NOT
  contain any `Per CONVENTIONS.md §Migration Patterns` line, and no warning is emitted.
- Correct behaviour to assert after the fix: Implementation Notes contain
  `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- Model the fixture on `evals/plan-feature/files/conventions-mock.md` (same structure, only adding
  trailing whitespace to the heading) and add a matching entry/assertion in
  `evals/plan-feature/evals.json` following the existing eval entry format.

**Fix:**
- Defect site — convention conformance analysis in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`:
  ```python
  section_name = line[3:]   # currently keeps trailing whitespace
  ```
  must become whitespace-normalized (equivalent of `line[3:].strip()`), covering spaces, tabs and
  the `\r` left by CRLF line endings.
- Consumer — convention-aware task enrichment (`### Convention-aware task enrichment`, same file):
  `if convention_name in discovered_conventions:` — compare normalized names on both sides.
- Make the instruction explicit in the skill prose (the CONVENTIONS.md lookup in Step 3 and the
  enrichment section): section names are trimmed before storage and comparison.
- Replace the silent miss with a visible warning when a convention section cannot be matched,
  without conflicting with the existing rule that conventions failing file-type applicability
  (`shared/convention-applicability-rules.md`) are excluded silently — the warning is for name
  matching failures only, not applicability exclusions.
- No CONVENTIONS.md exists at the acme-backend root; no repo-specific conventions apply.
- No persistence impact: the affected output goes into Jira task descriptions, not a database —
  no data migration needed.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing conventions fixture; copy its structure for the trailing-whitespace reproducer
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md::Convention-aware task enrichment` — existing `Per CONVENTIONS.md §<Section Name>: <action>` output format to preserve

## Acceptance Criteria
- [ ] Reproducer: a plan-feature eval using a CONVENTIONS.md with `## Migration Patterns  ` (trailing whitespace) produces Implementation Notes containing `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` — fails before the fix, passes after
- [ ] Heading names extracted from CONVENTIONS.md are trimmed of leading/trailing whitespace (spaces, tabs, `\r`) before being stored and compared
- [ ] Convention lookup in task enrichment matches regardless of trailing whitespace in the source heading
- [ ] An unmatched convention name produces a visible warning instead of being dropped silently (applicability-based exclusions remain silent)
- [ ] No regression in existing plan-feature evals (including `conventions-mock.md`-based cases)

## Test Requirements
- [ ] Reproducer eval: fixture `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` with heading `## Migration Patterns  `; assert the generated task for an FK-migration feature includes `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` (Expected Result) and does not omit it (Actual Result)
- [ ] Variant: heading with a trailing tab and a CRLF-terminated heading both resolve to `Migration Patterns`
- [ ] Existing conventions eval (no trailing whitespace) still produces the same convention reference

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create CONVENTIONS.md with heading `## Migration Patterns  ` (trailing whitespace) and body `Add Index::create() for all FK columns.`; run `/plan-feature ACME-100` on a feature needing a DB migration with foreign keys; inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention; no warning or error — the convention is silently dropped.
- **Root Cause**: plan-feature extracts heading names with `line[3:]` without stripping whitespace, so the stored key `"Migration Patterns  "` fails the exact-match lookup `convention_name in discovered_conventions` during task enrichment, and the miss path emits no warning.
