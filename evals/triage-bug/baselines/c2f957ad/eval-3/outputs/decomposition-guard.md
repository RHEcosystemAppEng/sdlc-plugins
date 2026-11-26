# Decomposition Guard — ACME-502 (Step 6)

Prompt shown to the user before any Task is created:

---

> This bug appears to involve multiple independent issues:
>
> 1. **Malformed convention references in Implementation Notes.** The convention
>    formatter turns `CONVENTIONS.md` headings into kebab-case slugs
>    (`§migration-patterns`) instead of keeping the heading text (`§Migration Patterns`).
>    (in `plugins/sdlc-workflow/skills/shared/convention-utils.md` — convention reference formatter)
> 2. **Tasks created with the wrong issue type.** Task creation uses the Feature
>    issue type ID (10142) instead of the discovered Task issue type ID (10050) when the
>    project has a custom issue type scheme.
>    (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Step 6a, task creation logic)
>
> These defects are in different modules, have different triggers (a `CONVENTIONS.md`
> file vs. a custom issue type scheme), and share no code path. Fixing one does not
> affect the other. They only both show up on the same generated task.
>
> Options:
> 1. **Proceed** — create a single Task covering all fixes
> 2. **Split** — I recommend creating separate Bugs for each independent issue,
>    then triaging each one individually
>
> Choose (1/2):

---

## Handling the response

- **1 (Proceed)**: continue with Step 5. Create one Task (label `ai-generated-jira`,
  Target Branch `main`, "Fixes ACME-502"). Put one reproducer criterion per root cause
  at the top of the Acceptance Criteria and Test Requirements. Link it with
  "Blocks" (Task blocks ACME-502) and post the description digest.
- **2 (Split)** (recommended): stop. Create no Task. Suggest the user file two Bugs:
  - "Convention references in Implementation Notes use kebab-case instead of the heading text" (component: sdlc-workflow, area: shared/convention-utils.md)
  - "plan-feature Step 6a creates tasks with the Feature issue type instead of Task under custom issue type schemes" (component: sdlc-workflow, area: plan-feature/SKILL.md Step 6a)

  Then run `/triage-bug` on each new Bug. When filing them, include the missing
  `### **Environment / Version**` section, which ACME-502 lacks.
