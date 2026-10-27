# Investigation: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

## Configuration Validated (Step 0)

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

## Parsed Description (Step 1)

### Issue Description

Two distinct problems occur when running `/plan-feature`:
1. The generated task description has malformed Implementation Notes -- convention references use the wrong section heading format (e.g., `section-migration-patterns` instead of `section-Migration Patterns`).
2. The task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

### Steps to Reproduce

1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

### Expected Result

- Implementation Notes should reference conventions as `section-Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

### Actual Result

- Implementation Notes reference conventions as `section-migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

### Attachments

None.

### Suggested Fix (Optional)

These are likely two separate bugs:
- The convention reference formatter lowercases and kebab-cases headings incorrectly.
- The task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

## Code-Path Tracing (Step 2)

The entry point is the `/plan-feature` skill invocation. Two independent code paths diverge from this entry point:

1. **Convention reference formatting path**: When generating the task description's Implementation Notes, the skill reads `CONVENTIONS.md` headings and formats them as section references. This formatting logic is handled by `shared/convention-utils.md`.

2. **Task creation path**: When creating the Jira issue, the skill selects an issue type ID from the project configuration. This logic is handled by `plan-feature/SKILL.md` Step 6a.

## Codebase Investigation (Step 3)

### Root Cause 1: Convention reference formatter (shared/convention-utils.md)

**What is broken**: The convention reference formatter in `shared/convention-utils.md` applies a lowercase-and-kebab-case transform to CONVENTIONS.md section headings when generating section references for Implementation Notes.

**Why it is broken**: The formatter normalizes headings by converting them to lowercase and replacing spaces with hyphens (kebab-case). For example, the heading `## Migration Patterns` is transformed to `migration-patterns`, producing the reference `section-migration-patterns`. The correct behavior is to preserve the original title case from the heading, producing `section-Migration Patterns`.

**Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference transformation function.

**Affected files**:
- `shared/convention-utils.md` -- contains the heading formatting logic that incorrectly lowercases and kebab-cases headings

### Root Cause 2: Task creation issue type (plan-feature/SKILL.md Step 6a)

**What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a uses the Feature issue type ID (10142) instead of the Task issue type ID (10050) when creating Jira issues.

**Why it is broken**: Step 6a reads the `Feature issue type ID` field from CLAUDE.md's Jira Configuration section rather than using the correct Task issue type ID. When the project has a custom issue type scheme where Task has its own ID (10050), the wrong issue type is selected because the code references the Feature configuration field instead of a Task-specific field.

**Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the issue type selection when calling `jira.create_issue`.

**Affected files**:
- `plan-feature/SKILL.md` -- Step 6a issue creation logic that references the wrong issue type ID field

## Root Cause Analysis (Step 4)

### Summary

ACME-502 describes two symptoms that stem from **two independent root causes** in **separate modules**:

| # | Symptom | Root Cause | Affected Module | Fix Scope |
|---|---------|-----------|-----------------|-----------|
| 1 | Convention references use kebab-case (`section-migration-patterns`) instead of title case (`section-Migration Patterns`) | Heading formatter applies lowercase + kebab-case transform instead of preserving original case | `shared/convention-utils.md` | Fix the heading-to-reference transform to preserve original title case |
| 2 | Created issue is type Feature (10142) instead of Task (10050) | Task creation reads `Feature issue type ID` config field instead of Task issue type ID | `plan-feature/SKILL.md` Step 6a | Change the config field lookup to use the correct Task issue type ID |

### Independence Assessment

These two root causes are **independent**:

- They reside in **different modules** (`shared/convention-utils.md` vs `plan-feature/SKILL.md`)
- They affect **different concerns** (text formatting vs Jira API call parameters)
- Fixing one does not fix or affect the other
- They can be reproduced independently
- They require separate test coverage

This triggers the **Decomposition Guard** (Step 6) -- the skill should not silently create a single Task bundling unrelated fixes.

### Reproducer Strategy

**For Root Cause 1**: Create a test that provides a CONVENTIONS.md with a titled heading (e.g., `## Migration Patterns`), runs the convention reference formatter, and asserts the output preserves the original case (`section-Migration Patterns`) rather than kebab-casing it (`section-migration-patterns`).

**For Root Cause 2**: Create a test that configures a project with Task issue type ID 10050 and Feature issue type ID 10142, runs the task creation step, and asserts the created issue uses issue type ID 10050 (Task), not 10142 (Feature).

### Persistence Impact

No persistence boundary identified. Convention references and issue type IDs are computed at task-creation time and passed directly to the Jira API. No database writes of these values occur in the application's own data store. The incorrect values exist only in already-created Jira issues, which would need manual correction but do not require a data migration in the application.
