# Decomposition Guard -- ACME-502

## Trigger

During investigation of ACME-502 (Steps 2-4), two independent root causes were identified in different modules:

- **Root Cause 1** is in `shared/convention-utils.md` (convention reference formatting pipeline).
- **Root Cause 2** is in `plan-feature/SKILL.md` Step 6a (Jira issue creation pipeline).

These root causes are independent: they affect different modules, follow different code paths, can be fixed independently, and require different reproducer strategies. This triggers the Decomposition Guard (Step 6) per the triage-bug skill specification.

## User Prompt

Per Step 6 of the triage-bug skill, the following prompt is presented to the user:

> "This bug appears to involve multiple independent issues:
> 1. Convention reference formatter uses wrong case transform -- headings are kebab-cased (`migration-patterns`) instead of preserving original text (`Migration Patterns`) (in `shared/convention-utils.md`)
> 2. Task creation uses Feature issue type ID (10142) instead of Task issue type ID (10050) (in `plan-feature/SKILL.md` Step 6a)
>
> Options:
> 1. **Proceed** -- create a single Task covering all fixes
> 2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually
>
> Choose (1/2):"

## Skill Behavior

The skill **STOPS here and waits for user input**. No Task is created until the user responds. The skill does NOT silently create a single Task bundling both fixes.

### If the user chooses "1. Proceed"

The skill creates a **single Task** covering both fixes. The Task description will include both root causes in its Implementation Notes, both reproducer tests in its Acceptance Criteria, and references to both affected modules. The triage continues with Step 5 (Generate Task) through Step 7 (Report Result).

### If the user chooses "2. Split"

The skill **stops execution** and recommends that the user create two separate Bug issues -- one for each independent root cause:

1. A Bug for the convention reference formatting issue in `shared/convention-utils.md`.
2. A Bug for the issue type selection problem in `plan-feature/SKILL.md` Step 6a.

Each new Bug would then be triaged individually via `/triage-bug`, producing its own focused Task with a single root cause, a targeted reproducer test, and scoped Implementation Notes. This approach keeps each fix atomic and independently verifiable.
