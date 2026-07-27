# Decomposition Guard — ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** (in `plugins/sdlc-workflow/shared/convention-applicability-rules.md`) — The convention reference formatter lowercases and kebab-cases CONVENTIONS.md section headings, producing `§migration-patterns` instead of `§Migration Patterns`. This is a formatting bug in the shared convention utilities module that affects how convention references are rendered in task Implementation Notes.

2. **Wrong issue type in task creation** (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a) — The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of using the dynamically discovered Task issue type ID from Step 2.5. This causes created issues to be of type "Feature" instead of "Task" in projects with custom issue type schemes.

These are independent root causes in different modules — the convention formatter in `shared/convention-applicability-rules.md` and the task creation logic in `plan-feature/SKILL.md` Step 6a. Each can be fixed independently without affecting the other.

Options:
1. **Proceed** — create a single Task covering all fixes
2. **Split** — I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
