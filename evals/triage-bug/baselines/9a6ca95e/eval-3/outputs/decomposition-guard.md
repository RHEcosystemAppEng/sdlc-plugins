This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- The convention reference formatter applies a kebab-case transform to CONVENTIONS.md section headings, producing references like `migration-patterns` instead of preserving the original title case `Migration Patterns`. This is a formatting/string-transform bug in the shared convention utilities module.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of using a Task issue type ID. When a project has a custom issue type scheme, created issues are incorrectly typed as Feature instead of Task. This is a configuration-lookup bug in the plan-feature task creation step.

These root causes are in different modules and affect independent code paths. Fixing one does not require or affect the other.

Options:
1. **Proceed** -- create a single Task covering both fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually with `/triage-bug`

Choose (1/2):
