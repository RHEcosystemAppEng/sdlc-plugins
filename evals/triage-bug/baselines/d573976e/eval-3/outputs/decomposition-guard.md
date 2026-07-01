# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** (in `shared/convention-utils.md`) -- The convention reference formatter lowercases and kebab-cases CONVENTIONS.md section headings (e.g., `## Migration Patterns` becomes `migration-patterns` instead of `Migration Patterns`). This is a defect in the shared convention utility's heading-to-reference conversion logic. It affects all skills that generate convention references in task descriptions.

2. **Wrong issue type for created tasks** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID. Under custom issue type schemes where Task has a different ID (e.g., 10050), tasks are created as Feature issues instead of Task issues. This is a defect in plan-feature's task creation step.

These are independent root causes in different modules with different code paths. Fixing one does not address the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
