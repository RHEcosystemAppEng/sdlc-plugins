# Triage Investigation: ACME-502

## Bug Summary

- **Issue**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
- **Summary**: Skill output is malformed and task creation uses wrong issue type
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow

## Step 0 -- Configuration Validation

Configuration extracted from project CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Feature issue type ID**: 10142
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration) are present. Configuration is valid.

## Step 1 -- Fetch and Parse Bug

### Issue type validation

Issue type ID 10020 matches the Bug issue type ID from Bug Configuration. Validated.

### Parsed description sections

**Required sections** (all present):

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |

**Optional sections**:

| Section | Status |
|---------|--------|
| Root Cause | Not present |
| Suggested Fix | Present |

### Extracted content

**Issue Description**: Two distinct problems occur when running `/plan-feature`: (1) generated task descriptions have malformed Implementation Notes where convention references use kebab-case instead of preserving original heading case, and (2) tasks are created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

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

**Suggested Fix**: The reporter suggests these are likely two separate bugs -- the convention reference formatter lowercases and kebab-cases headings incorrectly, and the task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

## Step 2 -- Code-Path Tracing

These are skill/documentation bugs that cannot be directly reproduced via CLI. Code-path tracing was performed instead.

### Trace 1: Convention reference formatting

- **Entry point**: `/plan-feature` skill invocation
- **Code path**: When generating Implementation Notes, the skill calls the convention reference formatter in `shared/convention-utils.md` to produce section references (e.g., `Migration Patterns`).
- **Divergence point**: The formatter in `shared/convention-utils.md` applies a kebab-case transform to heading text before emitting the reference. For the heading `## Migration Patterns`, it produces `migration-patterns` instead of preserving the original heading text `Migration Patterns`.
- **Trace outcome**: Confirmed -- the convention reference formatter uses a wrong case transform function that lowercases and hyphenates heading text.

### Trace 2: Task creation issue type

- **Entry point**: `/plan-feature` skill invocation
- **Code path**: After generating the task description, the skill creates the Jira issue in `plan-feature/SKILL.md` Step 6a. The issue type is determined by reading the project configuration.
- **Divergence point**: Step 6a reads the **Feature issue type ID** (10142) from Jira Configuration instead of the **Task issue type ID** (10050). When the project has a custom issue type scheme with a distinct Task type, the wrong type is used.
- **Trace outcome**: Confirmed -- the task creation logic references the wrong configuration field for the issue type.

## Step 3 -- Codebase Investigation

### Affected files and modules

| # | File/Module | Symbol/Location | Problem |
|---|-------------|----------------|---------|
| 1 | `shared/convention-utils.md` | Convention reference formatter (case transform logic) | Applies kebab-case transform to CONVENTIONS.md headings instead of preserving original heading case |
| 2 | `plan-feature/SKILL.md` | Step 6a (task creation) | Uses Feature issue type ID (10142) from Jira Configuration instead of Task issue type ID (10050) |

### Key observations

- The two affected files are in **different modules** (`shared/` vs `plan-feature/`).
- The two defects operate on **independent code paths** -- one is in the convention formatting pipeline, the other is in the issue creation pipeline.
- There is no shared root cause or common code path linking the two problems.
- A fix to one defect would have zero impact on the other.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention reference formatter uses wrong case transform

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` transforms CONVENTIONS.md section headings to kebab-case when producing section references for Implementation Notes.
- **Why it is broken**: The formatter applies a `toLowerCase()` + hyphenation transform to heading text, converting `Migration Patterns` to `migration-patterns`. It should preserve the original heading text as-is.
- **Where it is broken**: `shared/convention-utils.md` -- the case transform logic in the convention reference formatter.
- **How to verify the fix**: A reproducer test should create a CONVENTIONS.md with a heading like `## Migration Patterns`, invoke the convention reference formatter, and assert that the output reference preserves the original heading case (`Migration Patterns`) rather than producing kebab-case (`migration-patterns`).

### Root Cause 2: Task creation uses wrong issue type ID

- **What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a creates issues with the Feature issue type ID (10142) instead of the Task issue type ID.
- **Why it is broken**: Step 6a reads `Feature issue type ID` from Jira Configuration rather than `Task issue type ID`. In projects with custom issue type schemes where Task has a distinct ID (e.g., 10050), the created issue has the wrong type.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the issue type field reference in the `jira.create_issue` call.
- **How to verify the fix**: A reproducer test should configure a project with `Task issue type ID: 10050` in its Jira Configuration, invoke the task creation logic, and assert that the created issue has issue type ID 10050 (Task), not 10142 (Feature).

### Independence assessment

These two root causes are **independent**:

- They affect **different modules** (`shared/convention-utils.md` vs `plan-feature/SKILL.md`).
- They operate on **different code paths** (convention formatting vs issue creation).
- Fixing one has **no effect** on the other.
- They could be introduced and resolved at different times without conflict.

This triggers the **Decomposition Guard** (Step 6) -- see `outputs/decomposition-guard.md`.
