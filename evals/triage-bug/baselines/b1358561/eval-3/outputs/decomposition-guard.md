# Decomposition Guard — ACME-502 (Step 6)

Prompt presented to the user:

---

> "This bug appears to involve multiple independent issues:
> 1. **Malformed convention references**: the convention reference formatter
>    lowercases and kebab-cases CONVENTIONS.md headings, so Implementation Notes
>    contain `§migration-patterns` when they should contain `§Migration Patterns`
>    (in `plugins/sdlc-workflow/shared/convention-utils.md`, the convention
>    reference formatter)
> 2. **Wrong issue type on task creation**: task creation uses the Feature issue
>    type ID (10142) when it should use the Task issue type (10050 under the custom
>    issue type scheme), so tasks are created as Features (in
>    `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a – Create the tasks)
>
> These defects are in different modules and run at different phases (task
> description generation vs. Jira issue creation). They share no code or
> configuration, and fixing one does not fix the other.
>
> Options:
> 1. **Proceed** — create a single Task covering all fixes
> 2. **Split** — I recommend creating separate Bugs for each independent issue,
>    then triaging each one individually
>
> Choose (1/2):"

---

## Handling the response

- **1. Proceed**: Create one Task (Target Branch `main`, label `ai-generated-jira`).
  The reproducer tests for both defects go first in Acceptance Criteria and Test
  Requirements. Add a Bug Context section referencing ACME-502, link it with
  `Blocks` (Task blocks ACME-502), post the description digest comment, then report
  the result.
- **2. Split** (recommended): Stop triage of ACME-502. Do not create a Task. Suggest
  the user create two separate Bug issues:
  - Bug A: "plan-feature convention references are kebab-cased instead of matching
    the CONVENTIONS.md heading" (shared/convention-utils.md)
  - Bug B: "plan-feature Step 6a creates tasks with the Feature issue type instead
    of the Task issue type" (plan-feature/SKILL.md Step 6a)

  Then run `/triage-bug` on each one. When filing them, include the missing
  `### **Environment / Version**` section, which ACME-502 did not have.
