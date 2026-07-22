# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** -- The convention reference formatter produces kebab-case section slugs (`migration-patterns`) instead of preserving the original heading text (`Migration Patterns`). This is in the shared convention utilities module (`plugins/sdlc-workflow/shared/convention-applicability-rules.md`), which is consumed by both plan-feature and verify-pr skills.

2. **Wrong issue type on task creation** -- The task creation logic in plan-feature Step 6a uses the Feature issue type ID (10142) from the static Jira Configuration instead of the Task type ID (10050) from the dynamic type-to-role mapping built in Step 2.5. This is in the plan-feature skill (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a).

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
