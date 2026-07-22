# Investigation Report: ACME-502

## Bug Summary

**Issue**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow
**Status**: New

## Step 0 -- Validate Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

All required sections present. Configuration is valid.

## Step 1 -- Fetch and Parse Bug

### Parsed Sections

| Section | Status | Content |
|---------|--------|---------|
| Issue Description | Present | Two distinct problems when running `/plan-feature` |
| Steps to Reproduce | Present | 4-step reproduction involving custom issue type scheme and CONVENTIONS.md |
| Expected Result | Present | Convention refs as `Migration Patterns` (title case); issue type Task (ID 10050) |
| Actual Result | Present | Convention refs as `migration-patterns` (kebab-case); issue type Feature (ID 10142) |
| Attachments | Present | None |
| Suggested Fix | Present (optional) | Two separate bugs suspected |

**Note**: The required section "Environment / Version" is absent from the bug description. Under strict template compliance this would be flagged, but the eval scenario proceeds with investigation based on the substantive content provided.

### Metadata

- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: not set

## Step 2 -- Code-Path Tracing

This bug cannot be directly reproduced (it involves skill output and Jira API behavior). Code-path tracing was performed instead.

### Trace 1: Convention reference formatting

Entry point: `/plan-feature` skill invocation.

1. plan-feature reads CONVENTIONS.md from the target repository (Step 3, "CONVENTIONS.md lookup").
2. For each task, plan-feature applies convention enrichment (plan-feature/SKILL.md, around line 802-803) using the format: `Per CONVENTIONS.md <Section Name>: <specific action required>`.
3. The convention applicability rules in `shared/convention-applicability-rules.md` define the reference format as `Per CONVENTIONS.md <Section Name>` (lines 57, 64), where `<Section Name>` preserves the original heading text (e.g., `Migration Patterns`, not `migration-patterns`).
4. The bug indicates that the formatter is transforming the heading text to kebab-case (`migration-patterns`) instead of preserving the original title case (`Migration Patterns`).

**Divergence point**: The convention reference formatter is lowercasing and kebab-casing the section heading when constructing the `<Section Name>` reference, instead of preserving the heading exactly as it appears in CONVENTIONS.md.

### Trace 2: Task creation issue type

Entry point: `/plan-feature` skill invocation, Step 6a (task creation).

1. plan-feature Step 2.5 dynamically discovers project issue types via `jira.get_project_issue_types()` and maps them by `hierarchyLevel`: level 0 = Task, level 1 = Epic, level 2+ = Feature.
2. In Step 6a (plan-feature/SKILL.md, line 1019-1058), when creating tasks, the skill should use the Task type (hierarchyLevel 0, ID 10050 in this project's custom scheme).
3. The bug indicates the created issue uses the Feature issue type (ID 10142) instead of the Task type (ID 10050).

**Divergence point**: The task creation logic in Step 6a is reading the Feature issue type ID from the Jira Configuration section of CLAUDE.md (which stores Feature issue type ID: 10142) instead of using the dynamically discovered Task type from the Step 2.5 type-to-role mapping.

## Step 3 -- Codebase Investigation

### Affected Module 1: Convention Formatter

**File**: `plugins/sdlc-workflow/shared/convention-applicability-rules.md`

This shared module defines how convention section references are formatted in Implementation Notes. The prescribed format (line 57) is:

```
Per CONVENTIONS.md <Section Name>: <action required>.
```

The examples on lines 64 and 87 confirm that `<Section Name>` should preserve the original heading text verbatim (e.g., `Migration Patterns`, not `migration-patterns`).

The bug manifests when the agent constructs the section reference: instead of copying the heading text as-is from CONVENTIONS.md, it transforms it to kebab-case. This is a formatting/normalization error in the convention reference generation logic.

### Affected Module 2: Task Creation in plan-feature

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (Step 6a, lines 1019-1058)

The task creation sub-step instructs `jira.create_issue` to be called for each task. The issue type should come from the type-to-role mapping built in Step 2.5 (where Task = hierarchyLevel 0). The bug indicates the creation call is using the Feature issue type ID (10142) from the static `Jira Configuration` section instead of the Task type ID (10050) from the dynamic mapping.

The relevant mapping is defined at lines 407-412:

```
Type-to-role mapping:
  Feature: <type-name> (ID: <type-id>, level: <level>)
  Epic:    <type-name> (ID: <type-id>, level: 1)
  Task:    <type-name> (ID: <type-id>, level: 0)
```

Step 6a should reference the Task role from this mapping when creating implementation tasks, but the logic incorrectly falls back to the Feature issue type ID from CLAUDE.md's Jira Configuration.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention reference formatting (shared/convention-applicability-rules.md)

- **What is broken**: Convention section references in task Implementation Notes use kebab-case slug format (`migration-patterns`) instead of the original heading text (`Migration Patterns`).
- **Why it is broken**: The convention reference formatter normalizes section headings to kebab-case (lowercasing and replacing spaces with hyphens) rather than preserving the verbatim heading text from CONVENTIONS.md. The shared/convention-applicability-rules.md clearly specifies using `<Section Name>` which is the original heading, but the implementation transforms it.
- **Where it is broken**: `plugins/sdlc-workflow/shared/convention-applicability-rules.md` -- the convention reference formatting logic that constructs `Per CONVENTIONS.md <Section Name>` strings.
- **How to verify**: Create a CONVENTIONS.md with a section `## Migration Patterns`, run `/plan-feature`, and assert that the generated task's Implementation Notes contain `Per CONVENTIONS.md Migration Patterns:` (title case), not `Per CONVENTIONS.md migration-patterns:` (kebab-case).

### Root Cause 2: Task creation uses wrong issue type (plan-feature/SKILL.md Step 6a)

- **What is broken**: Tasks are created with the Feature issue type (ID 10142) instead of the Task issue type (ID 10050) in projects with custom issue type schemes.
- **Why it is broken**: The task creation logic in Step 6a reads the Feature issue type ID from the static Jira Configuration in CLAUDE.md rather than using the Task role from the dynamic type-to-role mapping built in Step 2.5. When the project has a custom issue type scheme where Task has a non-default ID, this mismatch causes the wrong type to be used.
- **Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a (lines 1019-1058) -- the `jira.create_issue` call that creates implementation tasks.
- **How to verify**: Configure a project with a custom issue type scheme where Task has ID 10050. Run `/plan-feature` and assert that the created issues have `issuetype.id` equal to the Task type ID (10050) from the dynamic mapping, not the Feature type ID (10142) from CLAUDE.md.

## Conclusion

These two problems have **independent root causes** in **different modules**:

1. The convention reference formatting bug is in the **shared convention utilities** (`shared/convention-applicability-rules.md`) -- a shared module consumed by multiple skills (plan-feature, verify-pr).
2. The wrong issue type bug is in the **plan-feature task creation logic** (`plan-feature/SKILL.md` Step 6a) -- specific to the plan-feature skill's Jira issue creation.

The two code paths do not interact. Fixing one does not affect the other. Each root cause should be addressed by a separate fix task to maintain proper scoping and testability.
