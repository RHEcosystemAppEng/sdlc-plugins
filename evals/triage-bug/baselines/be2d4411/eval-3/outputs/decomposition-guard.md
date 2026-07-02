# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`): The heading-to-reference conversion lowercases and kebab-cases CONVENTIONS.md section headings, producing `section-migration-patterns` instead of preserving the original case `section-Migration Patterns`.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a): The `jira.create_issue` call uses the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID, causing all planned tasks to be created as Feature issues.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):

---

## Rationale for triggering the Decomposition Guard

These two problems are independent because:

- They are located in **different modules**: `shared/convention-utils.md` (shared utility layer) vs. `plan-feature/SKILL.md` (skill-specific task creation logic).
- They affect **different code paths**: convention reference formatting pipeline vs. Jira issue creation pipeline.
- They have **no shared dependency**: fixing one does not affect or require fixing the other.
- They require **different reproducer tests**: one tests string formatting output, the other tests Jira API call parameters.

Per Step 6 of the triage-bug skill, the skill must not silently create a single Task that bundles unrelated fixes. The user must choose how to proceed before any Task is created.

### If the user chooses "1. Proceed"

A single Task will be created covering both fixes, with acceptance criteria and test requirements addressing both root causes. The Task will reference ACME-502 for traceability.

### If the user chooses "2. Split"

The user should create two separate Bug issues:

- **Bug A**: "Convention reference formatter lowercases and kebab-cases headings instead of preserving original case" (Component: sdlc-workflow, affects `shared/convention-utils.md`)
- **Bug B**: "plan-feature task creation uses Feature issue type ID instead of Task issue type ID" (Component: sdlc-workflow, affects `plan-feature/SKILL.md` Step 6a)

Each Bug can then be triaged individually with `/triage-bug`, producing focused, single-responsibility Tasks.
