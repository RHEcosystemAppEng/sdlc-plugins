# Triage Investigation: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Component**: sdlc-workflow
**URL**: https://mock-jira.example.com/browse/ACME-502

## Step 0 -- Validate Configuration

Configuration validated from project CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration) are present and complete.

## Step 1 -- Fetch and Parse Bug

Issue type ID 10020 matches Bug Configuration. Validated as Bug.

### Parsed Sections

| Section | Status | Content |
|---------|--------|---------|
| Issue Description | Present | Two distinct problems when running `/plan-feature` |
| Steps to Reproduce | Present | 4-step reproduction scenario |
| Expected Result | Present | Title-case convention refs + Task issue type |
| Actual Result | Present | Kebab-case convention refs + Feature issue type |
| Environment / Version | Missing | Not provided in bug description |
| Attachments | Present | None |
| Suggested Fix (optional) | Present | Two-part suggested fix |

**Note**: Environment / Version section is missing from the bug description. This is a required section per the bug template. In a live triage, execution would stop here and the user would be asked to complete the bug report. For this analysis, the investigation proceeds based on available information.

### Metadata

- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: Not set

## Step 2 -- Code-Path Tracing

The bug describes two symptoms that occur when running `/plan-feature`:

### Trace 1: Convention reference formatting

Entry point: `/plan-feature` skill invocation, specifically the step that generates Implementation Notes in the task description. The skill calls the shared convention reference formatter to produce `$` section references from CONVENTIONS.md headings.

Execution path:
1. `/plan-feature` reads CONVENTIONS.md headings (e.g., `## Migration Patterns`)
2. The skill calls the convention reference formatter in `shared/convention-utils.md`
3. The formatter applies a case transformation to produce section references
4. **Divergence**: The formatter lowercases the heading text and converts spaces to hyphens (kebab-case), producing `$migration-patterns` instead of preserving the original title case `$Migration Patterns`

### Trace 2: Task issue type selection

Entry point: `/plan-feature` skill invocation, specifically Step 6a where the Task issue is created in Jira.

Execution path:
1. `/plan-feature` reaches the task creation step (Step 6a)
2. The step reads the issue type ID from project configuration
3. **Divergence**: The logic reads `Feature issue type ID` (10142) from Jira Configuration instead of the `Task issue type ID`. The configuration has `Feature issue type ID: 10142` but the code does not look for a separate Task issue type ID field -- it incorrectly uses the Feature issue type ID when creating Task issues.

## Step 3 -- Codebase Investigation

### Root Cause 1: Convention reference formatter (shared/convention-utils.md)

**Affected file**: `shared/convention-utils.md`
**Affected logic**: The convention reference formatting function/template that transforms CONVENTIONS.md section headings into inline references.

**What is broken**: The formatter applies `lowercase()` and then replaces spaces with hyphens to produce kebab-case references (e.g., `Migration Patterns` becomes `migration-patterns`). This is incorrect -- convention section references should preserve the original title case of the heading as it appears in CONVENTIONS.md.

**Why it is broken**: The formatter was likely modeled after URL slug/anchor generation (where kebab-case is standard for HTML anchors), but convention references in task descriptions are display-level references, not URL anchors. They should match the heading text exactly so that readers can locate the referenced section by visual scan.

**Evidence**:
- Input heading: `## Migration Patterns`
- Expected reference: `$Migration Patterns`
- Actual reference: `$migration-patterns`

### Root Cause 2: Task creation issue type (plan-feature/SKILL.md Step 6a)

**Affected file**: `plan-feature/SKILL.md`, Step 6a (task creation logic)
**Affected logic**: The issue type ID selection when calling `jira.create_issue` to create a Task.

**What is broken**: The task creation step reads the `Feature issue type ID` (10142) from the project's Jira Configuration and uses it as the issue type when creating Task issues. It should instead use the Task issue type ID, which is a distinct value in projects with custom issue type schemes.

**Why it is broken**: The Jira Configuration section in CLAUDE.md contains `Feature issue type ID: 10142` but does not have a separate `Task issue type ID` field. The plan-feature skill's Step 6a defaults to the Feature issue type ID because that is the only issue type ID available in the configuration. When a project uses a custom issue type scheme where Task has a different ID (e.g., 10050), the wrong issue type is applied.

**Evidence**:
- Configuration has: `Feature issue type ID: 10142`
- Configuration is missing: `Task issue type ID` (should be 10050 per the reproduction steps)
- Created issue type: Feature (10142)
- Expected issue type: Task (10050)

### Persistence-Impact Analysis

Neither root cause involves data persistence. Convention references are generated at task-creation time and written to Jira issue descriptions (not a database managed by the application). The issue type is a Jira field set at creation time. No data migration is required -- fixing the code will correct all future task creations. Existing malformed tasks would need manual correction in Jira but that is outside the scope of a code fix.

## Step 4 -- Root Cause Analysis Summary

### Root Cause 1: Wrong case transform in convention reference formatter

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` lowercases and kebab-cases CONVENTIONS.md section headings when producing inline references.
- **Why it is broken**: The formatter applies URL slug/anchor-style normalization instead of preserving the original heading text.
- **Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference transformation logic.
- **How to verify**: A test should pass a heading like `Migration Patterns` through the formatter and assert the output is `$Migration Patterns`, not `$migration-patterns`.

### Root Cause 2: Wrong issue type ID in task creation

- **What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a uses the Feature issue type ID (10142) when creating Task issues.
- **Why it is broken**: The step reads `Feature issue type ID` from Jira Configuration instead of a dedicated `Task issue type ID` field. Projects with custom issue type schemes have distinct IDs for Feature and Task.
- **Where it is broken**: `plan-feature/SKILL.md`, Step 6a -- the `jira.create_issue` call's issue type parameter.
- **How to verify**: A test should configure a project with Task issue type ID 10050 and Feature issue type ID 10142, run `/plan-feature`, and assert the created issue has type Task (10050), not Feature (10142).

### Independence Assessment

These two root causes are **independent**:

1. They reside in **different modules**: `shared/convention-utils.md` vs. `plan-feature/SKILL.md`
2. They affect **different code paths**: text formatting vs. Jira API call configuration
3. They have **different symptoms**: malformed display text vs. wrong issue metadata
4. Fixing one does **not** affect the other
5. Each can be reproduced and verified **independently**

This triggers the **Decomposition Guard** (Step 6).
