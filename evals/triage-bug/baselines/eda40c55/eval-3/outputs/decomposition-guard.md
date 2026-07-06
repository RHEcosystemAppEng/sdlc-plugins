# Decomposition Guard — ACME-502

## Step 6 — Multiple Independent Root Causes Detected

Investigation of ACME-502 ("Skill output is malformed and task creation uses wrong issue type") revealed two independent root causes located in **different modules and code paths**. The skill will **not** silently create a single Task bundling both fixes — it stops here and waits for user input.

---

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   The formatter lowercases and kebab-cases CONVENTIONS.md section headings when generating `§`-prefixed references, producing `§migration-patterns` instead of preserving the original title case `§Migration Patterns`.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md Step 6a`)
   The task creation logic reads `Feature issue type ID` (10142) from Jira Configuration instead of Task issue type ID (10050), causing created issues to be typed as Feature instead of Task.

These root causes are in different modules (`shared/convention-utils.md` vs `plan-feature/SKILL.md`), affect different code paths (text formatting vs Jira issue creation), and can be fixed and tested independently.

Options:
1. **Proceed** — create a single Task covering all fixes
2. **Split** — I recommend creating separate Bugs for each independent issue, then triaging each one individually

**Note**: This skill will NOT silently create a single Task bundling both fixes. No Task has been created. The skill is paused at the Decomposition Guard and awaits your decision before proceeding.

Choose (1/2):
