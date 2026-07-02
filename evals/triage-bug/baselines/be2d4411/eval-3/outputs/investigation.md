# Triage Investigation: ACME-502

## Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142 (from Jira Configuration)

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration.

## Step 1 -- Fetch Bug

**Issue**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- matches Bug issue type ID from Bug Configuration. Valid.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

### Description parsing (against bug template)

**Required Sections** (all present):

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |

**Optional Sections**:

| Section | Status |
|---------|--------|
| Root Cause | Not present |
| Suggested Fix | Present |

### Parsed content

**Issue Description**: Two distinct problems occur when running `/plan-feature`:
1. The generated task description has malformed Implementation Notes -- convention references use the wrong section heading format (e.g., `section-migration-patterns` instead of `section-Migration Patterns`).
2. The task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

**Steps to Reproduce**:
1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

**Expected Result**:
- Implementation Notes should reference conventions as `section-Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

**Actual Result**:
- Implementation Notes reference conventions as `section-migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

**Suggested Fix** (from reporter):
These are likely two separate bugs:
- The convention reference formatter lowercases and kebab-cases headings incorrectly.
- The task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

## Step 2 -- Reproduce/Trace

The bug references a `/plan-feature` skill invocation, which is a documentation/skill-level behavior rather than a runnable command. Code-path tracing was performed instead of direct reproduction.

### Trace 1: Convention reference formatting

- **Entry point**: `/plan-feature` skill invocation
- **Code path**: When plan-feature generates task descriptions with Implementation Notes, it calls a convention reference formatter to produce section references (e.g., `section-Migration Patterns`).
- **Divergence point**: The formatter in `shared/convention-utils.md` applies a `lowercase + kebab-case` transform to CONVENTIONS.md section headings before emitting references. This produces `section-migration-patterns` instead of preserving the original heading case `section-Migration Patterns`.

### Trace 2: Issue type selection during task creation

- **Entry point**: `/plan-feature` skill invocation, Step 6a (task creation)
- **Code path**: When plan-feature creates a Jira issue for each task, it selects an issue type ID from the project configuration.
- **Divergence point**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the **Feature issue type ID** (10142) from Jira Configuration instead of reading the **Task issue type ID** from the project's issue type scheme. This causes all created issues to be of type "Feature" instead of "Task".

## Step 3 -- Codebase Investigation

### Target repository

Based on the Component field (`sdlc-workflow`) and the code paths described, the bug affects the sdlc-plugins repository itself (specifically the plan-feature skill and shared utilities).

### Investigation findings

#### Root Cause 1: Convention reference formatter (shared/convention-utils.md)

- **File**: `shared/convention-utils.md`
- **Defect**: The convention reference formatter applies a `lowercase + kebab-case` transform to CONVENTIONS.md section headings when generating `section-<heading>` references for task Implementation Notes.
- **Behavior**: Input heading `## Migration Patterns` is transformed to `section-migration-patterns` instead of preserving the original case as `section-Migration Patterns`.
- **Impact**: All convention references in generated task descriptions are malformed, causing implementers to see incorrect references that do not match the actual CONVENTIONS.md headings.

#### Root Cause 2: Task creation issue type (plan-feature/SKILL.md Step 6a)

- **File**: `plan-feature/SKILL.md`, Step 6a
- **Defect**: The task creation logic uses `Feature issue type ID` (10142) from Jira Configuration instead of using the Task issue type ID.
- **Behavior**: When creating Jira issues for planned tasks, the skill sets `issuetype.id` to 10142 (Feature) instead of the correct Task issue type ID.
- **Impact**: All tasks created by plan-feature are created as Feature issues rather than Task issues, which breaks issue type schemes and workflow automation.

### Independence assessment

These two root causes are **independent**:

- **Different modules**: Root cause 1 is in `shared/convention-utils.md` (a shared utility), while root cause 2 is in `plan-feature/SKILL.md` (a skill-specific step).
- **Different code paths**: Root cause 1 involves the convention reference formatting pipeline, while root cause 2 involves the Jira issue creation pipeline.
- **No shared dependency**: Fixing one does not affect the other. Each can be fixed, tested, and verified independently.
- **Different test strategies**: Root cause 1 requires testing convention reference output formatting; root cause 2 requires testing Jira issue creation parameters.

## Step 4 -- Root Cause Analysis

### Root Cause Summary

ACME-502 describes two distinct defects that manifest together when running `/plan-feature` but originate from independent code paths:

**Root Cause 1 -- Convention reference case transform**:
- **What is broken**: The convention reference formatter produces kebab-cased, lowercased section references instead of preserving the original heading case from CONVENTIONS.md.
- **Why it is broken**: `shared/convention-utils.md` applies a `toLowerCase() + kebab-case` transform to section headings before emitting `section-<heading>` references. This transform is incorrect -- convention references should preserve the original heading text exactly as written in CONVENTIONS.md.
- **Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference conversion logic.
- **How to verify**: A reproducer test should assert that a CONVENTIONS.md heading `## Migration Patterns` produces the reference `section-Migration Patterns`, not `section-migration-patterns`.

**Root Cause 2 -- Wrong issue type ID in task creation**:
- **What is broken**: Tasks created by plan-feature use the Feature issue type ID (10142) instead of the Task issue type ID.
- **Why it is broken**: `plan-feature/SKILL.md` Step 6a hardcodes or reads the `Feature issue type ID` from Jira Configuration instead of using the correct Task issue type ID from the project's issue type scheme or configuration.
- **Where it is broken**: `plan-feature/SKILL.md`, Step 6a -- the `jira.create_issue` call's issue type parameter.
- **How to verify**: A reproducer test should assert that the `issuetype.id` field in the `create_issue` call matches the Task issue type ID (e.g., 10050), not the Feature issue type ID (10142).

### Root Cause Comment (would be posted to ACME-502)

The following root cause analysis would be posted as an ADF comment on ACME-502:

---

**Root Cause**: This bug has two independent root causes in different modules:

1. **Convention reference formatter** (`shared/convention-utils.md`): The heading-to-reference conversion applies `toLowerCase() + kebab-case`, producing `section-migration-patterns` instead of preserving the original case `section-Migration Patterns`. The transform should pass through the heading text verbatim.

2. **Task creation issue type** (`plan-feature/SKILL.md` Step 6a): The `jira.create_issue` call uses the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID. This causes all plan-feature tasks to be created as Feature issues.

**Affected Files**:
- `shared/convention-utils.md` -- convention heading-to-reference transform
- `plan-feature/SKILL.md` Step 6a -- issue type parameter in `jira.create_issue`

**Suggested Approach**:
1. Fix the convention reference formatter to preserve original heading case instead of applying kebab-case transform.
2. Fix the task creation logic to use the Task issue type ID instead of the Feature issue type ID.

**Reproducer Strategy**:
- Root cause 1: Test that convention references preserve original heading case from CONVENTIONS.md.
- Root cause 2: Test that created issues use the correct Task issue type ID, not Feature.

---
*This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/mrizzi/sdlc-plugins) v0.11.1.*

## Step 6 -- Decomposition Guard Triggered

Because the investigation identified **two independent root causes** in **different modules** (`shared/convention-utils.md` and `plan-feature/SKILL.md`), the Decomposition Guard (Step 6) is triggered. The skill must NOT silently create a single Task. Instead, it must present the user with a choice. See `outputs/decomposition-guard.md` for the decomposition guard prompt.
