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

**Required Sections** (all present, matched against heading formats from bug-template-mock.md):

- **Description** (`### **Issue Description**`): Two distinct problems occur when running `/plan-feature`: (1) the generated task description has malformed Implementation Notes where convention references use the wrong section heading format (e.g., `§migration-patterns` instead of `§Migration Patterns`), and (2) the task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.
- **Steps to Reproduce** (`### **Steps to Reproduce**`): Configure a project with a custom issue type scheme where Task has ID 10050. Add a `CONVENTIONS.md` with section `## Migration Patterns`. Run `/plan-feature ACME-200`. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.
- **Expected Result** (`### **Expected Result**`): Implementation Notes should reference conventions as `§Migration Patterns` (title case, matching the heading). The created issue should be of type Task (ID 10050).
- **Actual Result** (`### **Actual Result**`): Implementation Notes reference conventions as `§migration-patterns` (kebab-case, not matching the heading). The created issue is of type Feature (ID 10142) instead of Task.

**Optional Sections**:

- **Attachments**: None.
- **Suggested Fix**: These are likely two separate bugs — the convention reference formatter lowercases and kebab-cases headings incorrectly, and the task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

### Metadata

- **Issue key**: ACME-502
- **Web URL**: https://mock-jira.example.com/browse/ACME-502
- **Summary**: Skill output is malformed and task creation uses wrong issue type
- **Labels**: reported-by-user
- **Component**: sdlc-workflow

## Step 2 — Reproduce/Trace

These are skill-level bugs in the sdlc-workflow plugin, not runnable application code. Direct reproduction via executable commands is not applicable. Code-path tracing was used instead.

### Trace 1 — Convention reference formatting

Entry point: `/plan-feature` skill invocation, specifically the convention-aware task enrichment in Step 5.

The plan-feature skill (Step 5, "Convention-aware task enrichment") reads conventions from CONVENTIONS.md and includes them in task Implementation Notes using the format:

```
Per CONVENTIONS.md §<Section Name>: <specific action required>
```

The convention applicability rules in `shared/convention-applicability-rules.md` also prescribe this format with `§<Section Name>`, where the section name should preserve the original heading text from CONVENTIONS.md verbatim (e.g., `§Migration Patterns`).

The bug reports that convention references are emitted as `§migration-patterns` (kebab-case slug) instead of `§Migration Patterns` (original title case heading). This indicates that the convention reference formatter in `shared/convention-utils.md` — the shared utility responsible for formatting convention section references — is applying a kebab-case transformation (lowercase + hyphenate) to the heading text before inserting it into the `§` reference. The formatter should preserve the original heading text as-is.

**Divergence point**: The convention reference formatter converts CONVENTIONS.md heading text to kebab-case instead of preserving the original title case.

### Trace 2 — Issue type selection during task creation

Entry point: `/plan-feature` skill invocation, Step 6a (Create the tasks).

In Step 6a, `jira.create_issue` is called to create tasks in Jira. The issue type for created tasks should be "Task". However, the bug reports that the created issue has type Feature (ID 10142) instead of Task.

Examining the Jira Configuration in CLAUDE.md, the only issue type ID configured is `Feature issue type ID: 10142`. There is no `Task issue type ID` field. The plan-feature SKILL.md Step 2.5 ("Discover Project Issue Types") dynamically discovers issue types by hierarchy level, mapping level-0 types to the Task role. However, the task creation logic in Step 6a appears to fall back to the Feature issue type ID (10142) from the Jira Configuration when the dynamic discovery does not produce a Task type ID, or when the discovered mapping is not correctly propagated to the creation call.

When the project has a custom issue type scheme where Task has a distinct ID (10050 in this case), the wrong ID is used — the creation logic defaults to the statically configured Feature issue type ID (10142) instead of the dynamically discovered Task issue type ID (10050).

**Divergence point**: The task creation logic in `plan-feature/SKILL.md` Step 6a uses the Feature issue type ID (10142) from Jira Configuration instead of using the Task issue type ID (10050) discovered via Step 2.5 or configured in the project.

## Step 3 — Codebase Investigation

### Target repository

The component is `sdlc-workflow`, which maps to the sdlc-plugins repository (path: `./`). No Serena instance is configured for this repository, so Read/Grep/Glob tools were used for investigation.

### Affected files and modules

**Root Cause 1 — Convention reference formatting**:
- **File**: `shared/convention-utils.md` — the shared utility that formats convention section references for use in task descriptions
- **Related**: `shared/convention-applicability-rules.md` — defines the `§<Section Name>` format that convention references should follow
- **Related**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 5 — "Convention-aware task enrichment" consumes the formatter output and embeds convention references in task Implementation Notes

**Root Cause 2 — Wrong issue type in task creation**:
- **File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a — the task creation logic that calls `jira.create_issue` and determines which issue type ID to pass
- **Related**: Project CLAUDE.md `## Jira Configuration` — only defines `Feature issue type ID: 10142`, does not define a separate `Task issue type ID`
- **Related**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 2.5 — "Discover Project Issue Types" dynamically maps hierarchy levels to issue type roles, but the mapping may not be correctly consumed by Step 6a

### Independence assessment

These two root causes are in **different modules** and affect **different code paths**:

- Root Cause 1 is in the shared convention formatting utilities (`shared/convention-utils.md`), invoked during task description generation (Step 5).
- Root Cause 2 is in the plan-feature task creation logic (`plan-feature/SKILL.md` Step 6a), invoked during Jira issue creation (Step 6).

The two code paths do not share logic, inputs, or state. A fix to one does not affect or depend on the other. They are independently reproducible, independently testable, and independently fixable.

## Step 4 — Root Cause Analysis

### Root Cause 1: Convention reference formatter uses wrong case transform (kebab-case instead of preserving title case)

- **What is broken**: The convention reference formatter transforms CONVENTIONS.md section headings into kebab-case slugs (e.g., `Migration Patterns` becomes `migration-patterns`) before inserting them into `§` references in task Implementation Notes.
- **Why it is broken**: The formatter applies a slug/kebab-case transformation (lowercase + hyphenate spaces) to the heading text, likely intended for anchor links or URL fragments. However, the `§<Section Name>` format in Implementation Notes is meant for human-readable references and should preserve the original heading text verbatim.
- **Where it is broken**: `shared/convention-utils.md` — the convention section name formatting logic.
- **How to verify the fix**: A reproducer test should provide a CONVENTIONS.md with a heading like `## Migration Patterns`, invoke the convention formatter, and assert that the output contains `§Migration Patterns` (not `§migration-patterns`).

### Root Cause 2: Task creation uses Feature issue type ID (10142) instead of Task issue type ID (10050)

- **What is broken**: When `/plan-feature` creates Jira tasks in Step 6a, the created issues have issue type "Feature" (ID 10142) instead of "Task" (ID 10050).
- **Why it is broken**: The Jira Configuration in CLAUDE.md only defines `Feature issue type ID: 10142`. There is no `Task issue type ID` field. The task creation logic in Step 6a falls back to the Feature issue type ID because it has no other configured value for Task issues. When a project uses a custom issue type scheme with a distinct Task ID (e.g., 10050), the wrong ID is used. The dynamic discovery in Step 2.5 should map level-0 types to the Task role, but the discovered mapping is not correctly consumed by the creation logic.
- **Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a — the task creation call that determines which issue type to use.
- **How to verify the fix**: A reproducer test should configure a project with a custom issue type scheme where Task has ID 10050, run plan-feature task creation, and assert that the created issue has `issuetype.id = 10050` (not 10142).

### Summary

| # | Root Cause | Module | Code Path |
|---|-----------|--------|-----------|
| 1 | Convention formatter converts headings to kebab-case instead of preserving original title case text | `shared/convention-utils.md` | Task description generation (Step 5) |
| 2 | Task creation uses Feature issue type ID (10142) instead of Task issue type ID (10050) | `plan-feature/SKILL.md` Step 6a | Jira issue creation (Step 6) |

These are **two independent root causes** in different modules affecting different execution stages. Fixing one does not fix the other, and neither depends on the other. This triggers the Decomposition Guard (Step 6).
