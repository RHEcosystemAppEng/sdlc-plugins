# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- The heading-to-reference formatter lowercases and kebab-cases CONVENTIONS.md section headings instead of preserving the original title case. For example, `## Migration Patterns` becomes `section-migration-patterns` instead of `section-Migration Patterns`.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID (10050), causing created issues to be typed as Feature instead of Task.

These are independent defects in separate modules with no shared code path. Fixing one does not address the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
