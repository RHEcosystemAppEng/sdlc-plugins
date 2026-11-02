# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter using wrong case transform** (in `shared/convention-utils.md`) -- converts section headings to kebab-case instead of preserving the original case from CONVENTIONS.md. For example, `## Migration Patterns` becomes `§migration-patterns` instead of `§Migration Patterns`.

2. **Task creation using Feature issue type ID instead of Task** (in `plan-feature/SKILL.md` Step 6a) -- reads `featureIssueTypeId` (10142) from configuration instead of the correct `taskIssueTypeId`, causing all planned tasks to be created as Feature issues.

These root causes are in different modules with no shared code path or causal relationship. Fixing one will not affect the other.

**Options:**

1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
