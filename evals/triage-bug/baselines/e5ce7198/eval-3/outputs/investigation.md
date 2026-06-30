# Investigation Findings -- ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow

The bug reports two distinct problems when running `/plan-feature`:
1. Generated task descriptions contain malformed convention references (kebab-case instead of title case).
2. Tasks are created with issue type "Feature" instead of "Task".

## Step 1 -- Fetch and Parse Bug

All required description sections are present and well-formed:
- **Issue Description**: Present -- describes two distinct problems.
- **Steps to Reproduce**: Present -- four numbered steps covering project setup, CONVENTIONS.md creation, `/plan-feature` invocation, and output observation.
- **Expected Result**: Present -- convention references should use title case (`Migration Patterns`); issue type should be Task (ID 10050).
- **Actual Result**: Present -- convention references are kebab-cased (`migration-patterns`); issue type is Feature (ID 10142).
- **Attachments**: Present (None).
- **Suggested Fix** (optional): Present -- reporter suspects two separate bugs.

Bug metadata:
- Issue type ID: 10020 (matches Bug Configuration -- validated)
- Labels: reported-by-user
- Component: sdlc-workflow

## Step 2 -- Code-Path Tracing

### Trace 1: Convention reference formatting

Entry point: `/plan-feature` invocation at Step 3 of the reproduction steps.

The plan-feature skill generates task descriptions that include Implementation Notes referencing conventions from CONVENTIONS.md. When a convention heading such as `## Migration Patterns` is referenced, the formatter should produce `Migration Patterns` (preserving the original title case from the heading).

Tracing the code path:
1. `/plan-feature` reads `CONVENTIONS.md` and extracts section headings.
2. The heading text is passed to a formatting utility in `shared/convention-utils.md`.
3. The formatter applies a case transform before emitting the reference.

### Trace 2: Issue type selection during task creation

Entry point: `/plan-feature` invocation at Step 4 of the reproduction steps.

When creating a Task issue in Jira, the plan-feature skill must use the correct issue type ID for "Task". The project's CLAUDE.md Jira Configuration contains `Feature issue type ID: 10142`, but the Task issue type ID is separate and project-specific (in this reproduction case, ID 10050).

Tracing the code path:
1. `/plan-feature` reaches Step 6a where it calls `jira.create_issue(...)`.
2. The code reads the issue type ID from the project configuration.
3. The logic selects the wrong configuration field.

## Step 3 -- Codebase Investigation

### Root Cause 1: Convention reference formatter applies wrong case transform

**Affected file**: `shared/convention-utils.md`

The convention reference formatter contains a case transformation step that converts section headings to kebab-case and lowercases them before emitting references. Specifically, a heading like `## Migration Patterns` is transformed to `migration-patterns`, producing the reference `migration-patterns` instead of preserving the original heading text `Migration Patterns`.

**What is broken**: The formatter applies `kebab-case + lowercase` instead of preserving the original heading text as-is.

**Why it is broken**: The formatting function was likely written to produce URL-friendly slugs (appropriate for anchor links) but is incorrectly used for display references where the original title-case heading should be preserved.

**Where it is broken**: The case transform logic in `shared/convention-utils.md` -- the function that converts convention headings to reference format.

**How to verify**: A test should pass a heading `## Migration Patterns` through the formatter and assert the output is `Migration Patterns` (title case preserved), not `migration-patterns`.

### Root Cause 2: Task creation uses Feature issue type ID instead of Task issue type ID

**Affected file**: `plan-feature/SKILL.md` (Step 6a)

The task creation logic in Step 6a reads the `Feature issue type ID` (10142) from the Jira Configuration section of CLAUDE.md instead of reading the Task issue type ID. When the project has a custom issue type scheme where Task has a different ID (e.g., 10050), the created issue ends up with the wrong type.

**What is broken**: The field lookup in Step 6a references `Feature issue type ID` instead of the Task issue type ID.

**Why it is broken**: The CLAUDE.md Jira Configuration section contains `Feature issue type ID: 10142` and the code reads this value when creating tasks, rather than looking up a separate Task issue type ID field or using a hardcoded/configured Task type ID.

**Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `create_issue` call's `issue_type` parameter sources the wrong configuration field.

**How to verify**: A test should invoke the task creation path with a project configuration where Task ID differs from Feature ID, and assert the created issue's `issuetype.id` matches the configured Task ID, not the Feature ID.

## Independence Assessment

These two root causes are **independent**:

| Dimension | Root Cause 1 | Root Cause 2 |
|-----------|-------------|-------------|
| Affected file | `shared/convention-utils.md` | `plan-feature/SKILL.md` Step 6a |
| Module | Shared utility (convention formatting) | Plan-feature skill (task creation) |
| Defect type | Wrong string transform | Wrong config field lookup |
| Symptom | Malformed convention references in description | Wrong issue type on created issue |
| Fix scope | Change case transform logic | Change config field reference |

The two defects are in different modules, affect different aspects of the output, and can be fixed independently without any interaction. Fixing one does not affect the other.

This triggers the **Decomposition Guard** (Step 6).
