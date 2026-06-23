# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention Reference Case Transform** (`shared/convention-utils.md`) -- The convention reference formatter applies kebab-case transform to section headings instead of preserving the original title case, producing `§migration-patterns` instead of `§Migration Patterns`.
2. **Task Creation Issue Type Mismatch** (`plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID, causing created issues to have the wrong type.

These root causes are in different modules and affect independent code paths.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
