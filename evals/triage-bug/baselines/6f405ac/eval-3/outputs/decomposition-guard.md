# Decomposition Guard (Step 6)

This bug appears to involve multiple independent issues:

1. **Malformed convention references** -- the convention reference formatter in `shared/convention-applicability-rules.md` applies an incorrect kebab-case transformation to CONVENTIONS.md section headings, producing `§migration-patterns` instead of `§Migration Patterns`. This is a defect in the shared convention formatting utilities.

2. **Wrong issue type during task creation** -- the task creation logic in `plan-feature/SKILL.md` Step 6a reads the `Feature issue type ID` (10142) from Jira Configuration instead of a dedicated `Task issue type ID`, causing created issues to have type "Feature" instead of "Task". This is a defect in the plan-feature skill's Jira integration.

These are independent root causes in different modules (`shared/convention-applicability-rules.md` vs `plan-feature/SKILL.md` Step 6a) with no shared code paths or state. Fixing one does not affect the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
