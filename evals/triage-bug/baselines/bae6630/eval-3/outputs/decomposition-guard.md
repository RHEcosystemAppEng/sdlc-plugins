# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** (in `shared/convention-utils.md`): The convention reference formatter lowercases and kebab-cases CONVENTIONS.md section headings when generating Implementation Notes references, producing `§migration-patterns` instead of the correct `§Migration Patterns`. The fix is isolated to the heading-to-reference conversion logic in the shared convention utilities module.

2. **Wrong issue type for created tasks** (in `plan-feature/SKILL.md` Step 6a): The task creation logic reads the Feature issue type ID (10142) from static Jira Configuration instead of using the Task issue type ID (10050) from the dynamically discovered type-to-role mapping built in Step 2.5. The fix is isolated to the issue type parameter selection in the plan-feature task creation step.

These are independent root causes in different modules -- the convention formatter is a shared utility (`shared/convention-utils.md`) while the issue type bug is in the plan-feature skill's task creation step (`plan-feature/SKILL.md` Step 6a). Fixing one does not affect or depend on fixing the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
