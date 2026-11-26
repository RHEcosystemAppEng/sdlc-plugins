# Step 5 — Generated Task (ACME-500)

## Jira create_issue parameters (simulated, not sent)

| Parameter | Value |
|---|---|
| cloudId | `mock-cloud-id-for-eval` |
| projectKey | `ACME` |
| issueType | `Task` |
| summary | Fix plan-feature dropping CONVENTIONS.md sections whose headings have trailing whitespace |
| labels | `["ai-generated-jira"]` |

Follow-up actions after creation (simulated):
- **Step 5b link**: `jira.create_issue_link(link_type="Blocks", inward_issue_key=<new-task-key>, outward_issue_key="ACME-500")`. The Task blocks the Bug.
- **Step 5c digest**: re-fetch the created task's description, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, and post the standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` with no footnote.
- **Step 6**: single root cause, so no decomposition prompt.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. When a `CONVENTIONS.md` heading line has trailing whitespace (e.g., `## Migration Patterns  `), plan-feature's convention conformance analysis stores the section under a whitespace-padded name. The exact-match lookup in convention-aware task enrichment then fails, and the convention is dropped from generated task Implementation Notes without any warning. This task normalizes extracted heading names and adds a warning for unmatched conventions, so conventions are applied reliably and mismatches are visible.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — strip whitespace from extracted `CONVENTIONS.md` section names in the convention conformance analysis, and add a warning in convention-aware task enrichment when an expected convention cannot be matched
- `evals/plan-feature/evals.json` — add a reproducer eval case covering headings with trailing whitespace

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — reproducer fixture: a CONVENTIONS.md whose `## Migration Patterns  ` heading has trailing spaces, with body `Add Index::create() for all FK columns.`

## Implementation Notes
Fixes ACME-500.

**Defect location.** In `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, the convention conformance analysis parses headings like this:
```python
if line.startswith('## '):
    section_name = line[3:]
```
`line[3:]` keeps trailing whitespace, and also keeps a trailing `\r` when the file uses CRLF line endings and is split on `\n`. Change the instruction or logic so the section name is normalized, for example `section_name = line[3:].strip()`. Stored keys must equal the canonical heading text.

**Silent-drop location.** Convention-aware task enrichment in the same file does:
```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```
Keep the exact-match lookup, which works once keys are normalized. Add an explicit warning path: when a convention relevant to the task cannot be found in `discovered_conventions`, surface a warning in the plan-feature output instead of skipping it silently. Optionally, normalize `convention_name` the same way (strip) before the lookup so both sides are compared symmetrically.

**Reproducer guidance (from the Bug's Steps to Reproduce).**
- Trigger input: a `CONVENTIONS.md` containing
  ```
  ## Migration Patterns  
  Add Index::create() for all FK columns.
  ```
  with two trailing spaces after `Patterns`, plus a feature (the ACME-100 equivalent) that needs a DB migration with foreign keys.
- Current (buggy) behavior to confirm before the fix: generated Implementation Notes contain **no** reference to `Migration Patterns`, and no warning is emitted.
- Correct behavior to assert after the fix: Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`. The section name in that string must have no trailing whitespace (`§Migration Patterns:`, not `§Migration Patterns  :`).

**Test patterns.** Model the new fixture on `evals/plan-feature/files/conventions-mock.md`, which currently has no trailing whitespace on headings. That is why this case was not covered. Add the eval entry to `evals/plan-feature/evals.json`, following the structure of existing entries (`id`, `prompt`, `expected_output`, `files`, `assertions`).

**Conventions.** The repository has no `CONVENTIONS.md` at its root, so no extra repo conventions apply.

**Persistence.** No persistence boundary. Parsed convention names exist only in memory while plan-feature generates a task, so no data migration is needed.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing conventions fixture to copy as the base for the trailing-whitespace reproducer
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (convention-aware task enrichment) — the existing `Per CONVENTIONS.md §{convention_name}: {action}` note format; reuse it unchanged

## Acceptance Criteria
- [ ] Reproducer: a plan-feature eval with a `CONVENTIONS.md` heading `## Migration Patterns  ` (trailing whitespace) produces Implementation Notes containing "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns." The eval fails before the fix and passes after it.
- [ ] Section names extracted from `CONVENTIONS.md` headings have leading and trailing whitespace stripped, including trailing tabs and `\r`
- [ ] When an expected convention cannot be matched, plan-feature emits a visible warning instead of dropping it silently
- [ ] Existing plan-feature evals (including the `conventions-mock.md` scenarios) still pass with no regression

## Test Requirements
- [ ] Reproducer eval: fixture `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` with `## Migration Patterns  `. Assert that the generated Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns` and that the cited section name has no trailing whitespace. Before the fix, this assertion fails because the reference is missing.
- [ ] Add an assertion (or a separate case) that a convention which cannot be matched produces a warning in plan-feature output
- [ ] Re-run all existing plan-feature evals to confirm there are no regressions

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with `## Migration Patterns  ` (trailing whitespace) followed by "Add Index::create() for all FK columns."; run `/plan-feature ACME-100` on a feature requiring an FK migration; inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention, and no warning or error is shown. The convention is silently dropped.
- **Root Cause**: plan-feature extracts heading names with `line[3:]` without stripping whitespace, so `"Migration Patterns  "` is stored. The exact-match lookup in task enrichment then misses it, and there is no warning path.
