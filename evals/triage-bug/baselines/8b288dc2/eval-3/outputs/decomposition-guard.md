# Decomposition Guard — ACME-502

## Multiple Independent Root Causes Detected

Investigation of ACME-502 reveals that this bug involves **multiple independent issues** rooted in **different modules** with **separate code paths**. A single remediation task would conflate unrelated fixes, so the Decomposition Guard is triggered.

---

## Independent Issues Identified

### Issue 1: Malformed convention references — wrong case transform

- **Affected file/module:** `shared/convention-utils.md`
- **Problem:** The convention reference formatter incorrectly lowercases and kebab-cases heading names when generating `§`-prefixed references. For example, the heading `## Migration Patterns` produces `§migration-patterns` instead of `§Migration Patterns`.
- **Impact:** Implementation Notes in generated task descriptions contain malformed convention references that do not match the actual CONVENTIONS.md section headings.

### Issue 2: Wrong issue type in task creation — reads Feature ID instead of Task ID

- **Affected file/module:** `plan-feature/SKILL.md` Step 6a
- **Problem:** The task creation logic reads the Feature issue type ID (10142) from the Jira Configuration instead of using a Task-specific issue type ID. When the project defines a custom issue type scheme with Task ID 10050, the created issue is assigned the wrong type.
- **Impact:** Tasks created by `/plan-feature` are filed as Feature issues instead of Task issues in Jira.

---

## Options

1. **Proceed** — Create a single Task covering all fixes (both the convention formatter in `shared/convention-utils.md` and the issue type lookup in `plan-feature/SKILL.md` Step 6a).

2. **Split** — Create separate Bug issues for each independent root cause, then triage each individually:
   - **Bug A:** Malformed convention references in `shared/convention-utils.md` (case transform fix)
   - **Bug B:** Wrong issue type in `plan-feature/SKILL.md` Step 6a (read Task ID instead of Feature ID)

---

## Awaiting User Input

The skill **WAITS** for user input before proceeding. It does **NOT** silently create a single Task when multiple independent root causes are detected. Please select one of the options above to continue.
