# Triage Investigation: ACME-502

## Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration.

## Step 1 -- Fetch Bug

**Issue key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue type**: Bug (ID: 10020) -- matches Bug issue type ID from Bug Configuration (10020). Validated.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

### Parsed Description Sections

**Required Sections** (all present):

- **Issue Description**: Two distinct problems occur when running `/plan-feature`: (1) malformed convention references in Implementation Notes using kebab-case instead of title case, and (2) task created with wrong issue type "Feature" instead of "Task".
- **Steps to Reproduce**: Configure a project with custom issue type scheme (Task ID 10050), add CONVENTIONS.md with `## Migration Patterns`, run `/plan-feature ACME-200`, observe the generated task.
- **Expected Result**: Convention references should use `§Migration Patterns` (title case); created issue should be type Task (ID 10050).
- **Actual Result**: Convention references use `§migration-patterns` (kebab-case); created issue is type Feature (ID 10142) instead of Task.

**Optional Sections**:

- **Root Cause** (from reporter): Not provided.
- **Suggested Fix** (from reporter): Two separate bugs identified -- convention reference formatter lowercases and kebab-cases headings incorrectly; task creation logic reads Feature issue type ID instead of Task issue type ID.
- **Attachments**: None.

## Step 2 -- Reproduce/Trace

These are skill/documentation bugs that cannot be directly reproduced via CLI commands. Code-path tracing was performed instead.

### Trace 1: Convention reference formatting

1. **Entry point**: `/plan-feature ACME-200` invocation.
2. **Execution path**: plan-feature Step 3 reads `CONVENTIONS.md` and discovers convention sections (e.g., `## Migration Patterns`). Step 5 performs "Convention-aware task enrichment" which cross-references discovered conventions against each task's scope and generates Implementation Notes references in the format `Per CONVENTIONS.md §<Section Name>: <action required>`.
3. **Divergence point**: The convention reference formatter in `shared/convention-applicability-rules.md` prescribes preserving the original heading text (e.g., `§Migration Patterns`). However, the formatting logic is converting the heading to a kebab-case slug (`§migration-patterns`) instead of preserving the original title-case heading. The slug conversion lowercases the heading and replaces spaces with hyphens, producing references that do not match the actual CONVENTIONS.md section names.

### Trace 2: Task issue type selection

1. **Entry point**: `/plan-feature ACME-200` invocation.
2. **Execution path**: plan-feature Step 2.5 dynamically discovers project issue types and maps them to hierarchy roles (Feature at level 2+, Epic at level 1, Task at level 0). Step 6a creates tasks using `jira.create_issue`.
3. **Divergence point**: In Step 6a, the task creation logic should use the dynamically discovered Task issue type (level 0, ID 10050 in this project's custom scheme). Instead, it reads the Feature issue type ID (10142) from the static `## Jira Configuration` in CLAUDE.md and uses that for task creation. The dynamic type-to-role mapping from Step 2.5 is not being consulted when creating the issue in Step 6a.

## Step 3 -- Codebase Investigation

### Target repository

The bug affects the `sdlc-workflow` plugin within the `sdlc-plugins` repository (component: sdlc-workflow).

### Affected files and modules

**Root Cause 1 -- Convention reference formatting:**

- **File**: `plugins/sdlc-workflow/shared/convention-applicability-rules.md`
  - This file defines the convention applicability rules and prescribes the format `Per CONVENTIONS.md §<Section Name>: <action required>` where `<Section Name>` must match the original CONVENTIONS.md heading text.
  - The convention reference format is also documented in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` in the "Convention-aware task enrichment" section (Step 5), which states: `"Per CONVENTIONS.md §<Section Name>: <specific action required>"`.
  - The bug is in whatever processing logic converts CONVENTIONS.md section headings into the `§` references -- it applies a slug/kebab-case transformation (lowercase + hyphen-separated) instead of preserving the original heading text.

**Root Cause 2 -- Wrong issue type for task creation:**

- **File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a
  - Step 2.5 correctly discovers the project's issue types and maps them to hierarchy roles (Task = level 0). The type-to-role mapping records the Task type ID dynamically.
  - Step 6a creates tasks with `jira.create_issue` but the issue type used is the Feature issue type ID (10142) from `## Jira Configuration` rather than the Task type ID from the Step 2.5 mapping.
  - The Jira Configuration section only stores `Feature issue type ID: 10142`; it does not store a Task issue type ID because that is meant to be discovered dynamically by Step 2.5.

### Independence of root causes

These two root causes are **independent**:

1. **Different modules**: Root Cause 1 is in the shared convention formatting logic (`shared/convention-applicability-rules.md`). Root Cause 2 is in the plan-feature task creation logic (`plan-feature/SKILL.md` Step 6a).
2. **Different code paths**: Root Cause 1 affects how convention section headings are formatted into `§` references during task description generation (Step 5). Root Cause 2 affects which issue type ID is passed to Jira when creating the task issue (Step 6a).
3. **Independent fixes**: Fixing the convention formatter does not affect or depend on fixing the issue type selection, and vice versa.
4. **Different symptoms**: Root Cause 1 produces malformed text in the task description content. Root Cause 2 produces the wrong issue type metadata on the created Jira issue.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention reference formatter uses kebab-case instead of preserving heading text

- **What is broken**: The convention reference formatter converts CONVENTIONS.md section headings into kebab-case slugs (e.g., `§migration-patterns`) when generating `Per CONVENTIONS.md §...` references in task Implementation Notes.
- **Why it is broken**: The formatting logic applies a slug transformation (lowercase + replace spaces with hyphens) to the heading text, which is appropriate for URL anchors but not for human-readable section references. The prescribed format in `shared/convention-applicability-rules.md` explicitly shows title-case headings (e.g., `§Migration Patterns`).
- **Where it is broken**: `plugins/sdlc-workflow/shared/convention-applicability-rules.md` -- the convention reference formatting logic that generates the `§` references during plan-feature Step 5's "Convention-aware task enrichment".
- **How to verify the fix**: A reproducer test should invoke the convention reference formatting with a CONVENTIONS.md containing `## Migration Patterns`, and assert the output contains `§Migration Patterns` (title case) rather than `§migration-patterns` (kebab-case).

### Root Cause 2: Task creation uses Feature issue type ID instead of dynamically discovered Task type

- **What is broken**: When creating tasks in plan-feature Step 6a, the skill uses the Feature issue type ID (10142) from the static Jira Configuration instead of the Task issue type ID discovered dynamically by Step 2.5.
- **Why it is broken**: Step 6a reads `Feature issue type ID` from `## Jira Configuration` in CLAUDE.md as the issue type for task creation, rather than consulting the type-to-role mapping built in Step 2.5 which correctly identifies the Task type (level 0) from the project's issue type scheme.
- **Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a -- the `jira.create_issue` call that creates task issues.
- **How to verify the fix**: A reproducer test should configure a project with a custom issue type scheme where Task has ID 10050 (different from Feature ID 10142), run plan-feature, and assert the created issue has `issuetype.id` equal to 10050 (Task), not 10142 (Feature).

### Comment that would be posted to ACME-502

**Root Cause**: This bug involves two independent defects:

1. The convention reference formatter in `shared/convention-applicability-rules.md` applies a kebab-case slug transformation to CONVENTIONS.md section headings instead of preserving their original title-case text. This causes Implementation Notes to contain `§migration-patterns` instead of the correct `§Migration Patterns`.

2. The task creation logic in `plan-feature/SKILL.md` Step 6a uses the Feature issue type ID (10142) from the static Jira Configuration rather than the Task issue type ID discovered dynamically by Step 2.5. This causes tasks to be created as Feature type instead of Task type.

**Affected Files**:
- `plugins/sdlc-workflow/shared/convention-applicability-rules.md` -- convention heading formatting logic
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Step 6a task creation issue type selection

**Suggested Approach**:
1. Fix the convention formatter to preserve original heading text from CONVENTIONS.md sections rather than applying slug transformation.
2. Fix Step 6a to use the Task type ID from the Step 2.5 type-to-role mapping instead of the Feature issue type ID from Jira Configuration.

**Reproducer Strategy**:
1. For Root Cause 1: Test that convention references preserve heading case (input: `## Migration Patterns`, expected output: `§Migration Patterns`).
2. For Root Cause 2: Test that task creation uses the dynamically discovered Task type ID (level 0) rather than the Feature type ID from configuration.
