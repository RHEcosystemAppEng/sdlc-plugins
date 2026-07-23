# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   The convention reference formatter applies a `toLowerCase()` + kebab-case transformation to CONVENTIONS.md section headings, producing `§migration-patterns` instead of preserving the original heading text `§Migration Patterns`. This violates the prescribed format in `shared/convention-applicability-rules.md`. The fix is isolated to the heading-to-reference conversion logic in the shared convention utilities module.

2. **Task creation uses Feature issue type ID instead of Task** (in `plan-feature/SKILL.md` Step 6a)
   The task creation step reads `Feature issue type ID` (10142) from CLAUDE.md's Jira Configuration and uses it as the issue type for created tasks, instead of using the Task type (hierarchyLevel: 0) discovered dynamically in Step 2.5. In projects with custom issue type schemes (e.g., Task ID 10050), this causes Features to be created instead of Tasks. The fix is isolated to the issue type selection logic in Step 6a of plan-feature.

These are independent root causes in different modules with no shared code path. Fixing one does not resolve the other.

Options:
1. **Proceed** -- create a single Task covering both fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually with `/triage-bug`

Choose (1/2):

---

*Awaiting user input. Task creation is paused until the user selects an option.*
