# Investigation Findings -- ACME-502

## Bug Summary

**Issue**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow

The bug report describes two distinct problems observed when running `/plan-feature`:
1. Convention references in generated task descriptions use kebab-case (`§migration-patterns`) instead of preserving the original title case (`§Migration Patterns`).
2. Tasks are created with issue type "Feature" (ID 10142) instead of "Task" (ID 10050).

---

## Root Cause 1: Convention Reference Formatter Uses Wrong Case Transform

**What is broken**: The convention reference formatter in `shared/convention-utils.md` transforms section headings into kebab-case when generating `§`-prefixed convention references. For example, a CONVENTIONS.md heading `## Migration Patterns` is rendered as `§migration-patterns` instead of `§Migration Patterns`.

**Why it is broken**: The formatter applies a `toKebabCase()` (or equivalent lowercase-and-hyphenate) transform to heading text before emitting the `§` reference. This transform is appropriate for generating URL-safe anchors but is incorrect for human-readable convention references that should preserve the original heading text.

**Where it is broken**: `shared/convention-utils.md` -- the convention reference formatting logic that converts CONVENTIONS.md headings into `§`-prefixed references for use in Implementation Notes.

**How to verify the fix**: A reproducer test should:
1. Provide a CONVENTIONS.md with a heading `## Migration Patterns`.
2. Invoke the convention reference formatter on that heading.
3. Assert the output is `§Migration Patterns` (title case preserved), not `§migration-patterns` (kebab-case).

---

## Root Cause 2: Task Creation Uses Feature Issue Type ID Instead of Task

**What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID (10050) when creating the fix task.

**Why it is broken**: The task creation step references `Feature issue type ID` from the `## Jira Configuration` section of CLAUDE.md, but the correct field for creating Tasks is the Task issue type ID. When a project has a custom issue type scheme with a distinct Task issue type (ID 10050), using the Feature ID (10142) results in the wrong issue type being assigned.

**Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the issue creation call passes `issuetype.id = 10142` (Feature) instead of `issuetype.id = 10050` (Task).

**How to verify the fix**: A reproducer test should:
1. Configure a project with Jira Configuration containing `Feature issue type ID: 10142` and a custom issue type scheme where Task has ID 10050.
2. Invoke the task creation logic.
3. Assert that the created issue has `issuetype.id = 10050` (Task), not `issuetype.id = 10142` (Feature).

---

## Independence Assessment

These two root causes are **independent**:

- **Root Cause 1** is located in `shared/convention-utils.md` (shared utility module for convention formatting). It affects how convention references are rendered in task descriptions.
- **Root Cause 2** is located in `plan-feature/SKILL.md` Step 6a (task creation logic). It affects which Jira issue type is assigned to created tasks.

The two defects are in **different modules** and **different code paths**. They do not share a common underlying cause. Fixing one does not fix the other. Each requires a targeted change in its respective module.

This triggers the **Decomposition Guard** (Step 6) -- the investigation must present these findings to the user and ask whether to proceed with a single Task or split into separate Bugs before creating any fix tasks.
