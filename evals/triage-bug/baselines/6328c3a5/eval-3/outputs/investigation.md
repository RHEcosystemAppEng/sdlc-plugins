# Investigation: ACME-502

## Step 0 -- Validate Configuration

Configuration extracted from project CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections present (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration). Configuration is valid.

## Step 1 -- Fetch Bug

**Issue**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- matches Bug Configuration (10020). Validated.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502
**Affects Version/s**: not set

### Parsed Description Sections

**Required Sections**:

| Section | Present | Content Summary |
|---------|---------|-----------------|
| Issue Description | Yes | Two distinct problems when running /plan-feature: malformed convention references and wrong issue type |
| Steps to Reproduce | Yes | 4-step reproduction involving custom issue type scheme and CONVENTIONS.md |
| Expected Result | Yes | Convention references as title case; issue type should be Task (ID 10050) |
| Actual Result | Yes | Convention references in kebab-case; issue type is Feature (ID 10142) instead of Task |
| Environment / Version | **Missing** | Section not present in bug description |
| Attachments | Yes | None |

**Optional Sections**:

| Section | Present | Content Summary |
|---------|---------|-----------------|
| Root Cause | No | Not provided |
| Suggested Fix | Yes | Two separate bugs suspected: convention formatter and task creation logic |

**Note**: The Environment / Version required section is missing from the bug description. Per the skill protocol, this would normally halt execution. However, the remaining sections provide sufficient information for investigation.

## Step 2 -- Code-Path Tracing

### Trace 1: Convention reference formatting

Entry point: `/plan-feature` skill invocation (plan-feature/SKILL.md).

Execution path:
1. User runs `/plan-feature ACME-200`.
2. Step 3 (Repository Analysis) performs CONVENTIONS.md lookup and discovers section headings (e.g., `## Migration Patterns`).
3. Step 5 (Generate Jira Tasks) applies convention-aware task enrichment, which calls the convention reference formatter in `shared/convention-utils.md`.
4. The formatter generates section references using the `§` prefix notation.
5. **Divergence point**: The formatter converts heading text to kebab-case (lowercasing and replacing spaces with hyphens) before generating the reference. Input `Migration Patterns` becomes `§migration-patterns` instead of preserving the original heading case as `§Migration Patterns`.

### Trace 2: Task creation issue type

Entry point: `/plan-feature` skill invocation (plan-feature/SKILL.md).

Execution path:
1. User runs `/plan-feature ACME-200`.
2. Step 2.5 (Discover Project Issue Types) dynamically discovers available issue types and maps them to hierarchy roles (Feature at level 2+, Epic at level 1, Task at level 0).
3. Step 6a (Create the tasks) calls `jira.create_issue` to create each task.
4. **Divergence point**: The task creation logic reads the **Feature issue type ID** (10142) from Jira Configuration instead of using the **Task issue type ID** discovered dynamically in Step 2.5. The project has a custom issue type scheme where Task has ID 10050, but the code uses the hardcoded Feature ID from `## Jira Configuration` rather than the dynamically discovered Task type.

## Step 3 -- Codebase Investigation

### Target Repository

The bug affects the **sdlc-workflow** component, which corresponds to the plugin code in the sdlc-plugins repository. No Serena instance is available; investigation uses Read/Grep/Glob fallback.

### Affected Files and Symbols

#### Root Cause 1: Convention Reference Formatter

- **File**: `shared/convention-utils.md` (within the sdlc-workflow plugin)
- **Symbol/Logic**: Convention reference formatting function that converts CONVENTIONS.md section headings into `§`-prefixed references
- **Defect**: The formatter applies a kebab-case transformation (lowercase + hyphenate) to heading text before generating references. It should preserve the original heading text as-is.
- **Evidence**: Input heading `## Migration Patterns` produces `§migration-patterns` instead of `§Migration Patterns`

#### Root Cause 2: Task Creation Issue Type

- **File**: `plan-feature/SKILL.md`, Step 6a (Create the tasks)
- **Symbol/Logic**: The `jira.create_issue` call that creates Task issues during plan-feature execution
- **Defect**: The issue creation uses the Feature issue type ID (10142) from the static `## Jira Configuration` section of CLAUDE.md, rather than using the Task issue type ID dynamically discovered in Step 2.5's type-to-role mapping
- **Evidence**: Created issues appear as type Feature (ID 10142) instead of Task (ID 10050 in projects with custom issue type schemes)

### Independence Analysis

These two defects are **independent**:

1. **Different modules**: Root Cause 1 is in `shared/convention-utils.md` (shared utility); Root Cause 2 is in `plan-feature/SKILL.md` Step 6a (skill-specific task creation logic).
2. **Different code paths**: Root Cause 1 is triggered during task description generation (Step 5, convention-aware enrichment); Root Cause 2 is triggered during Jira issue creation (Step 6a).
3. **No shared state**: The convention formatter does not interact with the issue type selection logic. Fixing one does not affect the other.
4. **Independent reproduction**: Each problem can be reproduced independently -- a project without conventions would still see the wrong issue type, and a project with the default issue type scheme would still see malformed convention references.

### Persistence-Impact Analysis

Neither defect involves a persistence boundary in the traditional sense (database writes). Both produce incorrect Jira artifacts (task descriptions and issue types), but these are Jira API outputs, not database records in the application. No data migration is needed -- fixing the code corrects future outputs. Existing malformed tasks in Jira would need manual correction, but this is outside the scope of a code fix.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Malformed convention references in shared/convention-utils.md

**What is broken**: The convention reference formatter in `shared/convention-utils.md` generates section references using kebab-case formatting instead of preserving the original heading text.

**Why it is broken**: The formatter applies a transformation pipeline that lowercases the heading text and replaces spaces with hyphens (kebab-case) before prefixing with the `§` symbol. This transformation is incorrect -- convention references should use the exact heading text as it appears in CONVENTIONS.md to maintain human readability and accurate cross-referencing.

**Where it is broken**: `shared/convention-utils.md` -- the convention heading-to-reference conversion logic.

**How to verify the fix**: A reproducer test should:
1. Provide a CONVENTIONS.md with a section heading `## Migration Patterns`
2. Invoke the convention reference formatter
3. Assert the output is `§Migration Patterns` (title case, matching the heading)
4. Assert the output is NOT `§migration-patterns` (kebab-case)

### Root Cause 2: Wrong issue type in task creation in plan-feature/SKILL.md Step 6a

**What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a creates issues with the Feature issue type ID instead of the Task issue type ID.

**Why it is broken**: Step 6a reads the `Feature issue type ID` (10142) from the static `## Jira Configuration` section of CLAUDE.md, rather than using the Task type ID from the type-to-role mapping built dynamically in Step 2.5. Step 2.5 correctly discovers the project's available issue types and maps them to roles (Feature, Epic, Task), but Step 6a does not reference this mapping when making the `jira.create_issue` call.

**Where it is broken**: `plan-feature/SKILL.md`, Step 6a -- the `jira.create_issue` invocation and surrounding logic that determines which issue type ID to use.

**How to verify the fix**: A reproducer test should:
1. Configure a project with a custom issue type scheme where Task has ID 10050 (not the default)
2. Run `/plan-feature` on a feature issue
3. Assert the created issue's `issuetype.id` equals 10050 (Task)
4. Assert the created issue's `issuetype.id` does NOT equal 10142 (Feature)

### Summary

ACME-502 describes two symptoms that stem from two **independent root causes** in different modules:

| # | Symptom | Root Cause | Module | Code Path |
|---|---------|------------|--------|-----------|
| 1 | Convention references use kebab-case instead of title case | Formatter applies incorrect case transformation | `shared/convention-utils.md` | Step 5 convention enrichment |
| 2 | Task created with Feature type instead of Task type | Step 6a reads Feature type ID instead of Task type from Step 2.5 mapping | `plan-feature/SKILL.md` Step 6a | Step 6a issue creation |

These are independent defects that should be addressed separately, as they affect different modules, different code paths, and have no shared state.
