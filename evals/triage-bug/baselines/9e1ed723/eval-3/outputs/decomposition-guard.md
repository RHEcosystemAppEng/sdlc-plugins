# Decomposition Guard — ACME-502 (Step 6)

Prompt shown to the user before any Task is created:

---

> "This bug appears to involve multiple independent issues:
> 1. **Malformed convention references**: the convention formatter kebab-cases
>    CONVENTIONS.md headings, so Implementation Notes say `§migration-patterns` instead of
>    `§Migration Patterns` (in `plugins/sdlc-workflow/shared/convention-utils.md`,
>    convention reference formatter)
> 2. **Wrong issue type on task creation**: tasks are created with the Feature issue
>    type ID (10142) instead of the discovered Task issue type ID (10050) (in
>    `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a)
>
> These root causes sit in different modules and don't share a code path. Fixing one
> won't fix the other, and each needs its own reproducer test.
>
> Options:
> 1. **Proceed**: create a single Task covering all fixes
> 2. **Split**: I recommend creating separate Bugs for each independent issue,
>    then triaging each one individually
>
> Choose (1/2):"

---

## Handling the response

- **1. Proceed**: continue to Step 5 and create one Task covering both fixes. Reproducer
  tests for both issues go first in Acceptance Criteria and Test Requirements. Then
  link the Task to ACME-502 (Blocks) and post the digest comment (Steps 5b, 5c).
- **2. Split**: stop. No Task is created. Suggest that the user create two Bug issues:
  - "Convention references in Implementation Notes use kebab-case instead of the heading
    text" (component: sdlc-workflow; scope: `shared/convention-utils.md`)
  - "plan-feature Step 6a creates tasks with Feature issue type instead of Task issue
    type" (component: sdlc-workflow; scope: `skills/plan-feature/SKILL.md` Step 6a)

  Then run `/triage-bug <new-key>` for each one. Add the missing
  `### **Environment / Version**` section to both new Bugs, which ACME-502 also lacks.
