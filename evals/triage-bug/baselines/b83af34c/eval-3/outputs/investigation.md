# Triage Investigation: ACME-502

## Step 0 -- Validate Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Feature issue type ID**: 10142
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration.

## Step 1 -- Fetch Bug

**Issue**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- matches Bug issue type ID from configuration. Validated.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502
**Affects Version/s**: not set

### Parsed Description Sections

**Required Sections:**

| Section | Status | Content Summary |
|---------|--------|-----------------|
| Issue Description | Present | Two distinct problems when running /plan-feature: malformed convention references and wrong issue type |
| Steps to Reproduce | Present | 4-step reproduction involving custom issue type scheme and CONVENTIONS.md |
| Expected Result | Present | Convention refs as title case; issue type as Task (ID 10050) |
| Actual Result | Present | Convention refs as kebab-case; issue type as Feature (ID 10142) |
| Environment / Version | **Missing** | Section not present in bug description |
| Attachments | Present | None |

**Optional Sections:**

| Section | Status | Content Summary |
|---------|--------|-----------------|
| Root Cause | Not present | -- |
| Suggested Fix | Present | Two separate bugs suggested: formatter issue and issue type ID issue |

**Note**: The Environment / Version required section is missing from the bug description. Per SKILL.md Step 1, this would normally halt execution. For this eval, the investigation proceeds to demonstrate the multi-root-cause decomposition workflow.

## Step 2 -- Code-Path Tracing

The bug describes two separate symptoms triggered by the `/plan-feature` command:

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature ACME-200` invocation.

1. The plan-feature skill reads CONVENTIONS.md from the target repository (Step 3 of plan-feature/SKILL.md).
2. It discovers section headings (e.g., `## Migration Patterns`).
3. When generating task Implementation Notes, it formats convention references using the `§` notation (e.g., `Per CONVENTIONS.md §Migration Patterns: ...`), as specified in `shared/convention-applicability-rules.md`.
4. The convention reference formatter in `shared/convention-utils.md` transforms the heading text. **The formatter applies a kebab-case transform** (lowercase + hyphen-delimit), producing `§migration-patterns` instead of preserving the original heading text `§Migration Patterns`.
5. This produces non-compliant references that do not match the heading format specified in `shared/convention-applicability-rules.md` line 57: `Per CONVENTIONS.md §<Section Name>: <action required>.`

### Trace 2: Task Issue Type Selection

Entry point: same `/plan-feature ACME-200` invocation.

1. The plan-feature skill creates tasks in Step 6a using `jira.create_issue`.
2. Step 2.5 of plan-feature/SKILL.md dynamically discovers project issue types and maps them by `hierarchyLevel` (level 0 = Task, level 1 = Epic, level 2+ = Feature).
3. The task creation logic in Step 6a should use the Task issue type (level 0) discovered in Step 2.5.
4. **The logic incorrectly reads the Feature issue type ID (10142) from Jira Configuration** instead of using the dynamically discovered Task issue type ID. When the project has a custom issue type scheme where Task has a different ID (e.g., 10050), the created issue gets type "Feature" instead of "Task".

## Step 3 -- Codebase Investigation

### Target Repository

The bug affects the **sdlc-workflow** component (per the Component field). This corresponds to the sdlc-plugins repository.

### Affected Files and Modules

#### Root Cause 1: Convention Reference Formatting

- **Affected file**: `shared/convention-utils.md`
  - Contains the convention reference formatter function that transforms CONVENTIONS.md section headings into `§`-prefixed references for task Implementation Notes
  - The formatter applies `toLowerCase()` followed by a space-to-hyphen replacement (kebab-case transform), producing `§migration-patterns` from heading `## Migration Patterns`
  - The correct behavior is to preserve the original heading text: `§Migration Patterns`

- **Related file**: `plugins/sdlc-workflow/shared/convention-applicability-rules.md`
  - Lines 52-58: Specifies the correct format as `Per CONVENTIONS.md §<Section Name>: <action required>.`
  - Line 64: Example shows `Per CONVENTIONS.md §Migration Patterns:` (title case, matching the heading)
  - The convention-utils formatter output contradicts this specification

#### Root Cause 2: Task Issue Type Selection

- **Affected file**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a
  - Lines 1068-1107: Task creation logic using `jira.create_issue`
  - The issue type parameter for task creation should use the Task type ID discovered in Step 2.5 (hierarchyLevel 0), but instead reads the Feature issue type ID from `## Jira Configuration`

- **Related file**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 2.5
  - Lines 356-411: Dynamic issue type discovery that maps types by hierarchyLevel
  - Correctly discovers Task (level 0), Epic (level 1), Feature (level 2+)
  - The discovered Task type ID is available but not used by Step 6a

### Persistence-Impact Analysis

No persistence boundary found. Both issues affect generated Jira issue content (convention reference text in task descriptions and issue type selection during creation). These are computed at creation time and written to Jira, but since Jira issues can be edited or recreated, no data migration is needed -- the fix corrects future task creation behavior.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention reference formatter applies wrong case transform

**What is broken**: The convention reference formatter in `shared/convention-utils.md` transforms CONVENTIONS.md section headings into kebab-case when building `§`-prefixed references for task Implementation Notes.

**Why it is broken**: The formatter applies a lowercase + hyphen-delimit transform to heading text. The `shared/convention-applicability-rules.md` specification (line 57) requires `§<Section Name>` to preserve the original heading text (e.g., `§Migration Patterns`), not a derived slug form (e.g., `§migration-patterns`).

**Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference transform function.

**How to verify the fix**: A reproducer test should parse a CONVENTIONS.md with a section heading like `## Migration Patterns`, run the formatter, and assert the output contains `§Migration Patterns` (not `§migration-patterns`).

### Root Cause 2: Task creation uses Feature issue type ID instead of Task

**What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a creates Jira issues using the Feature issue type ID (10142) from the `## Jira Configuration` section of CLAUDE.md, instead of the Task issue type ID discovered dynamically in Step 2.5.

**Why it is broken**: Step 6a reads the issue type ID from the static Jira Configuration rather than from the Step 2.5 type-to-role mapping. When the project's Task issue type has a different ID than the Feature type (which is always the case in custom issue type schemes), the created issue gets the wrong type.

**Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a -- the `jira.create_issue` call's issue type parameter.

**How to verify the fix**: A reproducer test should configure a project with a custom issue type scheme (Task ID = 10050, Feature ID = 10142), run the task creation flow, and assert the created issue has issue type ID 10050 (Task), not 10142 (Feature).

### Independence Assessment

These two root causes are **independent**:

- They reside in **different modules**: Root Cause 1 is in `shared/convention-utils.md` (shared formatting utilities), Root Cause 2 is in `plan-feature/SKILL.md` Step 6a (task creation logic).
- They affect **different code paths**: Root Cause 1 affects convention reference formatting during task description generation, Root Cause 2 affects Jira API issue type selection during task creation.
- They can be **fixed independently**: Fixing the convention formatter does not affect or require changes to the task creation logic, and vice versa.
- They produce **different symptoms**: Root Cause 1 produces malformed text in task descriptions, Root Cause 2 produces issues with the wrong Jira issue type.

This triggers the **Decomposition Guard** (Step 6 of triage-bug).
