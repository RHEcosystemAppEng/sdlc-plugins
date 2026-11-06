# Step 5 – Generated Task for ACME-500

## Jira API metadata (jira.create_issue parameters)

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueTypeName: "Task",
  summary: "Fix plan-feature convention lookup dropping CONVENTIONS.md headings with trailing whitespace",
  description: <task description below, markdown>,
  additional_fields: { "labels": ["ai-generated-jira"] }
)
```

Follow-up operations:
- **Step 5b – Link:** `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-500")`. The Task blocks the Bug.
- **Step 5c – Digest:** re-fetch the created task with `jira.get_issue(<created-task-key>)`, write the description to `/tmp/desc-<task-key>.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, and post the standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` with no footnote.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. When a `CONVENTIONS.md` section heading has trailing whitespace (for example, `## Migration Patterns  `), plan-feature's convention lookup stores the section name with that whitespace (`"Migration Patterns  "`). Later exact-match lookups during task enrichment then fail, and the convention is left out of the generated task's Implementation Notes with no warning. This task normalizes heading extraction so trailing (and leading) whitespace no longer affects matching. It also adds a reproducer eval that covers the edge case.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`: in the convention conformance analysis, strip whitespace from extracted heading names, replacing `line[3:]` with a stripped equivalent. In convention-aware task enrichment, compare normalized names, and optionally warn when a declared convention cannot be matched.
- `evals/plan-feature/evals.json`: add an eval case (with assertions) for a CONVENTIONS.md heading that has trailing whitespace.

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md`: reproducer fixture, a CONVENTIONS.md whose `## Migration Patterns  ` heading has two trailing spaces, followed by `Add Index::create() for all FK columns.`

## Implementation Notes
Fixes ACME-500.

**Reproducer (write first):**
- Trigger: a CONVENTIONS.md containing
  ```
  ## Migration Patterns  
  Add Index::create() for all FK columns.
  ```
  (two trailing spaces after `Patterns`), with plan-feature run on a feature that needs a database migration with foreign keys (the bug's `/plan-feature ACME-100` scenario).
- Current (buggy) behavior the test exposes: the generated task's Implementation Notes contain **no** reference to the Migration Patterns convention, and no warning is shown.
- Correct behavior to assert after the fix: Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`, and the section name is rendered without trailing whitespace.
- Base the fixture on `evals/plan-feature/files/conventions-mock.md`, which has no trailing whitespace, and register the new case in `evals/plan-feature/evals.json` using the same structure as existing cases (`prompt`, `expected_output`, `files`, `assertions`).

**Fix:**
- Defect location: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention conformance analysis. The heading loop does `section_name = line[3:]` with no normalization. Change it to strip whitespace (equivalent to `line[3:].strip()`). This also handles tabs and the `\r` left behind when CRLF files are split on `\n`.
- Consumer: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention-aware task enrichment (`if convention_name in discovered_conventions`). Normalize `convention_name` the same way so both sides are canonical.
- Recommended hardening: when a convention that is expected to apply cannot be found, show a visible warning instead of dropping it, which addresses the "no warning" part of the Actual Result. Keep this change small and confined to plan-feature.
- No `CONVENTIONS.md` exists at the acme-backend root, so no repo-specific conventions apply.
- Persistence impact: none. The convention map is computed in memory on each plan-feature run, so no data migration is needed.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md`: existing conventions fixture to copy as the basis for the trailing-whitespace reproducer.
- `evals/plan-feature/evals.json`: existing eval case structure and assertion style to follow.

## Acceptance Criteria
- [ ] Reproducer: a plan-feature eval with a CONVENTIONS.md heading `## Migration Patterns  ` (trailing whitespace) asserts that the generated Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` It fails before the fix and passes after.
- [ ] Heading extraction in plan-feature's convention conformance analysis strips leading and trailing whitespace (spaces, tabs, `\r`) from section names.
- [ ] Convention-aware task enrichment matches conventions by normalized name, so headings with and without trailing whitespace resolve identically.
- [ ] A convention that cannot be matched produces a visible warning instead of being silently dropped.
- [ ] No regression: all existing plan-feature evals (including the `conventions-mock.md` cases) still pass.

## Test Requirements
- [ ] Reproducer eval (first): fixture CONVENTIONS.md with `## Migration Patterns  ` followed by `Add Index::create() for all FK columns.`; run plan-feature on an FK-migration feature. Assert (a) the Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`, and (b) the rendered section name is exactly `Migration Patterns` with no trailing spaces. Before the fix, assertion (a) fails because the convention is missing.
- [ ] Additional case: a heading with a trailing tab and/or CRLF line endings is also matched.
- [ ] Regression: existing plan-feature conventions evals using `evals/plan-feature/files/conventions-mock.md` still pass unchanged.

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with a heading that has trailing whitespace (`## Migration Patterns  ` / `Add Index::create() for all FK columns.`), run `/plan-feature ACME-100` on a feature needing a DB migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention, and no warning or error is shown (the convention is silently dropped).
- **Root Cause**: plan-feature's convention lookup extracts heading names with `line[3:]` without stripping whitespace, so `## Migration Patterns  ` is stored as `"Migration Patterns  "`. The exact-match lookup in task enrichment against `"Migration Patterns"` fails, and there is no warning on a miss.
