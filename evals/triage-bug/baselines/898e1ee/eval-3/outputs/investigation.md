# Investigation Report: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

## Step 0 -- Validate Configuration

Configuration validated from project CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

## Step 1 -- Fetch and Parse Bug

Issue type verified: issue type ID 10020 matches Bug Configuration's Bug issue type ID 10020.

### Parsed Sections

All required sections are present per the bug template:

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Attachments | Present (None) |

Optional sections present:
- **Suggested Fix**: Present -- reporter suggests these are two separate bugs.

### Extracted Metadata

- **Labels**: reported-by-user
- **Component**: sdlc-workflow

## Step 2 -- Code-Path Tracing

The bug cannot be directly reproduced in this environment (it involves running `/plan-feature` against a configured project). Tracing was performed instead.

### Trace 1: Convention reference formatting

The Steps to Reproduce specify adding a `CONVENTIONS.md` with section `## Migration Patterns` and then observing that Implementation Notes convention references render as `migration-patterns` (kebab-case) instead of `Migration Patterns` (title case, matching the heading).

**Entry point**: `/plan-feature` generates task descriptions with Implementation Notes that include convention references using the `section-ref` syntax (e.g., `Migration Patterns`).

**Traced to**: `shared/convention-utils.md` -- the convention reference formatter. This module is responsible for transforming CONVENTIONS.md section headings into the reference format used in task Implementation Notes. The formatter applies a kebab-case transform (lowercasing and replacing spaces with hyphens) to headings, producing `migration-patterns` instead of preserving the original title case `Migration Patterns`.

### Trace 2: Task issue type selection

The Steps to Reproduce specify configuring a project with a custom issue type scheme where Task has ID 10050. The Actual Result shows that the created issue uses the Feature issue type (ID 10142) instead of Task (ID 10050).

**Entry point**: `/plan-feature` Step 6a -- task creation logic.

**Traced to**: `plan-feature/SKILL.md` Step 6a -- the task creation step reads the `Feature issue type ID` (10142) from Jira Configuration and uses it as the issue type for created tasks, rather than reading a separate Task issue type ID. In projects with custom issue type schemes, this results in tasks being created as Feature type instead of Task type.

## Step 3 -- Codebase Investigation

### Affected Files and Modules

| Root Cause | Affected Module | Affected File |
|------------|----------------|---------------|
| Convention reference kebab-casing | Shared utilities | `shared/convention-utils.md` |
| Wrong issue type for task creation | Plan-feature skill | `plan-feature/SKILL.md` (Step 6a) |

### Key Finding: Independent Code Paths

These two issues reside in **different modules** with **independent code paths**:

1. **`shared/convention-utils.md`** handles convention reference formatting. This module is used by any skill that generates Implementation Notes referencing CONVENTIONS.md sections. The bug is in the heading-to-reference transform function, which incorrectly applies kebab-case instead of preserving original casing.

2. **`plan-feature/SKILL.md` Step 6a** handles task creation in Jira. The bug is in the issue type selection logic, which uses the Feature issue type ID from Jira Configuration rather than a Task issue type ID. This is a configuration reading error in the plan-feature skill's task creation step.

These are **not** two manifestations of a single defect. They are independent bugs that happen to be observed together when running `/plan-feature`.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention reference formatter uses wrong case transform

- **What is broken**: Convention references in generated task Implementation Notes use kebab-case (`migration-patterns`) instead of preserving the original heading case (`Migration Patterns`).
- **Why it is broken**: The convention reference formatter in `shared/convention-utils.md` applies a `toKebabCase()` transform to CONVENTIONS.md section headings when generating section references. It should preserve the original title case of the heading.
- **Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference transformation logic.
- **How to verify the fix**: A reproducer test should:
  1. Provide a CONVENTIONS.md with a section heading `## Migration Patterns`
  2. Run the convention reference formatter
  3. Assert the output reference is `Migration Patterns` (title case preserved), not `migration-patterns` (kebab-case)

### Root Cause 2: Task creation uses Feature issue type ID instead of Task issue type ID

- **What is broken**: Tasks created by `/plan-feature` use the Feature issue type (ID 10142) instead of the Task issue type (ID 10050).
- **Why it is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads `Feature issue type ID` (10142) from Jira Configuration and passes it as the issue type when creating task issues. It should use a Task issue type ID instead.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `create_issue` call's issue type parameter.
- **How to verify the fix**: A reproducer test should:
  1. Configure a project with Task issue type ID 10050 and Feature issue type ID 10142
  2. Run task creation through `/plan-feature`
  3. Assert the created issue's type ID is 10050 (Task), not 10142 (Feature)

## Decomposition Determination

**Trigger: YES -- multiple independent root causes detected.**

The two root causes are in different modules (`shared/convention-utils.md` vs `plan-feature/SKILL.md`) and affect different code paths (convention formatting vs Jira issue creation). A single Task bundling both fixes would violate the principle that each task should address a single, coherent defect. The Decomposition Guard (Step 6) must be triggered.
