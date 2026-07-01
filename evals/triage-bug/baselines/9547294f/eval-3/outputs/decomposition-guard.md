# Decomposition Guard — ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) — The heading-to-reference formatting function applies kebab-case conversion (lowercase + hyphenation) to CONVENTIONS.md section headings, producing references like `migration-patterns` instead of preserving the original title-case heading text `Migration Patterns`.

2. **Task creation uses Feature issue type ID instead of Task** (in `plan-feature/SKILL.md` Step 6a) — The task creation logic reads the Feature issue type ID (10142) from Jira Configuration rather than a Task issue type ID, causing all created tasks to be issued as Feature type instead of Task type in projects with custom issue type schemes.

Options:
1. **Proceed** — create a single Task covering all fixes
2. **Split** — I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
