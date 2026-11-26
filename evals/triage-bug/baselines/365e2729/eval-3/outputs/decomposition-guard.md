# Decomposition Guard — ACME-502 (Step 6)

Prompt shown to the user before any Task is created:

---

> This bug appears to involve multiple independent issues:
> 1. **Malformed convention references**: the convention reference formatter turns CONVENTIONS.md headings into kebab-case slugs. For example `## Migration Patterns` is written as `§migration-patterns` instead of `§Migration Patterns` in the generated Implementation Notes. (in `plugins/sdlc-workflow/shared/convention-utils.md`, the convention formatter)
> 2. **Wrong issue type on task creation**: tasks are created with the configured Feature issue type ID (10142) instead of the Task issue type found for the project (10050 in a custom issue type scheme). (in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a, the task creation logic)
>
> These fixes share no code path, input, or symbol. Fixing one does not fix the other, and each can happen without the other. They only appeared together because both are hit in the same `/plan-feature` run.
>
> Options:
> 1. **Proceed**: create a single Task covering all fixes
> 2. **Split**: I recommend creating separate Bugs for each independent issue, then triaging each one individually
>
> Choose (1/2):

---

## Handling of the response

- **1. Proceed**: continue to Step 5. Create one Task linked to ACME-502 (Blocks). The two reproducer tests come first in Acceptance Criteria and Test Requirements, then both fixes, then a no-regression check. Then post the digest (Step 5c) and report (Step 7).
- **2. Split** (recommended): stop. Suggest that the user:
  1. Create a Bug for issue 1 (convention reference formatting in `shared/convention-utils.md`).
  2. Create a Bug for issue 2 (Task issue type selection in `plan-feature/SKILL.md` Step 6a).
  3. Optionally link both to ACME-502 (or close ACME-502 as split), then run `/triage-bug <new-key>` on each.

Also worth telling the user: ACME-502 has no `### **Environment / Version**` section, which the bug template requires. Each new Bug should include it so triage is not blocked and the Affects Version can be set.
