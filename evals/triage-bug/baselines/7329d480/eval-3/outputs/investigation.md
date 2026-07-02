# Triage Investigation: ACME-502

## Step 0 -- Validate Project Configuration

Configuration validated from project CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration.

## Step 1 -- Fetch Bug

**Issue**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- matches Bug Configuration, validated.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

### Parsed Description Sections

All required sections present per bug template:

- **Issue Description**: Two distinct problems occur when running `/plan-feature`: (1) malformed convention references using wrong case transform, (2) task creation uses Feature issue type instead of Task.
- **Steps to Reproduce**: Configure project with custom issue type scheme (Task ID 10050), add CONVENTIONS.md with `## Migration Patterns`, run `/plan-feature ACME-200`, observe task output.
- **Expected Result**: Convention references as `Migration Patterns` (title case); issue type Task (ID 10050).
- **Actual Result**: Convention references as `migration-patterns` (kebab-case); issue type Feature (ID 10142).
- **Suggested Fix** (optional): Two separate bugs -- convention formatter incorrectly lowercases/kebab-cases, task creation reads Feature issue type ID instead of Task.

## Step 2 -- Reproduce/Trace

This bug affects skill behavior (document generation and Jira issue creation), so code-path tracing is the appropriate approach rather than runnable reproduction.

### Trace 1: Convention reference formatting

Entry point: `/plan-feature` skill invocation generates task descriptions that include Implementation Notes with convention references.

Traced the convention reference pipeline:
1. The skill reads `CONVENTIONS.md` from the target repository.
2. Section headings (e.g., `## Migration Patterns`) are extracted.
3. These headings are passed through a formatter in `shared/convention-utils.md` to produce section references (e.g., `Migration Patterns`).
4. **Divergence found**: The formatter applies a `slugify` / kebab-case transform to the heading text, producing `migration-patterns` instead of preserving the original title-case heading text `Migration Patterns`.

### Trace 2: Task creation issue type

Entry point: `/plan-feature` Step 6a creates a Jira Task issue.

Traced the task creation pipeline:
1. The skill reads Jira Configuration from CLAUDE.md.
2. It needs to create an issue of type Task.
3. **Divergence found**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the `Feature issue type ID` (10142) from Jira Configuration instead of looking up the Task issue type ID. When the project has a custom issue type scheme, this causes the created issue to be of type Feature rather than Task.

## Step 3 -- Codebase Investigation

### Target repository

The bug affects the `sdlc-workflow` component, which corresponds to the plugin code in this repository.

### Affected files and modules

#### Root Cause 1: Convention reference formatter

- **File**: `shared/convention-utils.md`
- **Defect**: The convention reference formatter applies a slugify/kebab-case transform to CONVENTIONS.md section headings when generating section references. It converts `Migration Patterns` to `migration-patterns` instead of preserving the original heading text as-is.
- **Impact**: All convention references in generated task Implementation Notes use kebab-case (`migration-patterns`) instead of the correct title-case format (`Migration Patterns`).

#### Root Cause 2: Task creation issue type

- **File**: `plan-feature/SKILL.md`, Step 6a
- **Defect**: The task creation logic uses the `Feature issue type ID` (10142) from Jira Configuration when creating issues, instead of using the Task issue type ID. This is hardcoded or mis-mapped to the Feature type.
- **Impact**: All tasks created by `/plan-feature` are created as Feature issues instead of Task issues when the project has a custom issue type scheme.

### Independence assessment

These two root causes are **independent**:
- They reside in **different modules**: `shared/convention-utils.md` vs. `plan-feature/SKILL.md` Step 6a.
- They affect **different code paths**: the convention reference formatting pipeline vs. the Jira issue creation pipeline.
- They can be **fixed independently**: fixing the formatter does not affect issue type selection, and vice versa.
- They have **no shared cause**: the formatter bug is a string transform error; the issue type bug is a configuration lookup error.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention reference formatter uses wrong case transform

- **What is broken**: Convention references in generated task descriptions use kebab-case (`migration-patterns`) instead of preserving the original heading case (`Migration Patterns`).
- **Why it is broken**: The formatter in `shared/convention-utils.md` applies a slugify/kebab-case transform to section headings. This transform lowercases the text and replaces spaces with hyphens, which is appropriate for URL slugs but not for human-readable section references.
- **Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference formatting function.
- **How to verify the fix**: A reproducer test should provide a CONVENTIONS.md with a heading like `## Migration Patterns`, run the formatter, and assert the output reference is `Migration Patterns` (not `migration-patterns`).

### Root Cause 2: Task creation uses Feature issue type ID instead of Task

- **What is broken**: Tasks created by `/plan-feature` are created with issue type Feature (ID 10142) instead of Task.
- **Why it is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the `Feature issue type ID` from Jira Configuration instead of the Task issue type ID. This causes all created issues to use the Feature type regardless of the project's issue type scheme.
- **Where it is broken**: `plan-feature/SKILL.md`, Step 6a -- the issue creation call's `issuetype` parameter.
- **How to verify the fix**: A reproducer test should configure a project with Task issue type ID 10050, run `/plan-feature`, and assert the created issue has `issuetype.id` equal to 10050 (not 10142).

### Conclusion

The investigation reveals **two independent root causes** in **different modules** affecting **different code paths**. This triggers the Decomposition Guard (Step 6) -- the user must decide whether to proceed with a single Task or split into separate Bugs.
