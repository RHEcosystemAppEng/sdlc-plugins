# Decomposition Guard -- ACME-502

## Step 6 -- Decomposition Guard Prompt

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   - The heading-to-reference formatter lowercases and kebab-cases CONVENTIONS.md section headings instead of preserving title case.
   - Example: `## Migration Patterns` is referenced as `migration-patterns` instead of `Migration Patterns`.
   - Affects: Implementation Notes generation in all tasks produced by `/plan-feature`.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a)
   - The `jira.create_issue` call uses the Feature issue type ID (10142) from CLAUDE.md Jira Configuration instead of a Task-specific issue type ID (10050).
   - Affects: All tasks created by `/plan-feature` in projects with custom issue type schemes.

These root causes are in **different modules** (`shared/convention-utils.md` vs `plan-feature/SKILL.md`) and involve **independent code paths** (heading formatting vs Jira issue creation). Fixing one does not fix or affect the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):

---

**Note**: This skill will NOT silently create a single Task bundling both fixes. User input is required before proceeding. If the user chooses option 2 (Split), the skill will stop and suggest creating two separate Bug issues -- one for the convention formatter defect and one for the task creation issue type defect -- each to be triaged individually via `/triage-bug`.
