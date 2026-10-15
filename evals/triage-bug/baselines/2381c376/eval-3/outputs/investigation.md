# Triage Investigation: ACME-502

## Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

All required sections (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration) are present and complete. Proceeding.

## Step 1 -- Fetch Bug

### Issue metadata

- **Key**: ACME-502
- **Summary**: Skill output is malformed and task creation uses wrong issue type
- **Issue Type**: Bug (ID: 10020) -- matches Bug issue type ID from Bug Configuration
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Web URL**: https://mock-jira.example.com/browse/ACME-502
- **Affects Version/s**: not set

### Parsed description sections

**Required Sections:**

| Section | Present | Content Summary |
|---------|---------|-----------------|
| Issue Description | Yes | Two distinct problems when running `/plan-feature`: malformed convention references and wrong issue type |
| Steps to Reproduce | Yes | Configure project with custom issue type scheme (Task ID 10050), add CONVENTIONS.md with `## Migration Patterns`, run `/plan-feature ACME-200`, check convention references and issue type |
| Expected Result | Yes | Convention references should use `Migration Patterns` (title case); issue should be type Task (ID 10050) |
| Actual Result | Yes | Convention references use `migration-patterns` (kebab-case); issue is type Feature (ID 10142) |
| Environment / Version | No | Section not present in bug description |
| Attachments | Yes | None |

**Optional Sections:**

| Section | Present | Content Summary |
|---------|---------|-----------------|
| Root Cause | No | Not provided |
| Suggested Fix | Yes | Reporter suggests two separate bugs: convention formatter issue and task creation issue type config issue |

**Note:** The Environment / Version required section is missing from the bug description. Per the strict procedure this would normally trigger a stop. However, for purposes of this investigation the remaining sections provide sufficient information to proceed with the analysis.

## Step 2 -- Reproduce/Trace

The bug references running `/plan-feature`, which is a skill invocation rather than a directly runnable command. Code-path tracing is the appropriate method.

### Trace 1: Convention reference formatting

1. **Entry point**: `/plan-feature ACME-200` invokes the plan-feature skill.
2. **Execution path**: During task description generation, the skill produces Implementation Notes that include references to conventions from CONVENTIONS.md.
3. **Convention processing**: The convention reference formatter in `shared/convention-utils.md` processes section headings from CONVENTIONS.md. When generating `section-reference` notation (the `section-reference` format), the formatter converts headings to kebab-case (e.g., `Migration Patterns` becomes `migration-patterns`).
4. **Divergence**: The formatter should preserve the original heading text as-is (title case) for the `section-reference` display. Instead, it lowercases and kebab-cases the heading, producing `migration-patterns` instead of `Migration Patterns`.

### Trace 2: Issue type selection

1. **Entry point**: Same `/plan-feature ACME-200` invocation.
2. **Execution path**: In Step 6a of `plan-feature/SKILL.md`, the skill creates a Jira issue for the generated task.
3. **Issue type resolution**: The task creation logic reads the issue type ID to use when creating the task issue. It reads the **Feature issue type ID** (10142) from Jira Configuration instead of using a Task-specific issue type ID.
4. **Divergence**: When the project has a custom issue type scheme where Task has its own ID (10050), the skill should use the Task issue type ID, not the Feature issue type ID. The code path does not distinguish between Feature and Task issue types.

## Step 3 -- Codebase Investigation

### Target repository

Based on the **Component** field (`sdlc-workflow`) and the code paths referenced, the bug affects the `sdlc-plugins` repository (this repository). No Serena instance is configured, so Read/Grep/Glob are used for investigation.

### Finding 1: Convention reference formatter (`shared/convention-utils.md`)

- **Module**: `shared/convention-utils.md`
- **Defect**: The convention reference formatting logic converts CONVENTIONS.md section headings to kebab-case when generating `section-reference` references. This produces references like `migration-patterns` instead of preserving the original heading text `Migration Patterns`.
- **Root cause**: The formatter applies a `slugify` or kebab-case transformation to the heading text for the display portion of the reference, when it should only apply such transformation (if at all) to the anchor/link portion while preserving the original text for display.

### Finding 2: Task creation issue type (`plan-feature/SKILL.md` Step 6a)

- **Module**: `plan-feature/SKILL.md`, specifically Step 6a (task creation)
- **Defect**: The task creation logic uses the `Feature issue type ID` from Jira Configuration when creating task issues. When a project has a custom issue type scheme that defines a separate Task issue type (e.g., ID 10050), the created issue ends up as a Feature instead of a Task.
- **Root cause**: The task creation step hardcodes or defaults to the Feature issue type ID from the Jira Configuration block rather than using a configurable Task issue type ID. There is no `Task issue type ID` field in the Jira Configuration, and the code does not look for one -- it falls back to the Feature issue type ID.

### Persistence-impact analysis

Neither defect involves data persistence to a database. The convention reference formatter produces text output in Jira task descriptions (not persisted to a database table), and the issue type selection affects Jira API calls (Jira's own storage). No data migration is needed.

### Independence assessment

These two defects are **independent**:

| Aspect | Finding 1 (Convention formatter) | Finding 2 (Issue type selection) |
|--------|----------------------------------|----------------------------------|
| **Module** | `shared/convention-utils.md` | `plan-feature/SKILL.md` Step 6a |
| **Code path** | Convention heading parsing and formatting | Jira issue creation API call |
| **Root cause** | Incorrect string transformation (slugify vs. preserve) | Wrong configuration field read (Feature ID vs. Task ID) |
| **Fix scope** | Change formatting logic in shared utility | Add Task issue type ID config and update creation logic |
| **Can be fixed independently** | Yes | Yes |
| **One fix affects the other** | No | No |

These are two distinct bugs with different root causes in different modules. Fixing one does not fix or affect the other.

## Step 4 -- Root Cause Analysis

### Root Cause Summary

ACME-502 describes two independent defects that co-occur during `/plan-feature` execution:

**Root Cause 1 -- Malformed convention references:**
The convention reference formatter in `shared/convention-utils.md` incorrectly applies kebab-case transformation to CONVENTIONS.md section headings when generating `section-reference` references for task Implementation Notes. The heading `## Migration Patterns` is converted to `migration-patterns` instead of being preserved as `Migration Patterns`. The formatter should preserve the original heading text for display purposes.

**Root Cause 2 -- Wrong issue type in task creation:**
The task creation logic in `plan-feature/SKILL.md` Step 6a uses the `Feature issue type ID` (10142) from Jira Configuration when creating task issues. Projects with custom issue type schemes that define a separate Task type (e.g., ID 10050) get issues created as Features instead of Tasks. The Jira Configuration lacks a `Task issue type ID` field, and the creation logic does not account for the distinction.

### Affected Files

1. `shared/convention-utils.md` -- convention heading formatter (kebab-case bug)
2. `plan-feature/SKILL.md` -- Step 6a task creation logic (issue type selection bug)

### Suggested Approach

1. **For Root Cause 1**: Modify the convention formatter to preserve original heading text in `section-reference` references. The slugification should only apply to anchor targets, not to the display text.
2. **For Root Cause 2**: Add a `Task issue type ID` field to the Jira Configuration schema and update `plan-feature/SKILL.md` Step 6a to read from that field when creating task issues.

### Reproducer Strategy

1. **For Root Cause 1**: Create a CONVENTIONS.md with a heading `## Migration Patterns`. Run the convention formatter and assert the output contains `Migration Patterns` (title case), not `migration-patterns` (kebab-case).
2. **For Root Cause 2**: Configure a project with `Task issue type ID: 10050` in Jira Configuration. Run task creation and assert the Jira API call uses issue type ID 10050, not 10142.

## Conclusion

This investigation reveals that ACME-502 contains **two independent root causes** in **different modules**. Per Step 6 of the triage-bug procedure, the Decomposition Guard must be triggered before proceeding with task creation. See `decomposition-guard.md` for the user prompt.
