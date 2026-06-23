# Investigation — ACME-502

## Step 0 — Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections are present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration. Validation passed.

## Step 1 — Fetch Bug

### Issue type validation

Issue ACME-502 has `issuetype.id = 10020`, which matches the Bug issue type ID from Bug Configuration (10020). Validation passed.

### Parsed bug description

**Required Sections** (all present, matched against bug template headings):

- **Description**: Two distinct problems occur when running `/plan-feature`: (1) the generated task description has malformed Implementation Notes — convention references use the wrong section heading format (e.g., `§migration-patterns` instead of `§Migration Patterns`); (2) the task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.
- **Steps to Reproduce**: (1) Configure a project with a custom issue type scheme where Task has ID 10050. (2) Add a `CONVENTIONS.md` with section `## Migration Patterns`. (3) Run `/plan-feature ACME-200`. (4) Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.
- **Expected Result**: Implementation Notes should reference conventions as `§Migration Patterns` (title case, matching the heading). The created issue should be of type Task (ID 10050).
- **Actual Result**: Implementation Notes reference conventions as `§migration-patterns` (kebab-case, not matching the heading). The created issue is of type Feature (ID 10142) instead of Task.

**Optional Sections**:

- **Attachments**: None.
- **Suggested Fix**: Two separate bugs suspected — the convention reference formatter lowercases and kebab-cases headings incorrectly, and the task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

### Metadata

- **Issue key**: ACME-502
- **Web URL**: https://mock-jira.example.com/browse/ACME-502
- **Summary**: Skill output is malformed and task creation uses wrong issue type
- **Labels**: reported-by-user
- **Component**: sdlc-workflow

## Step 2 — Reproduce/Trace

These are skill-level bugs in the sdlc-workflow plugin, so direct reproduction via runnable commands is not applicable. Code-path tracing was used instead.

### Trace 1 — Convention reference formatting

Entry point: `/plan-feature` skill invocation, specifically the convention-aware task enrichment in Step 5.

The plan-feature skill (Step 5, "Convention-aware task enrichment") reads conventions from a project's CONVENTIONS.md and includes them in task Implementation Notes using the format defined in `shared/convention-applicability-rules.md`:

```
Per CONVENTIONS.md §<Section Name>: <specific action required>.
Applies: task modifies <matching file(s)> matching the convention's <scope signal>.
```

The section name in the `§` reference should preserve the original heading text from CONVENTIONS.md verbatim (e.g., `§Migration Patterns`).

The bug reports that convention references are emitted as `§migration-patterns` (kebab-case slug) instead of `§Migration Patterns` (original title-case heading). This indicates that the convention reference formatter — the logic in `shared/convention-utils.md` (the shared utility responsible for formatting convention section references) — is applying a kebab-case/slug transformation to the heading text before inserting it into the `§` reference. The formatter should preserve the original heading text verbatim.

**Divergence point**: The convention reference formatter in `shared/convention-utils.md` lowercases and kebab-cases the CONVENTIONS.md heading text when producing the `§` reference, instead of preserving the heading as-is.

### Trace 2 — Issue type selection during task creation

Entry point: `/plan-feature` skill invocation, Step 6a (Create the tasks).

In Step 6a, `jira.create_issue` is called to create tasks. The issue type for created tasks should be "Task" (the level-0 issue type from Step 2.5's hierarchy mapping). However, the bug reports that the created issue has type Feature (ID 10142) instead of Task.

Examining the Jira Configuration in CLAUDE.md, the only issue type ID explicitly configured is `Feature issue type ID: 10142`. There is no `Task issue type ID` field defined. Step 2.5 of plan-feature dynamically discovers issue types by fetching `jira.get_project_issue_types(cloudId, projectKey)` and mapping them by `hierarchyLevel` (level 0 = Task, level 1 = Epic, level 2+ = Feature). However, the task creation logic in Step 6a appears to fall back to the Feature issue type ID (10142) from the Jira Configuration when the dynamic discovery fails or when no Task issue type is found, causing created issues to have the wrong type in projects with custom issue type schemes where Task has a different ID (10050 in this case).

**Divergence point**: The task creation logic in `plan-feature/SKILL.md` Step 6a falls back to the Feature issue type ID (10142) from Jira Configuration instead of correctly using the Task issue type ID discovered in Step 2.5, when the project uses a custom issue type scheme.

## Step 3 — Codebase Investigation

### Target repository

The component is `sdlc-workflow`, which maps to the sdlc-plugins repository (path: `./`). No Serena instance is configured for this repository, so Read/Grep/Glob were used as fallback.

### Affected files and modules

**Root Cause 1 — Convention reference formatting**:
- **Primary file**: `shared/convention-utils.md` — the shared utility that formats convention section references for task descriptions. Contains the logic that transforms heading text into the `§<name>` reference format.
- **Related**: `shared/convention-applicability-rules.md` — defines the canonical `§<Section Name>` format that should be used, with examples showing title-case preservation (e.g., `§Migration Patterns`).
- **Related**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 5 — "Convention-aware task enrichment" consumes the formatter output and includes convention references in task Implementation Notes.

**Root Cause 2 — Wrong issue type**:
- **Primary file**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a — task creation logic that calls `jira.create_issue`. The issue type passed to the create call is determined here.
- **Related**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 2.5 — "Discover Project Issue Types" is responsible for dynamically mapping hierarchy levels to issue type IDs, but its output is not correctly consumed by Step 6a.
- **Related**: Project CLAUDE.md Jira Configuration — defines `Feature issue type ID: 10142` but does not define a `Task issue type ID`, which may contribute to the fallback behavior.

### Independence assessment

These two root causes are in **different modules** and affect **different code paths**:

- Root Cause 1 is in the shared convention formatting utilities (`shared/convention-utils.md`), invoked during task description generation (Step 5 of plan-feature).
- Root Cause 2 is in the plan-feature task creation logic (`plan-feature/SKILL.md` Step 6a), invoked during Jira issue creation (Step 6 of plan-feature).

They operate at different stages of the plan-feature workflow (description generation vs. Jira API call), involve different modules (shared utility vs. skill-specific logic), and neither fix depends on or affects the other. They are independently reproducible, independently testable, and independently fixable. This qualifies as a multi-root-cause scenario that triggers the Decomposition Guard (Step 6).

## Step 4 — Root Cause Analysis

### Root Cause 1: Convention reference formatter uses kebab-case instead of preserving heading text

- **What is broken**: The convention reference formatter transforms CONVENTIONS.md section headings into kebab-case slugs (e.g., `Migration Patterns` becomes `migration-patterns`) before inserting them into `§` references in task Implementation Notes.
- **Why it is broken**: The formatter applies a slug/kebab-case transformation (lowercase + hyphenate spaces) to the heading text, likely intended for anchor links or URL fragments. However, the `§<Section Name>` format defined in `shared/convention-applicability-rules.md` is meant for human-readable references and should preserve the original heading text verbatim.
- **Where it is broken**: `shared/convention-utils.md` — the convention section name formatting logic that produces the `§` reference string.
- **How to verify the fix**: A reproducer test should provide a CONVENTIONS.md with a heading like `## Migration Patterns`, invoke the convention formatter, and assert that the output contains `§Migration Patterns` (title case, matching the original heading) — not `§migration-patterns` (kebab-case slug).

### Root Cause 2: Task creation uses Feature issue type ID instead of Task issue type ID

- **What is broken**: When `/plan-feature` creates Jira tasks in Step 6a, the created issues have issue type "Feature" (ID 10142) instead of "Task".
- **Why it is broken**: The Jira Configuration in CLAUDE.md only defines `Feature issue type ID: 10142`. There is no `Task issue type ID` field. Step 2.5 is designed to dynamically discover issue types by `hierarchyLevel`, but the task creation logic in Step 6a falls back to the Feature issue type ID when dynamic discovery does not yield a Task type, or fails to use the discovered Task type ID correctly.
- **Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a — the task creation call that determines which issue type ID to pass to `jira.create_issue`.
- **How to verify the fix**: A reproducer test should configure a project with a custom issue type scheme where Task has ID 10050 (different from Feature ID 10142), run plan-feature task creation, and assert that the created issue has `issuetype.id = 10050` (not 10142).

### Summary

| # | Root Cause | Module | Code Path |
|---|-----------|--------|-----------|
| 1 | Convention formatter kebab-cases headings instead of preserving original heading text | `shared/convention-utils.md` | Task description generation (plan-feature Step 5) |
| 2 | Task creation reads Feature issue type ID instead of dynamically discovered Task issue type ID | `plan-feature/SKILL.md` Step 6a | Jira issue creation (plan-feature Step 6) |

These are **two independent root causes** in different modules affecting different execution stages of the plan-feature workflow. Fixing one does not fix the other, and neither depends on the other. This triggers the Decomposition Guard (Step 6).
