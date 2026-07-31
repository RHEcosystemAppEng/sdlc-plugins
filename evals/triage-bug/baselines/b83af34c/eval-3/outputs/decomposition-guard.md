# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   - The convention reference formatter applies a kebab-case transform to CONVENTIONS.md section headings, producing references like `§migration-patterns` instead of preserving the original heading text `§Migration Patterns`.
   - Affected module: `shared/convention-utils.md` (shared formatting utilities)
   - Correct behavior defined in: `shared/convention-applicability-rules.md` (line 57)

2. **Task creation uses Feature issue type ID instead of Task** (in `plan-feature/SKILL.md` Step 6a)
   - The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of using the Task issue type ID discovered dynamically in Step 2.5, causing created issues to have the wrong issue type.
   - Affected module: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a
   - Related logic: Step 2.5 (dynamic issue type discovery, which correctly identifies Task at hierarchyLevel 0)

These root causes are in different modules, affect different code paths, and can be fixed independently.

Options:
1. **Proceed** -- create a single Task covering both fixes
2. **Split** -- create separate Bug issues for each independent root cause, then triage each one individually with its own fix Task

Choose (1/2):
