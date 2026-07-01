# Investigation Findings — ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Component**: sdlc-workflow

## Step 0 — Configuration Validation

Project configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

Issue type confirmed: issue type ID 10020 matches Bug Configuration's Bug issue type ID. Proceeding.

## Step 1 — Fetch Bug / Parse Description

All required sections present per bug template:

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Attachments | Present (None) |

Optional sections:

| Section | Status |
|---------|--------|
| Root Cause | Not present |
| Suggested Fix | Present |

### Parsed Sections

**Steps to Reproduce**:
1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

**Expected Result**:
- Implementation Notes should reference conventions as `Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

**Actual Result**:
- Implementation Notes reference conventions as `migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

**Suggested Fix** (from reporter):
- The convention reference formatter lowercases and kebab-cases headings incorrectly.
- The task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

### Metadata

- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Web URL**: https://mock-jira.example.com/browse/ACME-502

## Step 2 — Reproduce/Trace

This is a skill/documentation bug that cannot be directly reproduced via CLI commands. Code-path tracing was performed instead.

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` invocation generates task descriptions with Implementation Notes that reference CONVENTIONS.md sections.

Traced the convention reference formatting logic to `shared/convention-utils.md`. This module provides utility functions for formatting section references from CONVENTIONS.md headings. The formatter applies a kebab-case transform (lowercase + hyphen-separated) to section headings before emitting them as references.

**Divergence found**: The formatter converts headings like `## Migration Patterns` into `migration-patterns` (kebab-case slug), but the expected output format is the original title-case heading text (e.g., `Migration Patterns`). The case transform is inappropriate for user-facing convention references in Implementation Notes.

### Trace 2: Task Issue Type Selection

Entry point: `/plan-feature` invocation creates a Jira issue at the end of its workflow.

Traced the task creation logic to `plan-feature/SKILL.md` Step 6a, which specifies the issue type to use when creating the task. The logic reads the Feature issue type ID (10142) from the Jira Configuration section of CLAUDE.md rather than reading a Task issue type ID.

**Divergence found**: When the project has a custom issue type scheme, the created issue uses issue type ID 10142 (Feature) instead of the correct Task issue type ID (10050 in the reproducer's configuration). The task creation step does not look up or use a Task-specific issue type ID.

## Step 3 — Codebase Investigation

### Target Repository

Based on the Component field (sdlc-workflow), the bug affects the sdlc-plugins repository itself (the plugin codebase).

No Serena instance is configured for this repository. Investigation used Read/Grep/Glob fallback.

### Affected Files and Symbols

**Root Cause 1 — Convention reference formatter**:
- **File**: `shared/convention-utils.md`
- **Defect**: The heading-to-reference transform function applies kebab-case conversion (lowercase + hyphenate) to CONVENTIONS.md section headings. It should preserve the original heading text as-is for use in Implementation Notes references.
- **Impact**: All generated task descriptions that reference CONVENTIONS.md sections produce malformed references (e.g., `migration-patterns` instead of `Migration Patterns`).

**Root Cause 2 — Task creation issue type**:
- **File**: `plan-feature/SKILL.md`, Step 6a
- **Defect**: The task creation logic uses the Feature issue type ID from `## Jira Configuration` (field: `Feature issue type ID`) instead of a Task issue type ID. There is no Task issue type ID configured in the Jira Configuration section, and the logic defaults to the Feature ID.
- **Impact**: All tasks created by `/plan-feature` in projects with custom issue type schemes are created as Feature issues instead of Task issues.

### Independence Assessment

These two defects are in **different modules** (`shared/convention-utils.md` vs `plan-feature/SKILL.md`) and affect **different code paths** (convention formatting vs issue creation). They share no common logic, data flow, or dependencies. Fixing one has no effect on the other.

## Step 4 — Root Cause Analysis

### Root Cause 1: Wrong case transform in convention reference formatter

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` converts CONVENTIONS.md section headings to kebab-case slugs instead of preserving the original title-case heading text.
- **Why it is broken**: The formatter applies `toLowerCase()` and hyphenation to heading text, which is appropriate for URL slugs/anchors but not for human-readable section references in Implementation Notes.
- **Where it is broken**: `shared/convention-utils.md` — the heading-to-reference formatting function.
- **How to verify the fix**: A reproducer test should create a CONVENTIONS.md with a section `## Migration Patterns`, invoke the convention reference formatter, and assert the output is `Migration Patterns` (not `migration-patterns`).

### Root Cause 2: Task creation uses Feature issue type ID instead of Task

- **What is broken**: The task creation step in `plan-feature/SKILL.md` Step 6a uses the Feature issue type ID (10142) from Jira Configuration when creating tasks.
- **Why it is broken**: The step reads `Feature issue type ID` from the configuration instead of a Task-specific issue type ID. There is no separate Task issue type ID in the Jira Configuration, so the logic falls back to the only available ID (Feature).
- **Where it is broken**: `plan-feature/SKILL.md`, Step 6a — the issue type parameter in the `jira.create_issue` call.
- **How to verify the fix**: A reproducer test should configure a project with a custom issue type scheme (Task ID = 10050, Feature ID = 10142), run `/plan-feature`, and assert the created issue has issue type ID 10050 (Task), not 10142 (Feature).

## Conclusion

ACME-502 contains **two independent root causes** in **different modules**. These are not a single defect manifesting in multiple ways — they are distinct bugs with distinct code paths and distinct fixes. Per the triage-bug Decomposition Guard (Step 6), this triggers the multi-root-cause decomposition prompt rather than creating a single bundled Task.
