# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** -- The convention section reference formatter in `shared/convention-utils.md` incorrectly applies kebab-case/slugify transformation to heading text, producing `migration-patterns` instead of preserving the original `Migration Patterns`. This affects any skill that generates Implementation Notes with convention references.

2. **Wrong issue type on created tasks** -- The task creation logic in `plan-feature/SKILL.md` Step 6a reads `Feature issue type ID` (10142) from CLAUDE.md instead of a Task-specific issue type ID, causing created issues to have type Feature instead of Task in projects with custom issue type schemes.

These two issues are in independent code paths (`shared/convention-utils.md` vs. `plan-feature/SKILL.md` Step 6a), affect different aspects of the output (description content vs. issue metadata), and can be fixed and tested independently with no shared regression risk.

Options:
1. **Proceed** -- create a single Task covering both fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually with `/triage-bug`

Choose (1/2):
