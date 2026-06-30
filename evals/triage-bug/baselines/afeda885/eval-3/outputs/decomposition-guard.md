This bug appears to involve multiple independent issues:
1. Convention reference formatter using wrong case transform (in shared/convention-utils.md) -- the formatter lowercases and kebab-cases convention headings instead of preserving title case, producing references like `migration-patterns` instead of `Migration Patterns`
2. Task creation using Feature issue type ID instead of Task (in plan-feature/SKILL.md Step 6a) -- reads Feature issue type ID (10142) from Jira Configuration instead of the Task issue type, causing created tasks to have the wrong issue type

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
