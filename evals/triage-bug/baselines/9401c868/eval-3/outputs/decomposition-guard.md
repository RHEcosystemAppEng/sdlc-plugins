# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** (in `shared/convention-utils.md`) -- The convention reference formatter lowercases and kebab-cases CONVENTIONS.md section headings, producing `section-migration-patterns` instead of preserving the original heading case `section-Migration Patterns`. This is a string formatting defect in the shared convention utility.

2. **Wrong issue type for created tasks** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of using the Task issue type (level 0) from the Step 2.5 type-to-role mapping, causing tasks to be created as Features instead of Tasks in projects with custom issue type schemes.

These are independent root causes in separate modules with no shared code path. Fixing one does not affect the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
