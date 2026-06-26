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
**Issue Type**: Bug (ID: 10020) -- matches Bug issue type ID in Bug Configuration. Validated.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

### Parsed Description Sections

**Required Sections** (all present):

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Attachments | Present (None) |

**Optional Sections:**

| Section | Status |
|---------|--------|
| Root Cause | Not provided |
| Suggested Fix | Present |

### Extracted Content

**Description**: Two distinct problems occur when running `/plan-feature`: (1) generated task description has malformed Implementation Notes where convention references use the wrong section heading format (e.g., `migration-patterns` instead of `Migration Patterns`); (2) the task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

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

**Suggested Fix**: These are likely two separate bugs: the convention reference formatter lowercases and kebab-cases headings incorrectly; the task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

## Step 2 -- Reproduce/Trace

This bug involves skill/documentation logic and cannot be directly reproduced via CLI commands. Code-path tracing was performed instead.

### Trace 1: Convention reference formatting

Entry point: `/plan-feature` skill invocation, specifically the Implementation Notes generation phase where CONVENTIONS.md headings are referenced.

The convention reference formatter in `shared/convention-utils.md` is responsible for transforming CONVENTIONS.md section headings into reference format. The formatter applies a `lowercase + kebab-case` transform to headings before emitting them as references (e.g., `## Migration Patterns` becomes `migration-patterns`). This is incorrect -- the reference should preserve the original title case of the heading as written in CONVENTIONS.md.

The divergence point: the formatter function applies string normalization (lowercasing and replacing spaces with hyphens) when it should pass through the heading text verbatim.

### Trace 2: Issue type selection during task creation

Entry point: `/plan-feature` skill invocation, Step 6a (Create Tasks in Jira).

The task creation logic in `plan-feature/SKILL.md` Step 6a calls `jira.create_issue` to create task issues. When determining the issue type ID to use, the logic references the **Feature issue type ID** (10142) from CLAUDE.md Jira Configuration instead of a dedicated **Task issue type ID**. In projects with custom issue type schemes where Task has a different ID (e.g., 10050), this results in tasks being created with the wrong issue type (Feature instead of Task).

The divergence point: Step 6a uses `Feature issue type ID` (10142) from CLAUDE.md but should use the Task issue type ID (10050) specific to the project's issue type scheme.

## Step 3 -- Codebase Investigation

### Target repository

The bug affects the `sdlc-workflow` component, which corresponds to the sdlc-plugins repository itself (path: `./`).

No Serena instance is configured for this repository. Investigation used Read, Grep, and Glob tools directly.

### Findings

#### Root Cause 1: Convention reference formatter (shared/convention-utils.md)

- **Affected file**: `shared/convention-utils.md` (within the sdlc-workflow plugin)
- **Defect**: The convention reference formatter applies a `lowercase + kebab-case` transformation to CONVENTIONS.md section headings when generating references for Implementation Notes. For example, `## Migration Patterns` is transformed to `migration-patterns` and emitted as `migration-patterns`.
- **Correct behavior**: The formatter should preserve the original title case of the heading, emitting `Migration Patterns` as the reference text.
- **Impact**: All convention references in generated task Implementation Notes are malformed, making them unrecognizable to implementers who look for the matching heading in CONVENTIONS.md.

#### Root Cause 2: Task creation issue type (plan-feature/SKILL.md Step 6a)

- **Affected file**: `plan-feature/SKILL.md`, Step 6a (Create the tasks)
- **Defect**: The task creation logic uses the `Feature issue type ID` (10142) from CLAUDE.md Jira Configuration when calling `jira.create_issue`. It does not use a project-specific Task issue type ID.
- **Correct behavior**: The logic should use the Task issue type ID (10050 in the reproducer scenario) rather than the Feature issue type ID. The project configuration should include a Task issue type ID, or the creation logic should resolve the correct type.
- **Impact**: All tasks created by `/plan-feature` in projects with custom issue type schemes are created as Features instead of Tasks, breaking workflow expectations and Jira board configurations.

### CONVENTIONS.md lookup

No CONVENTIONS.md file found at the repository root for sdlc-plugins. Not applicable to the fix task generation.

### Existing test patterns

No existing test files were identified for the convention formatter or the plan-feature task creation logic within the sdlc-plugins repository. The reproducer tests would be new additions.

## Step 4 -- Root Cause Analysis

### Summary

ACME-502 reports two symptoms that stem from **two independent root causes** in **different modules**:

| # | Root Cause | Affected File/Module | Code Path |
|---|-----------|---------------------|-----------|
| 1 | Convention reference formatter applies incorrect case transform (lowercase + kebab-case) instead of preserving title case | `shared/convention-utils.md` | Implementation Notes generation during plan-feature |
| 2 | Task creation uses Feature issue type ID (10142) instead of Task issue type ID (10050) | `plan-feature/SKILL.md` Step 6a | Jira issue creation during plan-feature |

### Root Cause 1: Convention reference formatter

**What is broken**: The convention reference formatter in `shared/convention-utils.md` lowercases and kebab-cases CONVENTIONS.md section headings when producing references for task Implementation Notes.

**Why it is broken**: The formatter applies a string normalization transform (lowercase, replace spaces with hyphens) that is appropriate for URL slugs or file paths but incorrect for human-readable convention references. The reference should preserve the heading's original title case so implementers can locate the matching section in CONVENTIONS.md.

**Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference transformation logic.

**How to verify the fix**: A reproducer test should:
1. Provide a CONVENTIONS.md with a section heading `## Migration Patterns`.
2. Invoke the convention reference formatter.
3. Assert the output reference is `Migration Patterns` (title case preserved), not `migration-patterns` (kebab-case).

### Root Cause 2: Task creation issue type

**What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a creates issues using the Feature issue type ID (10142) from CLAUDE.md Jira Configuration instead of a Task-specific issue type ID.

**Why it is broken**: The CLAUDE.md Jira Configuration section only defines `Feature issue type ID` (10142). Step 6a reads this value when creating tasks, but tasks require a different issue type ID (10050 in the project's custom scheme). There is no `Task issue type ID` configured, so the logic defaults to the only available ID.

**Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `jira.create_issue` call that selects the issue type.

**How to verify the fix**: A reproducer test should:
1. Configure a project with `Feature issue type ID: 10142` and `Task issue type ID: 10050`.
2. Run the task creation logic.
3. Assert the created issue's `issuetype.id` is `10050` (Task), not `10142` (Feature).

### Independence assessment

These two root causes are **independent**:
- They affect **different modules** (`shared/convention-utils.md` vs `plan-feature/SKILL.md`).
- They involve **different code paths** (heading formatting vs Jira issue creation).
- Fixing one does not fix or affect the other.
- They could each be reproduced in isolation.

This triggers the **Decomposition Guard** (Step 6).

### Root cause comment (would be posted to ACME-502)

The following comment would be posted to the Bug issue ACME-502 via `jira.add_comment`:

---

**Root Cause**: Two independent defects contribute to this bug:

1. **Convention reference formatter** (`shared/convention-utils.md`): The heading-to-reference transform lowercases and kebab-cases section headings (e.g., `## Migration Patterns` becomes `migration-patterns`) instead of preserving title case. This causes malformed convention references in Implementation Notes.

2. **Task creation issue type** (`plan-feature/SKILL.md` Step 6a): The `jira.create_issue` call uses the `Feature issue type ID` (10142) from CLAUDE.md Jira Configuration instead of a Task-specific issue type ID. In projects with custom issue type schemes, tasks are created as Features.

**Affected Files**:
- `shared/convention-utils.md` -- convention heading reference formatter
- `plan-feature/SKILL.md` Step 6a -- Jira issue creation logic

**Suggested Approach**:
1. Fix the convention formatter to preserve original heading case when generating references.
2. Add a `Task issue type ID` field to CLAUDE.md Jira Configuration and update Step 6a to use it.

**Reproducer Strategy**:
- Test 1: Verify convention references preserve title case (`Migration Patterns`, not `migration-patterns`).
- Test 2: Verify created tasks use the Task issue type ID, not the Feature issue type ID.

---
This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/mrizzi/sdlc-plugins) v0.11.0.
