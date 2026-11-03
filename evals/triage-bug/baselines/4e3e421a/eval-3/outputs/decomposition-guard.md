# Step 6 — Decomposition Guard Prompt (ACME-502)

Prompt shown to the user before any Task is created:

---

> This bug appears to involve multiple independent issues:
>
> 1. **Malformed convention references in Implementation Notes**: the convention
>    reference formatter lowercases and kebab-cases CONVENTIONS.md headings, so the output is
>    `§migration-patterns` when it should be `§Migration Patterns`. It should keep the
>    heading text exactly as written.
>    (in `shared/convention-utils.md`, the convention reference formatter)
> 2. **Tasks created with the wrong issue type**: task creation uses the Feature issue
>    type ID (10142) from Jira Configuration. It should use the level-0 Task type found
>    in Step 2.5 (10050 in ACME's custom scheme), so tasks are created as Feature instead of Task.
>    (in `skills/plan-feature/SKILL.md` Step 6a, task creation)
>
> These are independent root causes. They live in different modules, run in different
> phases of `/plan-feature` (description generation vs. Jira issue creation), and use
> different inputs. Fixing one has no effect on the other.
>
> Options:
> 1. **Proceed**: create a single Task covering all fixes
> 2. **Split**: I recommend creating separate Bugs for each independent issue,
>    then triaging each one individually
>
> Choose (1/2):

---

## Handling the response

- **1. Proceed**: continue to Step 5. Create one Task linked to ACME-502 (Task blocks
  Bug). It gets two reproducer tests as the first acceptance criteria and test
  requirements: (a) the `## Migration Patterns` heading produces `§Migration Patterns`;
  (b) task creation uses issue type 10050, not 10142. Then do Steps 5b, 5c and 7.
- **2. Split** (recommended): stop without creating a Task. Suggest the user file
  two separate Bugs:
  - Bug A: "Convention references in Implementation Notes use kebab-case instead of the
    heading text" (component: sdlc-workflow, area: `shared/convention-utils.md`)
  - Bug B: "plan-feature creates tasks with Feature issue type instead of the discovered
    Task type" (component: sdlc-workflow, area: `skills/plan-feature/SKILL.md` Step 6a)

  Then run `/triage-bug` on each one. When filing them, add the missing required
  `### **Environment / Version**` section. ACME-502 does not have it.
