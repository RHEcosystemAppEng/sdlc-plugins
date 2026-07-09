# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   -- The convention reference formatter applies a kebab-case transform to CONVENTIONS.md
   section headings, producing `migration-patterns` instead of preserving the original
   heading case `Migration Patterns`. This affects all convention references in generated
   Implementation Notes.

2. **Task creation uses Feature issue type instead of Task issue type** (in `plan-feature/SKILL.md` Step 6a)
   -- The task creation logic reads `Feature issue type ID` (10142) from Jira Configuration
   instead of `Task issue type ID` (10050), causing created issues to have the wrong type
   in projects with custom issue type schemes.

These are in different modules and different code paths -- fixing one does not affect the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
