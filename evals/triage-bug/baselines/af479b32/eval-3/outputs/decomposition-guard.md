# Decomposition Guard — ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** (in `shared/convention-utils.md`): The convention reference formatter applies kebab-case slugification to CONVENTIONS.md section headings, producing `§migration-patterns` instead of preserving the original heading format `§Migration Patterns`. This is a formatting logic defect in the shared convention utilities module, triggered during plan-feature Step 5 (convention-aware task enrichment).

2. **Wrong issue type in task creation** (in `plan-feature/SKILL.md` Step 6a): The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of using the Task issue type ID (level-0) from the type-to-role mapping discovered in Step 2.5. This causes created tasks to have issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

These two problems are caused by independent code paths in different modules:
- Root Cause 1 is in the shared convention formatting layer (`shared/convention-utils.md`), invoked during task description generation.
- Root Cause 2 is in the plan-feature task creation logic (`plan-feature/SKILL.md` Step 6a), invoked during Jira API calls.
- Fixing one does not affect the other. Each can be fixed and verified independently.

Options:
1. **Proceed** — create a single Task covering all fixes
2. **Split** — I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
