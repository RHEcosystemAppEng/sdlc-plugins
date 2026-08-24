# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** (in `shared/convention-utils.md`) -- The convention reference formatter incorrectly lowercases and kebab-cases CONVENTIONS.md section headings when generating references for Implementation Notes. For example, `## Migration Patterns` becomes `section-migration-patterns` instead of `section-Migration Patterns`. This is a formatting/transformation bug in the shared convention utilities module.

2. **Wrong issue type in task creation** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID, causing created issues to have the wrong type. This is a configuration-lookup bug in the plan-feature skill's issue creation step.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):

---

## Rationale for Decomposition

These two problems are caused by independent code paths in different modules:

- **Root cause 1** is in the shared convention utilities (`shared/convention-utils.md`), which handles text transformation of CONVENTIONS.md headings into reference format.
- **Root cause 2** is in the plan-feature skill (`plan-feature/SKILL.md` Step 6a), which handles Jira issue creation and issue type selection.

The fixes have no coupling -- changing the convention formatter has no effect on issue type selection, and vice versa. Each fix can be developed, tested, and reviewed independently. Bundling them into a single Task would mix unrelated changes, making the fix harder to review and increasing the risk of regressions.

**Recommendation**: Choose option 2 (Split) to create two separate Bug issues, then triage each independently with `/triage-bug`. This produces two focused Tasks, each with its own reproducer test, resulting in cleaner PRs and more targeted verification.
