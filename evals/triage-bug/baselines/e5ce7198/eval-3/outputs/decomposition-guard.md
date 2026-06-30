# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   The formatter kebab-cases and lowercases convention headings instead of preserving the original title case. This causes references like `Migration Patterns` to appear as `migration-patterns` in generated task descriptions.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a)
   The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID. This causes created issues to have type "Feature" instead of "Task".

These are independent defects in different modules -- fixing one does not affect or depend on the other.

Options:
1. **Proceed** -- create a single Task covering both fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
