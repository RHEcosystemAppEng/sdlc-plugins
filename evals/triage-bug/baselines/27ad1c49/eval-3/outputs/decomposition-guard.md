# Decomposition Guard: ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   The convention reference formatter applies a kebab-case slug transformation to CONVENTIONS.md section headings, producing references like `migration-patterns` instead of preserving the original title-case heading text `Migration Patterns`.

2. **Task creation uses Feature issue type ID instead of Task** (in `plan-feature/SKILL.md` Step 6a)
   The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID, causing created tasks to have the wrong issue type.

These issues affect different modules and different code paths. Fixing one does not affect the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
