# Step 5 – Generated Task: ACME-500 fix

**Create call (simulated, not sent):**

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueTypeName: "Task",
  summary: "Fix plan-feature dropping CONVENTIONS.md sections with trailing whitespace in headings",
  description: <below>,
  additional_fields: { "labels": ["ai-generated-jira"] }
)
```

**Link (Step 5b, simulated):**
`jira.create_issue_link(link_type="Blocks", inward_issue_key=<new-task-key>, outward_issue_key="ACME-500")`.
The Task blocks the Bug.

**Digest (Step 5c, simulated):** re-fetch the created task, write its description to
`/tmp/desc-<task-key>.txt`, run `python3 scripts/sha256-digest.py`, then post the standalone
comment `[sdlc-workflow] Description digest: <tagged-digest>` with no footnote.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-500. plan-feature's convention conformance analysis drops `CONVENTIONS.md`
sections whose heading lines have trailing whitespace (for example,
`## Migration Patterns  `), and it does so silently. Heading extraction keeps the trailing
whitespace, so the exact-match lookup during task enrichment fails, and the convention never
reaches the generated task's Implementation Notes. This task normalizes heading text so that
matching ignores whitespace, and adds a visible warning when an expected convention cannot be
matched.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`: strip whitespace from extracted
  convention heading names in the convention conformance analysis. Normalize lookup keys in
  the convention-aware task enrichment. Warn instead of silently skipping unmatched
  conventions.
- `evals/plan-feature/evals.json`: add a reproducer eval case for trailing-whitespace
  headings.

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md`: a
  `CONVENTIONS.md` fixture whose `## Migration Patterns  ` heading has trailing spaces, with
  the body `Add Index::create() for all FK columns.`

## Implementation Notes
Fixes ACME-500.

**Reproducer first.** Build the reproducer from the Bug's Steps to Reproduce:
- *Triggering input:* a `CONVENTIONS.md` with a heading line `## Migration Patterns  ` (two
  trailing spaces) followed by `Add Index::create() for all FK columns.`, used while planning
  a feature that needs a DB migration with foreign keys (as in `/plan-feature ACME-100`).
- *Current (incorrect) behavior to observe before the fix:* the generated task's
  Implementation Notes contain **no** reference to `§Migration Patterns`, and no warning is
  emitted.
- *Correct behavior to assert after the fix:* Implementation Notes contain
  `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- Base the new fixture on the existing `evals/plan-feature/files/conventions-mock.md`. Copy
  its structure and add trailing whitespace to the heading. Keep the trailing spaces intact:
  make sure editors and formatters do not strip them, for example by checking with
  `grep -n ' $'`.
- Add the eval case to `evals/plan-feature/evals.json`, following the shape of the existing
  entries (`id`, `prompt`, `expected_output`, `files`, `assertions`).

**Fix in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`:**
- Convention conformance analysis (heading extraction): the current logic is
  `section_name = line[3:]`. Change the instructions so the extracted name is
  whitespace-trimmed, the equivalent of `line[3:].strip()`. Also tolerate `##` followed by
  several spaces.
- Convention-aware task enrichment (`if convention_name in discovered_conventions:` →
  `notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")`): compare normalized
  (trimmed) names on both sides. Emit the citation with the trimmed name, so the output reads
  `§Migration Patterns` with no trailing spaces.
- Remove the silent failure: when a convention that applies to the task cannot be matched,
  state a visible warning in the plan output (for example, "Convention '<name>' referenced but
  not found in CONVENTIONS.md headings") instead of skipping it quietly.

**Scope notes:**
- The target repository has no root `CONVENTIONS.md`, so there are no extra repo conventions
  to apply.
- No persistence impact: the convention map is transient skill state and is not written to a
  database, so no data migration is needed.
- Other skills that parse `CONVENTIONS.md` headings may have the same pattern. Check them, but
  keep this task scoped to plan-feature unless the same defect is confirmed elsewhere. If it
  is, open a separate Bug.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md`: the existing conventions fixture. Use it
  as the template for the trailing-whitespace variant.
- `evals/plan-feature/evals.json`: existing eval case structure and assertion style to copy
  for the reproducer.

## Acceptance Criteria
- [ ] A reproducer eval exists using a `CONVENTIONS.md` fixture with
  `## Migration Patterns  ` (trailing whitespace). It fails before the fix (the convention is
  missing from Implementation Notes) and passes after the fix.
- [ ] plan-feature trims whitespace from convention heading names, so headings with trailing
  (or extra leading) whitespace match their expected convention names.
- [ ] The generated Implementation Notes cite the convention with its normalized name
  (`Per CONVENTIONS.md §Migration Patterns: ...`), with no trailing spaces in the citation.
- [ ] When an applicable convention cannot be matched, plan-feature shows a visible warning
  instead of dropping it silently.
- [ ] Existing plan-feature evals (including those using `conventions-mock.md`) still pass,
  with no regressions.

## Test Requirements
- [ ] Reproducer eval: given a `CONVENTIONS.md` fixture whose heading is
  `## Migration Patterns  ` and a feature needing an FK migration, assert that the generated
  task's Implementation Notes contain
  `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns`. Before the
  fix, the citation is absent and no warning appears (the Actual Result). After the fix, the
  citation is present (the Expected Result).
- [ ] Assert that the cited section name has no trailing whitespace.
- [ ] Re-run the existing plan-feature conventions eval(s) unchanged to confirm that headings
  without trailing whitespace still match.

## Verification Commands
- `grep -n ' $' evals/plan-feature/files/conventions-trailing-whitespace-mock.md` should list
  the `## Migration Patterns  ` line, confirming that the fixture keeps its trailing
  whitespace.

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with the heading
  `## Migration Patterns  ` (trailing spaces) and the body
  `Add Index::create() for all FK columns.`. Run `/plan-feature ACME-100` on a feature that
  needs a DB migration with foreign keys. Inspect the generated task's Implementation Notes.
- **Expected Result**: Implementation Notes include "Per CONVENTIONS.md §Migration Patterns:
  add `Index::create()` for all FK columns."
- **Actual Result**: Implementation Notes do not reference the Migration Patterns convention.
  No warning or error is shown, so the convention is silently dropped.
- **Root Cause**: plan-feature extracts `CONVENTIONS.md` heading names with `line[3:]` and
  does not strip whitespace, which yields `"Migration Patterns  "`. The exact-match lookup in
  task enrichment against `"Migration Patterns"` then fails, with no warning.

---

## Step 7 – Report (summary to user)

- **Task:** `<new-task-key>`, created and linked as *blocks* ACME-500 (simulated).
- **Root cause:** heading names in plan-feature's `CONVENTIONS.md` parsing are not trimmed,
  so exact-match lookups fail silently.
- **Fix:** trim heading names and lookup keys, and warn on unmatched conventions.
- **Reproducer:** a plan-feature eval with a trailing-whitespace `## Migration Patterns  `
  fixture, asserting that the `§Migration Patterns` citation appears.
- **Affects Version:** the existing value `0.9.0` was detected. The user was asked to choose
  Keep, Replace or Augment, and the answer is still pending (see version-resolution.md).
- **Next step:** run `/implement-task <new-task-key>` to implement the fix.
