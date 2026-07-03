# Triage Investigation: ACME-502

## Step 0 -- Validate Configuration

Configuration validated from project CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142 (from Jira Configuration)

## Step 1 -- Fetch Bug

**Issue**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- matches Bug Configuration (valid)
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

### Parsed Description Sections

**Required Sections** (all present):

- **Description**: Two distinct problems occur when running `/plan-feature`: (1) malformed convention references in Implementation Notes using wrong case transform, (2) task created with wrong issue type.
- **Steps to Reproduce**: Configure project with custom issue type scheme (Task ID 10050), add CONVENTIONS.md with `## Migration Patterns` heading, run `/plan-feature ACME-200`, observe generated task.
- **Expected Result**: Convention references should use title case (`Migration Patterns`); created issue should be type Task (ID 10050).
- **Actual Result**: Convention references use kebab-case (`migration-patterns`); created issue is type Feature (ID 10142).

**Optional Sections**:

- **Suggested Fix**: Present. Reporter suggests two separate bugs: convention reference formatter lowercases/kebab-cases incorrectly, and task creation logic reads Feature issue type ID instead of Task issue type ID.

## Step 2 -- Code-Path Tracing

This bug involves skill behavior (the `/plan-feature` skill), so direct reproduction via runnable commands is not applicable. Code-path tracing was performed instead.

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` skill invocation generates task descriptions with Implementation Notes that reference CONVENTIONS.md section headings.

Traced path:
1. `/plan-feature` reads the target repository's CONVENTIONS.md
2. Section headings are extracted (e.g., `## Migration Patterns`)
3. The convention reference formatter in `shared/convention-utils.md` transforms headings into reference format
4. **Divergence**: The formatter applies a kebab-case transform, producing `migration-patterns` instead of preserving the original title case `Migration Patterns`
5. The resulting reference `migration-patterns` is inserted into Implementation Notes

### Trace 2: Issue Type Selection

Entry point: `/plan-feature` skill invocation creates a Jira Task issue.

Traced path:
1. `/plan-feature` reaches Step 6a (task creation)
2. The task creation logic reads the issue type ID from project configuration
3. **Divergence**: The code reads the **Feature issue type ID** (10142) from Jira Configuration instead of using a Task issue type ID
4. The created issue has issue type Feature (10142) instead of Task

## Step 3 -- Codebase Investigation

### Target Repository

Component `sdlc-workflow` maps to the sdlc-plugins repository (the plugin codebase itself).

No Serena instance is configured for this repository. Investigation used Read/Grep/Glob fallback.

### Finding 1: Convention Reference Formatter (shared/convention-utils.md)

**Affected file**: `shared/convention-utils.md`
**Affected logic**: The convention reference formatter that transforms CONVENTIONS.md section headings into section reference notation (the `section-reference` format).

The formatter applies a kebab-case transform to section headings before producing the reference. For a heading like `## Migration Patterns`, it produces `migration-patterns` instead of preserving the original casing `Migration Patterns`.

**Root behavior**: The formatter lowercases the heading text and replaces spaces with hyphens (kebab-case), which is a standard slug transform. However, convention references should preserve the original heading text as-is to match the CONVENTIONS.md source.

### Finding 2: Task Creation Issue Type (plan-feature/SKILL.md Step 6a)

**Affected file**: `plan-feature/SKILL.md` (Step 6a -- task creation)
**Affected logic**: The issue type ID used when creating Jira issues via `jira.create_issue`.

The task creation step reads the Feature issue type ID (10142) from the project's Jira Configuration section. When a project has a custom issue type scheme where Task has a different ID (e.g., 10050), the created issue is incorrectly typed as Feature.

**Root behavior**: The skill hardcodes or defaults to the Feature issue type ID from Jira Configuration rather than using a Task-specific issue type ID. The Jira Configuration section in CLAUDE.md only defines `Feature issue type ID: 10142` and does not include a separate Task issue type ID field, so the skill falls back to the Feature ID.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Wrong case transform in convention reference formatter

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` produces kebab-case references (e.g., `migration-patterns`) instead of preserving the original title-case heading text (e.g., `Migration Patterns`).
- **Why it is broken**: The formatter applies a slug/kebab-case transformation to section headings. This is incorrect because convention section references should preserve the exact heading text from CONVENTIONS.md so they match when looked up.
- **Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference transform function.
- **How to verify the fix**: A reproducer test should create a CONVENTIONS.md with a title-case section heading (e.g., `## Migration Patterns`), invoke the convention reference formatter, and assert the output preserves the original casing (`Migration Patterns`) rather than producing kebab-case (`migration-patterns`).

### Root Cause 2: Task creation uses Feature issue type ID instead of Task issue type ID

- **What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a creates issues with the Feature issue type ID (10142) instead of the Task issue type ID.
- **Why it is broken**: The Jira Configuration in CLAUDE.md only defines `Feature issue type ID`, and the task creation step reads that value. There is no separate `Task issue type ID` field, so the skill defaults to the Feature type.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `jira.create_issue` call that specifies the issue type.
- **How to verify the fix**: A reproducer test should configure a project with a custom issue type scheme (Task ID = 10050, Feature ID = 10142), run `/plan-feature`, and assert the created issue has issue type Task (10050), not Feature (10142).

### Independence Assessment

These two root causes are **independent**:

- They reside in **different modules**: `shared/convention-utils.md` vs. `plan-feature/SKILL.md`
- They affect **different code paths**: convention reference formatting vs. Jira issue creation
- They can be **fixed independently**: fixing one does not affect the other
- They have **no shared dependencies**: they do not share functions, data structures, or configuration values

This triggers the **Decomposition Guard** (Step 6).
