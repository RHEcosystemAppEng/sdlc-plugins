# Investigation Report: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- validated against Bug Configuration (Bug issue type ID: 10020)
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

## Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

Repository Registry:
| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| acme-backend | Rust backend service | serena_backend | /home/dev/repos/acme-backend |

## Step 1 -- Fetch Bug

Issue type validated: issue type ID 10020 matches Bug Configuration's Bug issue type ID (10020).

### Parsed Bug Description

**Description**: Two distinct problems occur when running `/plan-feature`: (1) the generated task description has malformed Implementation Notes where convention references use the wrong section heading format (e.g., `§migration-patterns` instead of `§Migration Patterns`), and (2) the task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

**Steps to Reproduce**:
1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

**Expected Result**:
- Implementation Notes should reference conventions as `§Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

**Actual Result**:
- Implementation Notes reference conventions as `§migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

**Suggested Fix** (optional, from reporter):
- The convention reference formatter lowercases and kebab-cases headings incorrectly.
- The task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

### Extracted Metadata
- **Issue key**: ACME-502
- **webUrl**: https://mock-jira.example.com/browse/ACME-502
- **Summary**: Skill output is malformed and task creation uses wrong issue type
- **Labels**: reported-by-user
- **Component**: sdlc-workflow

## Step 2 -- Code-Path Tracing

Since this is a skill/documentation bug affecting the sdlc-workflow plugin, direct reproduction is not applicable. Tracing through the relevant code paths instead.

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` skill invocation (Step 5 -- Convention-aware task enrichment).

The plan-feature skill's Step 5 performs convention-aware task enrichment. After drafting each task's Implementation Notes, it cross-references conventions from CONVENTIONS.md and includes references in the format `Per CONVENTIONS.md §<Section Name>: <action required>`.

The convention formatting logic is governed by `shared/convention-applicability-rules.md`, which specifies the prescribed format:

```
Per CONVENTIONS.md §<Section Name>: <action required>.
Applies: task modifies <matching file(s)> matching the convention's <scope signal>.
```

The `<Section Name>` placeholder should preserve the original heading text from CONVENTIONS.md (e.g., `§Migration Patterns`). The bug is that the formatter transforms the heading into kebab-case (`§migration-patterns`) instead of preserving the original title case.

**Affected module**: `shared/convention-applicability-rules.md` (convention-utils / convention reference formatting logic)

### Trace 2: Issue Type Selection During Task Creation

Entry point: `/plan-feature` skill invocation (Step 6a -- Create the tasks).

The plan-feature skill's Step 6a creates tasks using `jira.create_issue`. The issue type used for task creation should be "Task", but the bug report indicates that the created issue is of type "Feature" (ID 10142).

Looking at the CLAUDE.md configuration:
- `Feature issue type ID: 10142` is listed under Jira Configuration.
- There is no explicit `Task issue type ID` field in the Jira Configuration.

The task creation logic in Step 6a reads the issue type from the project configuration. When the project has a custom issue type scheme where Task has ID 10050, the logic incorrectly falls back to the Feature issue type ID (10142) instead of using the correct Task issue type ID.

**Affected module**: `plan-feature/SKILL.md` Step 6a (task creation logic)

## Step 3 -- Codebase Investigation

### Root Cause 1: Convention Reference Formatter (shared/convention-applicability-rules.md)

The convention-applicability-rules document defines how convention section names should be referenced in task Implementation Notes. The prescribed format uses `§<Section Name>` where `<Section Name>` should match the original CONVENTIONS.md heading verbatim.

The defect is in the convention reference formatting pipeline: when the formatter processes a CONVENTIONS.md heading like `## Migration Patterns`, it applies a kebab-case transformation (lowercasing and replacing spaces with hyphens), producing `§migration-patterns` instead of preserving the original `§Migration Patterns`.

**Affected files and symbols**:
- `plugins/sdlc-workflow/shared/convention-applicability-rules.md` -- defines the `§<Section Name>` format but does not explicitly prohibit case transformation
- The convention formatter implementation (wherever the heading-to-reference conversion happens) applies an incorrect slug/kebab-case transformation

**Correct behavior**: The `§<Section Name>` reference must preserve the original heading text exactly as it appears in CONVENTIONS.md, including capitalization and spacing.

### Root Cause 2: Task Creation Issue Type (plan-feature/SKILL.md Step 6a)

The plan-feature skill's Step 6a creates Jira issues but uses the wrong issue type. The CLAUDE.md Jira Configuration section contains `Feature issue type ID: 10142` but does not contain a `Task issue type ID` field. When the task creation logic needs to create a Task, it reads the Feature issue type ID instead because no separate Task issue type ID is configured.

**Affected files and symbols**:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a -- the `jira.create_issue` call that creates tasks
- The project's CLAUDE.md `## Jira Configuration` section -- missing `Task issue type ID` field

**Correct behavior**: The task creation logic should use a dedicated Task issue type ID from configuration (not the Feature issue type ID). The Jira Configuration section should include a `Task issue type ID` field, and Step 6a should reference it when creating Task issues.

## Step 4 -- Root Cause Analysis

### Finding: Two Independent Root Causes

The investigation reveals that the two problems described in ACME-502 are caused by **independent code paths in different modules**:

| # | Problem | Root Cause | Affected Module | Fix Location |
|---|---------|-----------|-----------------|-------------|
| 1 | Malformed convention references (`§migration-patterns` instead of `§Migration Patterns`) | Convention reference formatter applies incorrect kebab-case transformation to CONVENTIONS.md headings | `shared/convention-applicability-rules.md` (convention formatting logic) | Convention formatter / heading-to-reference conversion |
| 2 | Wrong issue type (Feature instead of Task) | Task creation reads Feature issue type ID (10142) from config instead of Task issue type ID | `plan-feature/SKILL.md` Step 6a (task creation logic) | Step 6a issue type selection + CLAUDE.md Jira Configuration |

### Why these are independent

1. **Different modules**: Root cause 1 is in the shared convention formatting utilities (`shared/convention-applicability-rules.md`), while root cause 2 is in the plan-feature skill's task creation logic (`plan-feature/SKILL.md` Step 6a).

2. **Different code paths**: The convention formatting occurs during Step 5 (Generate Jira Tasks -- convention-aware task enrichment), while the issue type selection occurs during Step 6a (Create Tasks in Jira). These are sequential but independent operations.

3. **No shared state**: The convention reference format and the issue type selection do not share any common variables, configuration fields, or logic paths. Fixing one has no effect on the other.

4. **Independent reproducibility**: Each problem can be reproduced independently -- a project without CONVENTIONS.md would still exhibit the wrong issue type bug, and a project with the correct Task issue type configured would still exhibit the malformed convention references.

### Root Cause Comment (would be posted to ACME-502)

**Root Cause**: Two independent defects in the `/plan-feature` skill produce the observed symptoms:

1. **Convention reference formatter** (`shared/convention-applicability-rules.md`): The formatter applies a kebab-case transformation to CONVENTIONS.md section headings when generating `§<Section Name>` references, producing `§migration-patterns` instead of preserving the original heading `§Migration Patterns`.

2. **Task creation issue type** (`plan-feature/SKILL.md` Step 6a): The task creation logic reads the `Feature issue type ID` (10142) from Jira Configuration instead of a dedicated `Task issue type ID`, causing created tasks to have issue type "Feature" instead of "Task".

**Affected Files**:
- `plugins/sdlc-workflow/shared/convention-applicability-rules.md` -- convention reference formatting
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Step 6a task creation

**Suggested Approach**:
1. Fix the convention formatter to preserve original heading text (no case transformation).
2. Add `Task issue type ID` to the Jira Configuration contract and update Step 6a to use it.

**Reproducer Strategy**:
1. For convention formatting: create a CONVENTIONS.md with a titled section, run `/plan-feature`, verify the `§` reference preserves the original heading case.
2. For issue type: configure a project with a custom Task issue type ID, run `/plan-feature`, verify the created issue uses the Task type ID (not Feature).
