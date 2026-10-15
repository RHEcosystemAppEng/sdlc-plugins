# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** (in `shared/convention-utils.md`) -- The convention reference formatter incorrectly applies kebab-case transformation to CONVENTIONS.md section headings. It produces `migration-patterns` instead of preserving the original heading text `Migration Patterns`. This is a string formatting defect in the shared convention utilities module.

2. **Wrong issue type in task creation** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of a Task-specific issue type ID. Projects with custom issue type schemes get tasks created as the wrong issue type. This is a configuration resolution defect in the plan-feature skill's task creation step.

These two issues have independent root causes in different modules, affect different code paths, and can be fixed independently without either fix affecting the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
