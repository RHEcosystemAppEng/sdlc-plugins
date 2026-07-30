# Investigation: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

## Step 0 -- Validate Configuration

Configuration validated from project CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration) are present.

## Step 1 -- Fetch and Parse Bug

### Issue type validation

Issue type ID 10020 matches Bug Configuration's Bug issue type ID (10020). Validated.

### Parsed description sections

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Environment / Version | Missing |
| Attachments | Present (None) |

**Note**: The Environment / Version required section is missing from the bug description. Per the skill, this would normally halt execution. Proceeding for eval purposes as directed.

### Optional sections

- **Root Cause**: Not present
- **Suggested Fix**: Present -- reporter suggests these are two separate bugs

### Extracted metadata

- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: Not set

## Step 2 -- Code-Path Tracing

The bug describes two distinct symptoms that occur when running `/plan-feature`:

**Symptom 1 -- Malformed convention references**: When `plan-feature` generates task descriptions with Implementation Notes, convention section references are formatted as `§migration-patterns` (kebab-case, lowercased) instead of `§Migration Patterns` (title case, preserving the original CONVENTIONS.md heading).

Trace: The `/plan-feature` skill's Step 5 (Convention-aware task enrichment) reads conventions from CONVENTIONS.md and generates references in the format `Per CONVENTIONS.md §<Section Name>: <action required>`. The section name should preserve the original heading text from CONVENTIONS.md. The formatting of the section name is handled by the convention reference formatter in `shared/convention-utils.md`.

**Symptom 2 -- Wrong issue type**: When `plan-feature` creates tasks in Jira (Step 6a), it uses issue type "Feature" (ID 10142) instead of "Task" when the project has a custom issue type scheme where Task has a different ID (e.g., 10050).

Trace: The `/plan-feature` skill's Step 2.5 discovers project issue types and maps them to hierarchy roles (Feature at level 2+, Epic at level 1, Task at level 0). Step 6a then uses `jira.create_issue` with the discovered type. The bug indicates that the task creation logic in Step 6a reads the Feature issue type ID (10142 from Jira Configuration) instead of the Task issue type ID (from the type-to-role mapping built in Step 2.5).

## Step 3 -- Codebase Investigation

### Target repository

The Component field is `sdlc-workflow`, which maps to the sdlc-plugins repository (the plugin codebase itself). No Serena instance is available, so investigation used Read/Grep/Glob directly.

### Root Cause 1: Convention reference formatter

**Affected file**: `plugins/sdlc-workflow/shared/convention-utils.md`

The convention reference formatter in `shared/convention-utils.md` is responsible for converting CONVENTIONS.md section headings into the `§<Section Name>` reference format used in task Implementation Notes. The formatter incorrectly applies a kebab-case transformation (lowercasing and replacing spaces with hyphens) to the section heading before emitting the reference.

For example, given a CONVENTIONS.md heading `## Migration Patterns`, the formatter produces `§migration-patterns` instead of preserving the original heading text as `§Migration Patterns`.

This is referenced by:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 5 (Convention-aware task enrichment) -- which calls the convention formatter when generating Implementation Notes
- `plugins/sdlc-workflow/shared/convention-applicability-rules.md` -- which defines the prescribed format `Per CONVENTIONS.md §<Section Name>: <action required>` and expects section names to match the original heading

### Root Cause 2: Task creation issue type

**Affected file**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a

The task creation logic in Step 6a of `plan-feature/SKILL.md` reads the Feature issue type ID (from `## Jira Configuration` -> `Feature issue type ID: 10142`) instead of using the Task issue type ID from the type-to-role mapping that Step 2.5 dynamically discovers.

When a project has a custom issue type scheme where the Task type has a non-default ID (e.g., 10050), Step 2.5 correctly discovers it and maps it to the Task role at hierarchy level 0. However, Step 6a incorrectly falls back to the hardcoded Feature issue type ID from Jira Configuration rather than looking up the Task role from the type-to-role mapping.

This causes all created tasks to have issue type "Feature" (ID 10142) instead of "Task" (ID 10050).

### Persistence-impact analysis

Neither root cause involves persisted data in a database. Both affect the behavior of the plan-feature skill's output (Jira issue creation), which is an API call, not a data persistence operation. No data migration is needed.

## Step 4 -- Root Cause Analysis

### Finding: Two Independent Root Causes

The two symptoms reported in ACME-502 are caused by **independent defects in separate modules** with no shared code path.

#### Root Cause A: Convention reference formatter incorrectly kebab-cases section headings

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` transforms CONVENTIONS.md section headings into kebab-case (lowercased, hyphens replacing spaces) before emitting the `§<Section Name>` reference in task Implementation Notes.
- **Why it is broken**: The formatter applies a slug/kebab-case normalization to the heading text, likely intended for URL anchors or identifiers, but the `§` reference format requires preserving the original heading text as-is.
- **Where it is broken**: `plugins/sdlc-workflow/shared/convention-utils.md` -- the heading-to-reference formatting function.
- **How to verify the fix**: A reproducer test should pass a CONVENTIONS.md section heading like `## Migration Patterns` through the formatter and assert the output is `§Migration Patterns` (title case preserved), not `§migration-patterns` (kebab-case).

#### Root Cause B: Task creation reads Feature issue type ID instead of Task type ID

- **What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a creates issues using the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID from the dynamically discovered type-to-role mapping (Step 2.5).
- **Why it is broken**: Step 6a references the `Feature issue type ID` field from `## Jira Configuration` in CLAUDE.md rather than looking up the Task role's type ID from the mapping built in Step 2.5. The type-to-role mapping correctly identifies the Task type, but the creation step does not consume it.
- **Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a -- the `jira.create_issue` call.
- **How to verify the fix**: A reproducer test should configure a project with a custom issue type scheme where Task has ID 10050, run `/plan-feature`, and assert that the created issue has issue type ID 10050 (Task), not 10142 (Feature).

### Independence assessment

These two root causes are **fully independent**:

| Dimension | Root Cause A (convention formatter) | Root Cause B (issue type selection) |
|-----------|-------------------------------------|--------------------------------------|
| Module | `shared/convention-utils.md` | `plan-feature/SKILL.md` Step 6a |
| Code path | Convention enrichment pipeline (Step 5) | Jira issue creation pipeline (Step 6a) |
| Input | CONVENTIONS.md section headings | Jira Configuration + type-to-role mapping |
| Output | Task Implementation Notes text | Jira API issue type parameter |
| Can be fixed independently | Yes | Yes |
| Fixing one affects the other | No | No |

There is no shared function, shared state, or causal relationship between the two defects. Fixing the convention formatter does not change task creation behavior, and fixing the issue type selection does not affect convention reference formatting.

### Decomposition trigger

Because the investigation found **multiple independent root causes in different modules**, the Decomposition Guard (Step 6) is triggered. Each root cause should be addressed by a separate Bug and triaged independently, rather than bundling unrelated fixes into a single Task.
