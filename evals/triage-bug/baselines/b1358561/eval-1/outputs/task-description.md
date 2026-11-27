# Jira API Metadata (jira.create_issue parameters)

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueType: "Task",
  summary: "Fix plan-feature dropping CONVENTIONS.md sections whose headings have trailing whitespace",
  description: <task description body below>,
  additional_fields: {
    "labels": ["ai-generated-jira"]
  }
)
```

- Project key: `ACME`
- Issue type: `Task`
- Labels: `ai-generated-jira`

Follow-up operations:
- Step 5b: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<created-task-key>, outward_issue_key="ACME-500")`. The Task blocks the Bug.
- Step 5c: re-fetch the created task, compute the digest with `python3 scripts/sha256-digest.py`, then post the standalone comment `[sdlc-workflow] Description digest: <tagged-digest>`.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. plan-feature's convention conformance analysis silently drops any `CONVENTIONS.md` section whose `## ` heading line has trailing whitespace. The heading text is taken with `line[3:]` and never stripped, so `## Migration Patterns  ` is stored as `"Migration Patterns  "`. The later exact-match lookup for `"Migration Patterns"` then fails, and generated tasks leave out the convention without any warning. This task normalizes heading extraction and lookup so trailing whitespace no longer drops a convention, and adds a reproducer eval for this case.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — strip whitespace from extracted convention heading text in the convention conformance analysis, normalize the lookup key in convention-aware task enrichment, and warn instead of dropping silently when a match fails
- `evals/plan-feature/evals.json` — add a reproducer eval entry for a trailing-whitespace convention heading

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — CONVENTIONS.md fixture whose `## Migration Patterns  ` heading has trailing whitespace, with the body `Add Index::create() for all FK columns.`

## Implementation Notes
Fixes ACME-500.

**Defect location:** `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, convention conformance analysis. The heading extraction loop reads:
```
if line.startswith('## '):
    section_name = line[3:]
```
`line[3:]` keeps trailing spaces and tabs. Change it to strip the extracted name (equivalent to `line[3:].strip()`), and say explicitly in the skill instructions that heading names are compared after trimming whitespace.

**Consumer:** in the same file, the convention-aware task enrichment step does `if convention_name in discovered_conventions:` and then `notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")`. Normalize `convention_name` the same way, so both sides of the comparison are trimmed. The emitted note must use the trimmed name (`§Migration Patterns`, not `§Migration Patterns  `).

**Silent failure:** today a miss has no else branch. Add an instruction to warn when an applicable convention section cannot be matched, so future mismatches show up.

**Reproducer guidance (from Steps to Reproduce):**
- Trigger input: a `CONVENTIONS.md` with
  ```
  ## Migration Patterns  
  Add Index::create() for all FK columns.
  ```
  (two trailing spaces after `Patterns`), used with `/plan-feature ACME-100` on a feature that needs a database migration with foreign keys.
- Incorrect behavior before the fix (Actual Result): the generated task's Implementation Notes do not mention Migration Patterns, and no warning is shown.
- Correct behavior after the fix (Expected Result): the Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`

**Test pattern to follow:** copy the existing fixture `evals/plan-feature/files/conventions-mock.md` (whose headings have no trailing whitespace) into a new fixture that adds the trailing whitespace. Register a new eval in `evals/plan-feature/evals.json` with assertions, matching the structure of the existing entries. Make sure the trailing whitespace survives in the fixture file, since editors and pre-commit hooks may strip it.

**Conventions:** the repository has no `CONVENTIONS.md` at its root, so no extra repo conventions apply.

**Persistence impact:** none. Extracted section names are used in memory only, so no data migration is needed.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing conventions fixture to base the trailing-whitespace fixture on
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (convention-aware task enrichment `notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")`) — existing note format the reproducer assertion should match

## Acceptance Criteria
- [ ] A reproducer eval with a `CONVENTIONS.md` heading `## Migration Patterns  ` (trailing whitespace) asserts that the generated task's Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` It fails before the fix and passes after.
- [ ] Convention heading extraction in plan-feature strips leading and trailing whitespace from section names
- [ ] Convention lookup in task enrichment compares trimmed names, and emitted notes use the trimmed section name
- [ ] A warning is surfaced when an applicable convention section cannot be matched, instead of silently dropping it
- [ ] Existing plan-feature evals (including the `conventions-mock.md` scenario) still pass with no regressions

## Test Requirements
- [ ] Reproducer test: a new plan-feature eval using `evals/plan-feature/files/conventions-trailing-whitespace-mock.md`, where the heading `## Migration Patterns  ` has trailing spaces, run against a feature needing a DB migration with FK columns. Assert that the generated task's Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.` (Expected Result). Assert that the section name appears without trailing whitespace. Before the fix this assertion fails because the convention is absent (Actual Result).
- [ ] Regression test: re-run the existing plan-feature conventions eval with `conventions-mock.md` (no trailing whitespace) and confirm conventions are still included as before
- [ ] Edge case: a heading with a trailing tab (`## Migration Patterns\t`) is also matched

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with the heading `## Migration Patterns  ` (trailing whitespace) and the body `Add Index::create() for all FK columns.`. Run `/plan-feature ACME-100` on a feature needing a DB migration with foreign keys, then inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention. No warning or error is shown and the convention is silently dropped.
- **Root Cause**: plan-feature's convention heading extraction (`section_name = line[3:]`) does not strip trailing whitespace, so the stored key `"Migration Patterns  "` fails the exact-match lookup `convention_name in discovered_conventions` in task enrichment. A miss has no warning path.
