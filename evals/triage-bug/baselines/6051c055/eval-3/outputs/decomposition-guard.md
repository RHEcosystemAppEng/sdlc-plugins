# Decomposition Guard — ACME-502

## Step 6 — Multiple Independent Root Causes Detected

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   - The convention formatter applies a kebab-case transformation to CONVENTIONS.md section headings, producing `§migration-patterns` instead of preserving the original heading case `§Migration Patterns`.

2. **Task creation uses Feature issue type ID instead of Task** (in `plan-feature/SKILL.md Step 6a`)
   - The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID (10050) from the project's custom issue type scheme.

These root causes are in **different modules** (`shared/convention-utils.md` vs. `plan-feature/SKILL.md`) and affect **independent code paths** (convention formatting vs. Jira issue creation). Fixing one does not fix the other.

Options:
1. **Proceed** — create a single Task covering all fixes
2. **Split** — I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):

---

**Execution paused.** Waiting for user input before proceeding. The skill does NOT silently create a single Task bundling both fixes.
