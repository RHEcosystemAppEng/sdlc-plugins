# Decomposition Guard -- ACME-502

## Multiple Independent Root Causes Detected

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   -- The convention reference formatter applies kebab-case transformation to CONVENTIONS.md headings, producing `§migration-patterns` instead of preserving the original title case `§Migration Patterns`. This affects all generated Implementation Notes that reference conventions.

2. **Task creation uses Feature issue type ID instead of Task** (in `plan-feature/SKILL.md` Step 6a)
   -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID (10050). This causes created tasks to have the wrong issue type when the project uses a custom issue type scheme.

These two issues are in **different modules** with **independent code paths**. Each fix addresses a distinct root cause rather than a single defect manifesting in multiple places.

## Options

1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):

---

**Execution is paused.** No Task will be created until the user selects an option. The skill will not silently bundle both fixes into a single Task.

- If **Proceed (1)**: a single Task will be created covering both the convention formatter fix in `shared/convention-utils.md` and the issue type fix in `plan-feature/SKILL.md` Step 6a.
- If **Split (2)**: the user should create two separate Bug issues -- one for the convention reference formatting defect and one for the wrong issue type defect -- and then triage each independently with `/triage-bug`.
