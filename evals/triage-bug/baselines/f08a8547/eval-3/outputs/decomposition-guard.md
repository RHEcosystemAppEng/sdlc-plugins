# Decomposition Guard -- ACME-502

## Step 6 -- Decomposition Guard

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses kebab-case instead of preserving heading text** (in `shared/convention-utils.md`)
   - The function that constructs `§` references from CONVENTIONS.md section headings applies a kebab-case transformation (e.g., `## Migration Patterns` becomes `§migration-patterns` instead of `§Migration Patterns`).
   - This contradicts the format specified in `shared/convention-applicability-rules.md` and `plan-feature/SKILL.md`.

2. **Task creation uses Feature issue type ID instead of dynamically discovered Task type** (in `skills/plan-feature/SKILL.md` Step 6a)
   - The `jira.create_issue` call in Step 6a reads the Feature issue type ID (10142) from static Jira Configuration instead of using the level-0 (Task) type ID discovered in Step 2.5's type-to-role mapping.
   - In projects with custom issue type schemes where Task has a different ID (e.g., 10050), this causes tasks to be created as Feature issues.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):

---

### Rationale for Decomposition

These two problems are independent because:

- They reside in **different modules**: the convention formatter is in `shared/convention-utils.md` (a shared utility), while the issue type logic is in `skills/plan-feature/SKILL.md` Step 6a (skill-specific task creation).
- They affect **different code paths**: convention enrichment (Step 5) vs. Jira issue creation (Step 6a).
- They produce **different symptoms**: malformed text in task descriptions vs. wrong issue type on created issues.
- **Fixing one does not fix the other**: correcting the convention formatter has no effect on issue type resolution, and vice versa.

### If "Split" is chosen

I recommend creating two separate Bug issues:

1. **Bug: Convention reference formatter produces kebab-case instead of title case**
   - Component: sdlc-workflow
   - Affected file: `shared/convention-utils.md`
   - Steps to Reproduce: Add a CONVENTIONS.md with section `## Migration Patterns`, run `/plan-feature`, and observe that Implementation Notes contain `§migration-patterns` instead of `§Migration Patterns`.

2. **Bug: plan-feature creates tasks with Feature issue type instead of Task**
   - Component: sdlc-workflow
   - Affected file: `skills/plan-feature/SKILL.md` Step 6a
   - Steps to Reproduce: Configure a project with a custom issue type scheme where Task has ID 10050, run `/plan-feature`, and observe that the created issue has type Feature (10142) instead of Task (10050).

Each bug can then be triaged individually with `/triage-bug`, producing a focused single-root-cause Task for `/implement-task` to consume.
