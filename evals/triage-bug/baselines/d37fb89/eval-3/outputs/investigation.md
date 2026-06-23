# Investigation: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

## Step 0 -- Configuration Validation

Project configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections present (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration).

## Step 1 -- Bug Parsing

Issue type confirmed: Bug (ID 10020) matches Bug Configuration.

### Parsed Sections

**Description**: Two distinct problems occur when running `/plan-feature`: (1) malformed Implementation Notes with wrong convention reference format, and (2) task creation using wrong issue type.

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

**Suggested Fix** (optional section, present):
- The convention reference formatter lowercases and kebab-cases headings incorrectly.
- The task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

All required sections present. No missing sections.

## Step 2 -- Code-Path Tracing

This bug involves skill behavior (not runnable commands), so code-path tracing was performed rather than direct reproduction.

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` generates Implementation Notes that reference CONVENTIONS.md sections.

The convention reference formatter in `shared/convention-utils.md` is responsible for transforming CONVENTIONS.md section headings into reference format. The formatter applies a kebab-case transform (lowercasing and hyphenating spaces) to produce references like `migration-patterns`. The correct behavior is to preserve the original title case from the heading, producing `Migration Patterns`.

The defect is in the case transform logic of the convention reference formatter -- it applies `kebab-case` when it should preserve the original heading text as-is (title case).

### Trace 2: Task Creation Issue Type

Entry point: `/plan-feature` Step 6a creates a Jira issue for each planned task.

The task creation logic in `plan-feature/SKILL.md` Step 6a reads the issue type ID from Jira Configuration. It reads the `Feature issue type ID` field (value: 10142) instead of a `Task issue type ID` field. When the project has a custom issue type scheme with a separate Task issue type (ID 10050), the created issue is incorrectly typed as Feature.

The defect is in the issue type ID lookup -- it references the wrong configuration field.

## Step 3 -- Codebase Investigation

### Affected Repository

Target repository: sdlc-plugins (sdlc-workflow component), based on the Component field.

No Serena instance configured; investigation used Read/Grep/Glob fallback.

### Root Cause Location 1: Convention Reference Formatter

**File**: `shared/convention-utils.md`
**Defect**: The convention reference formatter applies a kebab-case transform to CONVENTIONS.md section headings when generating section references (e.g., `migration-patterns` instead of `Migration Patterns`). The transform lowercases the heading text and replaces spaces with hyphens, but the correct behavior is to preserve the original heading text verbatim.

### Root Cause Location 2: Task Creation Issue Type

**File**: `plan-feature/SKILL.md` (Step 6a)
**Defect**: The task creation logic reads `Feature issue type ID` (10142) from the Jira Configuration section of CLAUDE.md. It should instead read a `Task issue type ID` field, or use the correct issue type ID for Task (10050) when creating Task issues. This causes all tasks to be created as Feature issues instead of Task issues.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Wrong Case Transform in Convention Reference Formatter

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` produces kebab-case references (`migration-patterns`) instead of preserving the original heading text (`Migration Patterns`).
- **Why it is broken**: The formatter applies a `toLowerCase()` + hyphenation transform to section headings. This transform is appropriate for URL slugs or CSS class names but incorrect for human-readable convention references in Implementation Notes.
- **Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference conversion logic.
- **How to verify**: A reproducer test should create a CONVENTIONS.md with a multi-word title-cased section heading (e.g., `## Migration Patterns`), run the convention reference formatter, and assert the output is `Migration Patterns` (not `migration-patterns`).

### Root Cause 2: Wrong Issue Type ID in Task Creation

- **What is broken**: Tasks created by `/plan-feature` use the Feature issue type (ID 10142) instead of the Task issue type (ID 10050).
- **Why it is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the `Feature issue type ID` from Jira Configuration. There is no separate `Task issue type ID` field in the configuration, or the logic does not distinguish between Feature and Task issue types.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the issue type ID selection during `jira.create_issue`.
- **How to verify**: A reproducer test should configure a project with a custom issue type scheme (Task ID: 10050, Feature ID: 10142), run `/plan-feature`, and assert the created issue has `issuetype.id` equal to `10050` (not `10142`).

### Independence Assessment

These two root causes are **independent**:

- They are in **different modules**: `shared/convention-utils.md` vs. `plan-feature/SKILL.md`.
- They affect **different code paths**: the convention formatting pipeline vs. the Jira issue creation pipeline.
- They can be **fixed independently**: fixing the case transform does not affect issue type selection, and vice versa.
- They produce **different symptoms**: malformed text output vs. wrong Jira issue type.

This triggers the **Decomposition Guard** (Step 6) -- the skill must not silently create a single Task bundling unrelated fixes.
