# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** -- the convention heading formatter in `shared/convention-utils.md` lowercases and kebab-cases CONVENTIONS.md section headings (producing `§migration-patterns` instead of the prescribed `§Migration Patterns`), causing all generated task Implementation Notes to have incorrectly formatted convention references.

2. **Wrong issue type for created tasks** -- the task creation logic in `plan-feature/SKILL.md` Step 6a reads the Feature issue type ID (10142) from Jira Configuration instead of using the level-0 Task type discovered dynamically in Step 2.5, causing all created tasks to have issue type "Feature" instead of "Task" in projects with custom issue type schemes.

These are independent root causes in different modules (`shared/convention-utils.md` vs `plan-feature/SKILL.md` Step 6a) with no shared code paths or state. Fixing one has no effect on the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
