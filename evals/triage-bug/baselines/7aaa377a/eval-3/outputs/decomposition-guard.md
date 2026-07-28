# Decomposition Guard — Step 6

The following prompt would be presented to the user after completing root cause analysis
for ACME-502, before creating any Task issue.

---

## Prompt to Present to User

> This bug appears to involve multiple independent issues:
>
> 1. **Malformed convention cross-reference labels** (in `shared/convention-utils.md`)
>    — The convention formatter applies a URL-slug transformation (lowercase + hyphenate)
>    to CONVENTIONS.md section headings when building cross-reference labels, producing
>    `§migration-patterns` instead of preserving the original heading text `§Migration Patterns`.
>    This is a bug in the heading-to-reference conversion function in the shared convention
>    utility module.
>
> 2. **Task created with wrong issue type** (in `plan-feature/SKILL.md` Step 6a)
>    — The task creation step reads `Feature issue type ID` from CLAUDE.md configuration
>    (10142) and uses it when creating Task issues, causing tasks to be created as Features
>    in projects with custom issue type schemes. The Task issue type ID (10050 in this
>    project) is not surfaced as a separate configuration field and is therefore never
>    consulted.
>
> These are in separate modules with no shared code path — fixing one does not affect
> the other.
>
> Options:
> 1. **Proceed** — create a single Task covering all fixes
> 2. **Split** — I recommend creating separate Bugs for each independent issue,
>    then triaging each one individually
>
> Choose (1/2):

---

## Skill Behavior Based on Choice

**If the user chooses 1 (Proceed)**:
Continue to Step 5 — generate a single Task that covers both fixes:
- Files to Modify: `shared/convention-utils.md` and `plan-feature/SKILL.md`
- Acceptance Criteria include reproducer tests for both the formatter fix and the
  issue type fix
- Implementation Notes cover both code paths

**If the user chooses 2 (Split)**:
Stop execution. Inform the user:

> "Recommended next steps:
> 1. Create a new Bug for the convention formatter issue (the `§migration-patterns`
>    label format) and run `/triage-bug <new-bug-key>` to generate a focused fix Task.
> 2. Create a new Bug for the wrong issue type on task creation and run
>    `/triage-bug <new-bug-key>` to generate a focused fix Task.
>
> ACME-502 can then be closed as a duplicate or parent tracking issue once both
> child bugs are resolved."

---

## Rationale

Per `triage-bug` SKILL.md Step 6:

> "If the bug appears to need multiple independent fixes across different files or
> modules — where each fix addresses a distinct root cause rather than a single
> defect — flag this to the user rather than silently creating a single Task that
> bundles unrelated fixes."

ACME-502 meets this criterion:
- Root Cause 1 is entirely contained within `shared/convention-utils.md` (the formatter).
- Root Cause 2 is entirely contained within `plan-feature/SKILL.md` Step 6a (the creator).
- These are not a single defect manifesting across multiple files — they are two
  distinct defects triggered by the same top-level skill invocation.

This is **not** the case where a single root cause manifests across multiple files
(which would not trigger decomposition). Each issue here has its own independent
cause, fix, and reproducer test.
