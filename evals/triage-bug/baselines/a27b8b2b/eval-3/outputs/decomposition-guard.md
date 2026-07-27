# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatting produces kebab-case instead of title case** (in `plugins/sdlc-workflow/shared/convention-applicability-rules.md` and the convention-aware task enrichment logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 5)
   - The convention reference formatter normalizes CONVENTIONS.md section headings to kebab-case slug format (e.g., `§migration-patterns`) instead of preserving the original title-case heading text (e.g., `§Migration Patterns`).

2. **Task creation uses Feature issue type ID instead of Task** (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a)
   - The task creation logic reads the `Feature issue type ID` (10142) from the static Jira Configuration in CLAUDE.md instead of using the dynamically discovered Task type (level 0) from the Step 2.5 type-to-role mapping, causing created issues to be of type Feature instead of Task.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):

---

**Rationale for triggering the guard**: These two defects have independent root causes in different modules (`shared/convention-applicability-rules.md` vs. `plan-feature/SKILL.md` Step 6a), affect different code paths (convention string formatting vs. Jira issue type selection), share no state, and can be fixed and verified independently. A single Task bundling both fixes would conflate unrelated changes, making the fix harder to review and test. Splitting into separate Bugs ensures each fix is scoped, testable, and reviewable in isolation.
