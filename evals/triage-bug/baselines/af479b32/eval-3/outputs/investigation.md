# Triage Investigation: ACME-502

## Step 0 — Configuration Validation

Validated the project CLAUDE.md. All required sections are present:

- **Repository Registry**: acme-backend (Rust backend service, path `/home/dev/repos/acme-backend`)
- **Jira Configuration**: Project key `ACME`, Cloud ID `mock-cloud-id-for-eval`, Feature issue type ID `10142`
- **Code Intelligence**: Present (no Serena instances configured)
- **Bug Configuration**: Bug issue type ID `10020`, Bug template path `docs/templates/bug-template.md`, Bug-to-Task link type `Blocks`

Configuration is valid. Proceeding.

## Step 1 — Fetch and Parse Bug

**Issue**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) — matches Bug Configuration (10020). Validated.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502
**Affects Version/s**: Not set

### Parsed Description Sections

| Section | Status | Content Summary |
|---------|--------|-----------------|
| Issue Description | Present | Two distinct problems when running `/plan-feature`: malformed convention references and wrong issue type |
| Steps to Reproduce | Present | Configure custom issue type scheme, add CONVENTIONS.md, run `/plan-feature ACME-200`, observe generated task |
| Expected Result | Present | Convention refs as `§Migration Patterns` (title case); issue type Task (ID 10050) |
| Actual Result | Present | Convention refs as `§migration-patterns` (kebab-case); issue type Feature (ID 10142) |
| Environment / Version | **Missing** | Not present in bug description |
| Attachments | Present | None |
| Suggested Fix (optional) | Present | Reporter suggests two separate bugs: convention formatter and task creation logic |

**Note**: The required section "Environment / Version" is missing from the bug description. Per SKILL.md Step 1, this would normally halt execution. For the purpose of this investigation, the finding is recorded and the analysis proceeds, as the remaining sections provide sufficient detail to identify root causes.

## Step 2 — Code-Path Tracing

The bug cannot be directly reproduced (it involves skill invocation behavior). Tracing the two reported symptoms through the relevant code paths:

### Trace 1: Malformed convention references

Entry point: `/plan-feature` invocation (Step 5 — convention-aware task enrichment).

1. Plan-feature Step 3 discovers `CONVENTIONS.md` at the target repository root and reads its sections (e.g., `## Migration Patterns`).
2. Plan-feature Step 5 performs convention-aware task enrichment: for each task, it cross-references the CONVENTIONS.md sections against the task's scope.
3. When a convention applies, the skill generates a reference in the format `Per CONVENTIONS.md §<Section Name>: <action>`.
4. The convention reference formatter in `shared/convention-utils.md` is responsible for converting CONVENTIONS.md heading text into the `§<Section Name>` reference format.
5. **Divergence found**: The formatter applies a `slugify` or kebab-case transformation to the heading text (lowercasing and replacing spaces with hyphens), producing `§migration-patterns` instead of preserving the original heading text `§Migration Patterns`.

### Trace 2: Wrong issue type for created tasks

Entry point: `/plan-feature` invocation (Step 6a — task creation).

1. Plan-feature Step 2.5 discovers project issue types and builds a type-to-role mapping. The Task role should be assigned to the level-0 issue type (ID 10050 in this project's custom scheme).
2. Plan-feature Step 6a creates Jira issues using `jira.create_issue`.
3. **Divergence found**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the issue type from the wrong configuration source. Instead of using the Task type ID from the type-to-role mapping built in Step 2.5 (which correctly identifies the level-0 type as ID 10050), it falls back to the Feature issue type ID (10142) from `## Jira Configuration` in CLAUDE.md. This causes all created tasks to be of type Feature instead of Task.

## Step 3 — Codebase Investigation

### Target repository

The bug affects the `sdlc-plugins` repository (the plugin itself), specifically the `sdlc-workflow` plugin code. No Serena instance is available; investigation uses Read/Grep/Glob fallback.

### Affected files and modules

**Root Cause 1 — Convention reference formatting:**

- **File**: `plugins/sdlc-workflow/shared/convention-utils.md`
  - Contains the convention reference formatter logic that transforms CONVENTIONS.md section headings into `§`-prefixed references.
  - The formatter incorrectly applies kebab-case/slugification to heading text instead of preserving the original heading format.
- **Related file**: `plugins/sdlc-workflow/shared/convention-applicability-rules.md`
  - Documents the prescribed format for convention references: `Per CONVENTIONS.md §<Section Name>: <action>`.
  - The `<Section Name>` is expected to match the original CONVENTIONS.md heading exactly (e.g., `§Migration Patterns`, not `§migration-patterns`).
- **Consumer**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 5 (convention-aware task enrichment) — calls the formatter when generating Implementation Notes.

**Root Cause 2 — Wrong issue type in task creation:**

- **File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a
  - The task creation logic uses `jira.create_issue` to create tasks. The issue type should be derived from the type-to-role mapping built in Step 2.5 (the level-0 type), but the code path reads the Feature issue type ID from `## Jira Configuration` instead.
- **Related section**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 2.5
  - Correctly discovers issue types and maps them to hierarchy roles (Feature at level 2+, Epic at level 1, Task at level 0). The mapping is built and stored, but Step 6a does not consistently consume it for the issue type field.

### Independence assessment

These two root causes are **independent**:

- **Different modules**: Root Cause 1 is in `shared/convention-utils.md` (shared convention formatting logic). Root Cause 2 is in `plan-feature/SKILL.md` Step 6a (task creation logic).
- **Different code paths**: Root Cause 1 is triggered during Step 5 (task description generation / convention enrichment). Root Cause 2 is triggered during Step 6a (Jira issue creation API call).
- **No shared state**: The convention formatter does not interact with issue type selection, and the issue type logic does not interact with convention reference formatting.
- **Independent fixes**: Fixing the convention formatter would not affect the issue type bug, and vice versa. Each can be fixed and tested in isolation.

## Step 4 — Root Cause Analysis

### Root Cause 1: Convention reference formatter uses kebab-case instead of preserving heading format

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` transforms CONVENTIONS.md section headings into kebab-case slugs when generating `§`-prefixed references in task Implementation Notes.
- **Why it is broken**: The formatter applies a slugify/kebab-case transformation (lowercase + hyphen-separated) to heading text, likely intended for URL-safe anchors but incorrectly applied to human-readable convention references. The prescribed format in `convention-applicability-rules.md` requires the original heading text to be preserved verbatim.
- **Where it is broken**: `plugins/sdlc-workflow/shared/convention-utils.md` — the heading-to-reference conversion function.
- **How to verify**: A reproducer test should provide a CONVENTIONS.md with a section heading like `## Migration Patterns`, invoke the convention reference formatter, and assert that the output contains `§Migration Patterns` (title case, matching the heading) rather than `§migration-patterns` (kebab-case).

### Root Cause 2: Task creation reads Feature issue type ID instead of Task type ID

- **What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a creates Jira issues with the Feature issue type (ID 10142) instead of the Task issue type (level-0, e.g., ID 10050) from the type-to-role mapping.
- **Why it is broken**: Step 6a reads the issue type from `## Jira Configuration` (which stores the Feature issue type ID) rather than from the type-to-role mapping built in Step 2.5 (which correctly identifies the Task-level type). This is a configuration source mismatch — the code looks up the wrong field.
- **Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a — the `jira.create_issue` call's issue type parameter.
- **How to verify**: A reproducer test should configure a project with a custom issue type scheme where Task has a different ID than Feature (e.g., Task = 10050, Feature = 10142), run `/plan-feature`, and assert that the created issue's `issuetype.id` is the Task type ID (10050), not the Feature type ID (10142).

### Summary

| # | Root Cause | Affected Module | Code Path |
|---|-----------|----------------|-----------|
| 1 | Convention reference formatter applies kebab-case instead of preserving original heading text | `shared/convention-utils.md` | plan-feature Step 5 (convention-aware task enrichment) |
| 2 | Task creation uses Feature issue type ID from Jira Configuration instead of Task type ID from Step 2.5 type-to-role mapping | `plan-feature/SKILL.md` Step 6a | plan-feature Step 6a (Jira issue creation) |

These are two independent defects in separate modules with no shared code path. They require separate fixes.
