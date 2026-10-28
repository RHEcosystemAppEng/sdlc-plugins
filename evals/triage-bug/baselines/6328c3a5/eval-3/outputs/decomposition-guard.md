# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** -- the convention reference formatter lowercases and kebab-cases CONVENTIONS.md section headings (e.g., `§migration-patterns` instead of `§Migration Patterns`). The defect is in the heading-to-reference conversion logic in `shared/convention-utils.md`.

2. **Wrong issue type in task creation** -- the task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of using the Task issue type ID from the dynamically discovered type-to-role mapping (Step 2.5). The defect is in `plan-feature/SKILL.md` Step 6a.

These are independent root causes in different modules with no shared state:
- Root cause 1 is in the shared convention formatting utility (`shared/convention-utils.md`), triggered during task description generation (Step 5).
- Root cause 2 is in the plan-feature skill's task creation logic (`plan-feature/SKILL.md` Step 6a), triggered during Jira issue creation (Step 6a).
- Fixing one does not affect the other. Each can be reproduced independently.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
