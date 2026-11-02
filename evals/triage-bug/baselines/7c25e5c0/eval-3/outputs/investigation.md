# Investigation: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type

Two distinct problems reported when running `/plan-feature`:
1. Convention references in generated task descriptions use kebab-case (`§migration-patterns`) instead of preserving the original heading case (`§Migration Patterns`).
2. Tasks are created with issue type "Feature" (ID 10142) instead of "Task" when the project has a custom issue type scheme.

---

## Finding 1: Convention Reference Formatter Uses Wrong Case Transform

**Location**: `shared/convention-utils.md`

The convention reference formatter is responsible for generating `§`-prefixed references to CONVENTIONS.md section headings. When it encounters a heading like `## Migration Patterns`, it converts it to kebab-case (`migration-patterns`) before emitting the reference.

**Root cause**: The formatter lowercases the heading text and replaces spaces with hyphens (kebab-case transform), producing `§migration-patterns`. It should instead preserve the original case from the CONVENTIONS.md heading, producing `§Migration Patterns`.

**Impact**: All convention references in generated Implementation Notes are malformed, making them unrecognizable to users who expect them to match the actual section headings in CONVENTIONS.md.

---

## Finding 2: Task Creation Uses Feature Issue Type ID Instead of Task

**Location**: `plan-feature/SKILL.md` Step 6a

The task creation logic in Step 6a reads the issue type ID from the project configuration to create Jira issues for planned tasks. It currently reads `featureIssueTypeId` (value 10142) from the Jira Configuration section of CLAUDE.md instead of reading `taskIssueTypeId`.

**Root cause**: Step 6a references the wrong configuration field. It uses `featureIssueTypeId` (10142, the Feature issue type) when it should use `taskIssueTypeId` (which would be the Task issue type, e.g., 10050 in the reporter's project).

**Impact**: All tasks created by `/plan-feature` are created as Feature issues instead of Task issues, breaking issue type schemes and potentially affecting workflows, boards, and reports that filter by issue type.

---

## Conclusion

These are **two independent root causes** in **different modules and code paths**:

1. **Convention formatting** (shared/convention-utils.md) -- a string transformation bug in a shared utility
2. **Task creation issue type** (plan-feature/SKILL.md Step 6a) -- a configuration field reference bug in the plan-feature skill

The two bugs share no code path, no shared state, and no causal relationship. They happen to co-occur when running `/plan-feature` because that skill invokes both the convention formatter and the task creation logic, but fixing one will not affect the other.

This triggers the **Decomposition Guard** -- the bug should be considered for splitting into separate issues before proceeding with task creation.
