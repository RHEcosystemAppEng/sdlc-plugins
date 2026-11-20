# Decomposition Guard — ACME-502 (Step 6)

The investigation (Steps 2–4) found two independent root causes in different modules. They share no code path, and each needs its own separate fix. Creating one Task that bundles both fixes is not done automatically. The following prompt is presented to the user first:

---

> This bug appears to involve multiple independent issues:
>
> 1. **Malformed convention references**: the convention reference formatter lowercases and kebab-cases CONVENTIONS.md section headings, so Implementation Notes contain `§migration-patterns` where they should contain `§Migration Patterns`. (in `plugins/sdlc-workflow/skills/shared/convention-utils.md`, convention reference formatter)
> 2. **Wrong issue type on task creation**: task creation passes the Feature issue type ID (10142) from Jira Configuration to `jira.create_issue` where it should pass the discovered Task issue type ID (10050), so tasks are created as Features in projects with custom issue type schemes. (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a, Create the tasks)
>
> These defects are in different modules, have different causes (string formatting vs. configuration lookup), and share no code path. Either can be fixed and verified without the other.
>
> Options:
> 1. **Proceed**: create a single Task covering all fixes
> 2. **Split**: I recommend creating separate Bugs for each independent issue, then triaging each one individually
>
> Choose (1/2):

---

## Recommendation

**Option 2 (Split)** is recommended. Each fix gets its own reproducer test, its own review, and its own revert path. This also follows the rule that each generated Task is scoped to a single fix.

## Follow-up behavior

- **If 2 (Split)**: stop. Do not create a Task or a link. Suggest that the user files two Bugs, for example:
  - "Convention references in Implementation Notes are kebab-cased instead of matching the CONVENTIONS.md heading" (component: sdlc-workflow, `shared/convention-utils.md`)
  - "plan-feature creates tasks with the Feature issue type instead of Task under custom issue type schemes" (component: sdlc-workflow, `plan-feature/SKILL.md` Step 6a)

  Then run `/triage-bug <new-key>` for each one. The new Bugs should also include the `### **Environment / Version**` section, which ACME-502 is missing.
- **If 1 (Proceed)**: create one Task, labeled `ai-generated-jira`, with Target Branch `main`. Its acceptance criteria are, in order:
  1. Reproducer tests for both defects. The first reproducer asserts that `## Migration Patterns` produces `§Migration Patterns`. The second asserts that the created issue type is 10050.
  2. Fix criteria for the formatter and for Step 6a.
  3. No regressions.

  Then link the Task to ACME-502 with link type Blocks (Task is inward, Bug is outward), post the digest comment, and report the result.
