# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- The convention reference formatter applies kebab-case to CONVENTIONS.md section headings, producing references like `migration-patterns` instead of preserving the original title case `Migration Patterns`. This is a defect in the shared convention formatting utility.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the `Feature issue type ID` (10142) from Jira Configuration instead of using the correct Task issue type ID (10050). This causes all plan-feature tasks to be created as Feature issues instead of Task issues.

These root causes are in different modules and affect independent code paths. Fixing one does not affect the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
