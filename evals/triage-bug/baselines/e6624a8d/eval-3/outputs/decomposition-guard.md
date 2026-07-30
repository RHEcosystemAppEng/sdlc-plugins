# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** (in `shared/convention-utils.md`): The convention reference formatter incorrectly kebab-cases CONVENTIONS.md section headings, producing `§migration-patterns` instead of `§Migration Patterns`. The formatter applies a slug normalization that should preserve the original heading text. This affects the Convention-aware task enrichment pipeline in plan-feature Step 5.

2. **Wrong issue type in task creation** (in `plan-feature/SKILL.md` Step 6a): The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID from the type-to-role mapping discovered in Step 2.5. This causes tasks to be created as Feature issues instead of Task issues when the project uses a custom issue type scheme.

These are independent defects in separate modules with no shared code path. Fixing one does not affect the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
