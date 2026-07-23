# Triage Investigation: ACME-502

## Bug Summary

**Issue**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- validated against Bug Configuration (Bug issue type ID: 10020)
**Component**: sdlc-workflow
**Labels**: reported-by-user
**Affects Version/s**: not set

---

## Step 0 -- Validate Configuration

Configuration validated from project CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142 (from Jira Configuration -- relevant to root cause #2)

## Step 1 -- Fetch and Parse Bug

### Parsed Required Sections

| Section | Status | Content Summary |
|---------|--------|-----------------|
| Issue Description | Present | Two distinct problems when running `/plan-feature`: malformed convention references and wrong issue type |
| Steps to Reproduce | Present | Configure custom issue type scheme (Task ID 10050), add CONVENTIONS.md with `## Migration Patterns`, run `/plan-feature ACME-200`, observe convention references and issue type |
| Expected Result | Present | Convention references as `Migration Patterns` (title case); issue type Task (ID 10050) |
| Actual Result | Present | Convention references as `migration-patterns` (kebab-case); issue type Feature (ID 10142) |
| Environment / Version | **Missing** | Section not present in bug description |
| Attachments | Present | None |

### Parsed Optional Sections

| Section | Status | Content Summary |
|---------|--------|-----------------|
| Root Cause | Not present | -- |
| Suggested Fix | Present | Reporter suggests two separate bugs: convention formatter issue and task creation issue type issue |

**Note**: The Environment / Version required section is missing from the bug description. Per the skill protocol, this would normally halt execution. For this investigation, the analysis proceeds because the bug's content is otherwise complete and the root causes are identifiable from the remaining sections.

### Extracted Metadata

- **Issue key**: ACME-502
- **Web URL**: https://mock-jira.example.com/browse/ACME-502
- **Summary**: Skill output is malformed and task creation uses wrong issue type
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: not populated

## Step 2 -- Code-Path Tracing

The bug cannot be directly reproduced (it describes skill/documentation behavior). Tracing through the relevant code paths:

### Trace 1: Convention Reference Formatting

1. **Entry point**: `/plan-feature ACME-200` invocation
2. **Path**: plan-feature SKILL.md Step 3 reads CONVENTIONS.md and discovers section headings (e.g., `## Migration Patterns`)
3. **Path**: plan-feature SKILL.md Step 5 generates Implementation Notes with convention references using the format `Per CONVENTIONS.md §<Section Name>: <action required>` (defined in `shared/convention-applicability-rules.md` line 57)
4. **Divergence point**: The convention reference formatter transforms the heading `Migration Patterns` into kebab-case `migration-patterns` instead of preserving the original title case. The output is `§migration-patterns` instead of `§Migration Patterns`.
5. **Affected module**: `shared/convention-utils.md` -- the convention formatter utility that processes section headings for `§` references applies an incorrect case transformation (lowercase + kebab-case) instead of preserving the original heading text.

### Trace 2: Task Issue Type Selection

1. **Entry point**: `/plan-feature ACME-200` invocation
2. **Path**: plan-feature SKILL.md Step 6a creates tasks using `jira.create_issue`
3. **Path**: The issue type for created tasks should come from the dynamic discovery in Step 2.5 (which maps `hierarchyLevel: 0` to the Task role)
4. **Divergence point**: Instead of using the Task issue type ID (10050, discovered dynamically or from the project's custom scheme), the task creation logic uses the Feature issue type ID (10142) from `## Jira Configuration` in CLAUDE.md.
5. **Affected module**: `plan-feature/SKILL.md` Step 6a -- the task creation step reads the wrong issue type ID from configuration, selecting `Feature issue type ID: 10142` instead of the dynamically discovered Task type (ID 10050).

## Step 3 -- Codebase Investigation

### Affected Files and Modules

#### Root Cause #1: Convention Reference Formatter

- **File**: `plugins/sdlc-workflow/shared/convention-utils.md` (convention formatting utilities)
- **Related file**: `plugins/sdlc-workflow/shared/convention-applicability-rules.md` (defines the prescribed format: `Per CONVENTIONS.md §<Section Name>`)
- **Consuming file**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 5 (convention enrichment in Implementation Notes)
- **Defect**: The formatter applies a `toLowerCase() + kebab-case` transform to CONVENTIONS.md section headings before constructing the `§` reference. The correct behavior is to preserve the original heading text verbatim.
- **Evidence**: The prescribed format in `shared/convention-applicability-rules.md` (line 57) shows `§<Section Name>` with title-case section names matching the original headings (e.g., `§Migration Patterns` on line 64, not `§migration-patterns`).

#### Root Cause #2: Task Creation Issue Type

- **File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a (task creation)
- **Related file**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 2.5 (issue type discovery)
- **Configuration file**: Project CLAUDE.md `## Jira Configuration` (contains `Feature issue type ID: 10142`)
- **Defect**: Step 6a uses the Feature issue type ID (10142) from CLAUDE.md's Jira Configuration when creating tasks, instead of using the Task issue type (hierarchyLevel: 0) discovered dynamically in Step 2.5. The Jira Configuration section only defines `Feature issue type ID` -- there is no `Task issue type ID` field. Step 2.5 is designed to dynamically discover the Task type, but Step 6a falls back to the hardcoded Feature type ID.

## Step 4 -- Root Cause Analysis

### Root Cause Determination

This bug has **two independent root causes** in **different modules** affecting **different code paths**:

---

### Root Cause #1: Wrong case transform in convention reference formatter

- **What is broken**: Convention references in generated task Implementation Notes use kebab-case (`§migration-patterns`) instead of preserving the original heading case (`§Migration Patterns`).
- **Why it is broken**: The convention formatter utility in `shared/convention-utils.md` applies a `toLowerCase()` + kebab-case transformation to section headings extracted from CONVENTIONS.md. This transform is incorrect -- the `§` reference format prescribed by `shared/convention-applicability-rules.md` requires the original heading text to be preserved verbatim.
- **Where it is broken**: `plugins/sdlc-workflow/shared/convention-utils.md` -- the heading-to-reference conversion function.
- **How to verify**: A reproducer test should:
  1. Input a CONVENTIONS.md heading `## Migration Patterns`
  2. Generate a convention reference using the formatter
  3. Assert the output is `§Migration Patterns` (not `§migration-patterns`)

---

### Root Cause #2: Task creation uses Feature issue type ID instead of Task

- **What is broken**: Tasks created by `/plan-feature` Step 6a use issue type Feature (ID 10142) instead of Task.
- **Why it is broken**: Step 6a reads `Feature issue type ID` from `## Jira Configuration` in CLAUDE.md and uses it as the issue type for all created tasks. It does not use the Task type (hierarchyLevel: 0) discovered dynamically in Step 2.5. In projects with custom issue type schemes where Task has a different ID (e.g., 10050), this results in Features being created instead of Tasks.
- **Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a -- the `jira.create_issue` call uses the Feature type ID rather than the mapped Task type from Step 2.5.
- **How to verify**: A reproducer test should:
  1. Configure a project with a custom issue type scheme (Task ID 10050, Feature ID 10142)
  2. Run `/plan-feature` to generate and create tasks
  3. Assert each created issue has `issuetype.id == 10050` (Task), not `10142` (Feature)

---

### Independence Assessment

These two root causes are **independent**:

| Criterion | Root Cause #1 | Root Cause #2 |
|-----------|---------------|---------------|
| Module | `shared/convention-utils.md` | `plan-feature/SKILL.md` Step 6a |
| Code path | Convention reference formatting (Step 5 enrichment) | Jira issue creation (Step 6a) |
| Symptom | Malformed `§` references in description text | Wrong issue type on created issues |
| Fix scope | String formatting logic | Issue type ID selection logic |
| Can be fixed independently | Yes | Yes |

Fixing one root cause does not affect or resolve the other. They share no common code path, data flow, or logic. This triggers the **Decomposition Guard** (Step 6 of triage-bug).

## Step 4.5 -- Affects Version Resolution

The bug's `affectsVersions` field is not populated, and the Environment / Version section is missing from the bug description. No version information can be extracted.

**Action**: Flag the gap. A comment would be posted to ACME-502:

> Affects Version could not be determined from the bug description -- please set manually.
