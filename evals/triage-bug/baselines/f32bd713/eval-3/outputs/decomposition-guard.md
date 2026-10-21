# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   - The convention reference formatter lowercases and kebab-cases CONVENTIONS.md section headings instead of preserving title case.
   - Example: heading `## Migration Patterns` produces reference `$migration-patterns` instead of `$Migration Patterns`.
   - Affected module: `shared/convention-utils.md`

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a)
   - The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID.
   - Result: tasks are created as Feature issues instead of Task issues in projects with custom issue type schemes.
   - Affected module: `plan-feature/SKILL.md`, Step 6a

These are independent root causes in different modules and code paths. Fixing one does not address the other.

Options:
1. **Proceed** -- create a single Task covering both fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
