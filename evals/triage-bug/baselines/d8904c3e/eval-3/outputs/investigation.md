# Triage Investigation: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Component**: sdlc-workflow

## Parsed Bug Description

### Issue Description

Two distinct problems occur when running `/plan-feature`:
1. The generated task description has malformed Implementation Notes -- convention references use the wrong section heading format (e.g., `§migration-patterns` instead of `§Migration Patterns`).
2. The task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

### Steps to Reproduce

1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

### Expected Result

- Implementation Notes should reference conventions as `§Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

### Actual Result

- Implementation Notes reference conventions as `§migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

### Environment / Version

Not provided in the bug description.

## Codebase Investigation

### Target Repository

The bug affects the `sdlc-plugins` repository (component: sdlc-workflow). No Serena instance is configured; investigation uses Read, Grep, and Glob tools directly.

### Root Cause 1: Malformed Convention References

**Affected module**: `plugins/sdlc-workflow/shared/convention-applicability-rules.md` (the convention formatting/applicability module)

**What is broken**: The convention reference formatter that generates `§<Section Name>` references in task Implementation Notes lowercases and kebab-cases CONVENTIONS.md section headings instead of preserving the original title case. When a CONVENTIONS.md has `## Migration Patterns`, the formatter produces `§migration-patterns` instead of `§Migration Patterns`.

**Why it is broken**: The convention reference formatting logic applies a slug/kebab-case transformation to section headings before inserting them into the `Per CONVENTIONS.md §<Section Name>: ...` pattern. The prescribed format in `shared/convention-applicability-rules.md` (lines 57-58) clearly specifies that the section name should match the original heading:

```
Per CONVENTIONS.md §<Section Name>: <action required>.
```

The examples in the same file (line 64) confirm the expected format:

```
Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.
```

The `plan-feature/SKILL.md` Step 5 "Convention-aware task enrichment" section (line 803) also prescribes:

```
"Per CONVENTIONS.md §<Section Name>: <specific action required>"
```

The formatter incorrectly normalizes the heading to kebab-case (`migration-patterns`) instead of preserving the original heading text (`Migration Patterns`).

**Where it is broken**: The convention reference formatting logic resides in `plugins/sdlc-workflow/shared/convention-applicability-rules.md`, which defines how convention references should be formatted. The bug is in the runtime application of this formatting -- the section heading extraction step converts headings to slugs rather than preserving the original text from the `## <Heading>` line in CONVENTIONS.md.

**Affected files and symbols**:
- `plugins/sdlc-workflow/shared/convention-applicability-rules.md` -- the convention applicability rules that define the `§<Section Name>` format
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (Step 5, "Convention-aware task enrichment") -- the consumer that applies convention references using this format

**Persistence impact**: None. Convention references are generated at task creation time and written to Jira task descriptions. The output is persisted to Jira, but fixing the formatter will correct future tasks. Existing tasks with malformed references would need manual correction in Jira, but no database migration is required -- this is a Jira content issue, not a database schema issue.

### Root Cause 2: Wrong Issue Type in Task Creation

**Affected module**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a (task creation logic)

**What is broken**: When creating tasks in Jira, the task creation logic in Step 6a uses the Feature issue type ID (10142) from CLAUDE.md's `## Jira Configuration` instead of the Task issue type ID (10050) that was dynamically discovered in Step 2.5.

**Why it is broken**: Step 2.5 ("Discover Project Issue Types") correctly discovers the project's issue types and maps them to hierarchy roles, identifying the level-0 type as "Task" with its project-specific ID. However, Step 6a's `jira.create_issue` call does not use the Task type ID from the Step 2.5 mapping. Instead, it reads the `Feature issue type ID` field from `## Jira Configuration` in CLAUDE.md (which is 10142) and uses that as the issue type for created tasks.

The type-to-role mapping from Step 2.5 stores:
```
Task: <type-name> (ID: <type-id>, level: 0)
```

But Step 6a does not reference this mapping when constructing the `create_issue` call. In projects with custom issue type schemes where the Task type has a non-default ID (e.g., 10050), the Feature type ID (10142) is used instead, causing created issues to be of type "Feature" rather than "Task".

**Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a ("Create the tasks"), specifically the issue type selection in the `jira.create_issue` call.

**Affected files and symbols**:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (Step 6a) -- the task creation logic that should use the dynamically discovered Task type ID from Step 2.5 but instead uses the Feature issue type ID from Jira Configuration

**Persistence impact**: None directly in the codebase. Created Jira issues have the wrong type, but this is correctable in Jira by changing the issue type after creation. No database migration is needed.

## Root Cause Analysis Summary

This bug involves **two independent root causes** in **different modules**:

| # | Root Cause | Module | File |
|---|-----------|--------|------|
| 1 | Convention reference formatter kebab-cases section headings instead of preserving original title case | Convention formatting (shared) | `plugins/sdlc-workflow/shared/convention-applicability-rules.md` |
| 2 | Task creation uses Feature issue type ID from config instead of dynamically discovered Task type ID | Task creation (plan-feature) | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a |

These two root causes are **independent**: they affect different code paths (convention formatting vs. issue type selection), different modules (`shared/convention-applicability-rules.md` vs. `plan-feature/SKILL.md`), and can be fixed independently without affecting each other.

### Reproducer Strategy

**For Root Cause 1 (convention references)**:
- Create a CONVENTIONS.md with a multi-word section heading (e.g., `## Migration Patterns`)
- Run plan-feature to generate tasks
- Assert that Implementation Notes contain `§Migration Patterns` (title case) and NOT `§migration-patterns` (kebab-case)

**For Root Cause 2 (issue type)**:
- Configure a project with a custom issue type scheme where Task has a non-default ID (e.g., 10050)
- Run plan-feature to generate tasks
- Assert that the created issue has issue type ID matching the Task role from Step 2.5 discovery (10050), not the Feature issue type ID from Jira Configuration (10142)
