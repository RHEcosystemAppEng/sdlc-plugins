# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** (in `shared/convention-applicability-rules.md`): The convention reference formatter converts CONVENTIONS.md section headings into kebab-case slugs (e.g., `§migration-patterns`) instead of preserving the original heading text (e.g., `§Migration Patterns`). This is a formatting defect in the shared convention utilities used during task description generation.

2. **Wrong issue type for task creation** (in `plan-feature/SKILL.md` Step 6a): The task creation logic uses the Feature issue type ID (10142) from the static Jira Configuration rather than the Task issue type ID discovered dynamically by Step 2.5. This causes tasks to be created as Feature type instead of Task type in projects with custom issue type schemes.

These two issues are in independent code paths -- the convention formatting logic in the shared module and the issue type selection logic in plan-feature's task creation step. Fixing one does not affect or depend on the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
