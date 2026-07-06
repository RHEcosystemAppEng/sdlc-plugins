# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- The convention reference formatter applies a slugify/kebab-case transform to CONVENTIONS.md section headings, producing `migration-patterns` instead of preserving the original title-case heading `Migration Patterns`.

2. **Task creation uses Feature issue type ID instead of Task** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID, causing created issues to be of type Feature rather than Task.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
