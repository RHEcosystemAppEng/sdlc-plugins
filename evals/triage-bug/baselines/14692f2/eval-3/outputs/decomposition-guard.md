# Step 6 -- Decomposition Guard

## Trigger

The investigation (Steps 2-4) identified **two independent root causes** in different modules with different code paths. This triggers the Decomposition Guard per the skill definition: "if the bug appears to need multiple independent fixes across different files or modules -- where each fix addresses a distinct root cause rather than a single defect -- flag this to the user."

## Prompt to User

> This bug appears to involve multiple independent issues:
>
> 1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
>    The convention reference formatter applies a kebab-case transform (lowercase + replace spaces with hyphens) to CONVENTIONS.md section headings, producing `migration-patterns` instead of preserving the original heading text `Migration Patterns`. This is a formatting logic error in the shared convention utilities module.
>
> 2. **Task creation uses Feature issue type ID instead of Task** (in `plan-feature/SKILL.md` Step 6a)
>    The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID (10050), causing created tasks to have the wrong issue type. This is a configuration field reference error in the plan-feature skill.
>
> These issues are in different modules (`shared/convention-utils.md` vs `plan-feature/SKILL.md`) and involve entirely different code paths (convention reference formatting vs Jira issue creation). They can be fixed, tested, and merged independently.
>
> Options:
> 1. **Proceed** -- create a single Task covering both fixes
> 2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually
>    - Bug A: Convention reference formatter applies wrong case transform to section headings (`shared/convention-utils.md`)
>    - Bug B: Task creation uses Feature issue type ID instead of Task issue type ID (`plan-feature/SKILL.md` Step 6a)
>
> Choose (1/2):

## Skill behavior

The skill **stops here and waits for user input**. No Task will be created until the user explicitly chooses an option.

- If the user chooses **1 (Proceed)**: the skill continues to Step 5 and creates a single Task covering both fixes, with acceptance criteria and reproducer tests for both root causes.
- If the user chooses **2 (Split)**: the skill stops and recommends the user create two separate Bug issues (one for each root cause), then triage each individually with `/triage-bug`.

This guard ensures the user explicitly decides whether to bundle unrelated fixes into a single Task or to keep them separated for cleaner tracking, independent PRs, and simpler review.
