# Decomposition Guard — ACME-502 (Step 6)

The investigation found two **independent root causes** in different modules. Each one needs its own fix and its own reproducer test. This is not a single defect that appears in several files, so the Decomposition Guard applies. No Task has been created yet.

---

> This bug appears to involve multiple independent issues:
> 1. **Malformed convention references**: the convention reference formatter lowercases and kebab-cases CONVENTIONS.md headings, so Implementation Notes cite `§migration-patterns` instead of the verbatim heading `§Migration Patterns` (in `plugins/sdlc-workflow/shared/convention-utils.md`, convention reference formatter)
> 2. **Wrong issue type on task creation**: tasks are created with the Feature issue type ID (10142) from Jira Configuration instead of the Task-role issue type ID discovered in Step 2.5 (10050 in custom issue type schemes) (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a – Create the tasks)
>
> These two defects have no shared code path. Fixing one does not affect the other, and each can be reproduced and verified on its own.
>
> Options:
> 1. **Proceed**: create a single Task covering all fixes
> 2. **Split**: I recommend creating separate Bugs for each independent issue, then triaging each one individually
>
> Choose (1/2):

---

*Waiting for the user's answer. If the answer is 1, the skill continues with Step 5 (one Task with a reproducer test for each root cause), then 5b (link with "Blocks"), 5c (digest), and 7. If the answer is 2, the skill stops and suggests creating two separate Bug issues, one per root cause above, and running `/triage-bug` on each.*
