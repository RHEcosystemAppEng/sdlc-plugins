# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   The convention reference formatter applies a kebab-case transform to CONVENTIONS.md section headings, producing references like `migration-patterns` instead of preserving the original title case `Migration Patterns`. This affects any skill that generates Implementation Notes referencing conventions.

2. **Task creation uses Feature issue type instead of Task issue type** (in `plan-feature/SKILL.md` Step 6a)
   The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of using a Task issue type ID (10050). This causes created tasks to have the wrong issue type in projects with custom issue type schemes.

These are independent defects in different modules and code paths. Bundling them into a single Task would mix unrelated fixes and make the reproducer tests and review harder to scope.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
