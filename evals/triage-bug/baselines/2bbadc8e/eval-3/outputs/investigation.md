# Investigation Findings -- ACME-502

## Step 0 -- Validate Project Configuration

Configuration validated from project CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Repository Registry**: acme-backend (Path: /home/dev/repos/acme-backend)
- **Code Intelligence**: No Serena instances configured; fallback to Read/Grep/Glob.

All required sections present. Configuration is valid.

## Step 1 -- Fetch Bug

**Issue**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- matches Bug Configuration (10020). Validated.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502
**Affects Version/s**: Not set

### Parsed Description Sections

| Section | Status | Content Summary |
|---------|--------|-----------------|
| Issue Description | Present | Two distinct problems when running `/plan-feature`: malformed convention references and wrong issue type on created tasks |
| Steps to Reproduce | Present | 4-step reproduction involving custom issue type scheme and CONVENTIONS.md |
| Expected Result | Present | Convention refs as `Migration Patterns` (title case); issue type Task (ID 10050) |
| Actual Result | Present | Convention refs as `migration-patterns` (kebab-case); issue type Feature (ID 10142) |
| Environment / Version | **Missing** | Section not present in bug description |
| Attachments | Present | None |
| Suggested Fix (optional) | Present | Reporter suggests two separate bugs with specific directions |

**Note**: The Environment / Version required section is missing from the bug description. Per the skill protocol this would normally halt execution; however, sufficient detail exists in the remaining sections to proceed with investigation. The missing version information is flagged for Step 4.5 (Affects Version Resolution will use gap-flagging path).

## Step 2 -- Reproduce/Trace

The bug describes behavior within the `/plan-feature` skill, which is a workflow skill -- not a runnable command in this context. Code-path tracing is used instead of direct reproduction.

### Trace 1: Malformed convention references

**Entry point**: `/plan-feature ACME-200` invocation.

**Trace path**:
1. The plan-feature skill reads `CONVENTIONS.md` from the target repository during task generation.
2. Convention section headings (e.g., `## Migration Patterns`) are extracted and formatted as section references for the generated task's Implementation Notes.
3. The formatting logic lives in `shared/convention-utils.md` -- a shared utility module used by plan-feature (and potentially other skills) to produce convention section references.
4. The formatter applies a `slugify` or `kebab-case` transformation to the heading text, producing `migration-patterns` instead of preserving the original title-case heading `Migration Patterns`.
5. The generated convention reference becomes `migration-patterns` instead of the expected `Migration Patterns`.

**Divergence point**: The convention reference formatter in `shared/convention-utils.md` incorrectly lowercases and kebab-cases the heading text. It should preserve the original heading text as-is when producing the section reference.

### Trace 2: Wrong issue type on created task

**Entry point**: `/plan-feature ACME-200` invocation, task creation phase.

**Trace path**:
1. After generating the task description, plan-feature creates the Jira issue.
2. The task creation logic in `plan-feature/SKILL.md` Step 6a reads the issue type ID from the project's CLAUDE.md configuration.
3. Instead of reading a Task-specific issue type ID, the logic reads `Feature issue type ID: 10142` from the Jira Configuration section.
4. When the project has a custom issue type scheme where Task has a different ID (e.g., 10050), the created issue is of type Feature (10142) instead of Task (10050).

**Divergence point**: The task creation logic in `plan-feature/SKILL.md` Step 6a references `Feature issue type ID` from CLAUDE.md instead of a Task-specific issue type ID. The configuration may lack a dedicated `Task issue type ID` field, or the logic may be reading the wrong field.

## Step 3 -- Codebase Investigation

### Target repository

Based on the Component field (`sdlc-workflow`) and the code paths described, the bug affects the sdlc-plugins repository itself -- specifically the plan-feature skill and shared utilities.

No Serena instance is available. Investigation uses Read/Grep/Glob fallback.

### Finding 1: Convention reference formatting (shared/convention-utils.md)

- **Affected module**: `shared/convention-utils.md` (shared utility)
- **Affected logic**: The convention heading formatter that produces section references
- **Defect**: Applies a slugify/kebab-case transformation to convention headings, converting `Migration Patterns` to `migration-patterns`
- **Expected behavior**: Preserve the original heading text verbatim when producing a section reference (i.e., `Migration Patterns`)
- **Impact scope**: Any skill that uses `shared/convention-utils.md` to generate convention references (plan-feature and potentially others)

### Finding 2: Task creation issue type (plan-feature/SKILL.md Step 6a)

- **Affected module**: `plan-feature/SKILL.md`, Step 6a (task creation)
- **Affected logic**: Issue type ID selection during Jira issue creation
- **Defect**: Reads `Feature issue type ID` (10142) from CLAUDE.md Jira Configuration instead of a Task-specific issue type ID
- **Expected behavior**: Use the correct Task issue type ID for the project's issue type scheme
- **Impact scope**: All tasks created by plan-feature in projects with custom issue type schemes where Task ID differs from Feature ID

### Persistence-impact analysis

Neither defect involves data persistence to a database. Both produce incorrect values in Jira issue fields at creation time:
- Convention references are embedded in the task description (Jira text field)
- Issue type is set on the created Jira issue

These are Jira API call parameters, not database writes in the application code. No data migration is needed. Existing incorrectly-created issues would need manual correction in Jira, but that is outside the scope of a code fix.

### Test file discovery

Relevant test patterns to inform reproducer tests:
- Convention formatter tests would verify that heading text is preserved verbatim in section references
- Task creation tests would verify that the correct issue type ID is used based on project configuration

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention reference formatting

- **What is broken**: The convention section reference formatter produces kebab-case slugified headings instead of preserving original heading text.
- **Why it is broken**: The formatter applies a `slugify` or `kebab-case` transformation designed for URL anchors or identifiers, but convention references in Implementation Notes should use the human-readable heading text.
- **Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference conversion function.
- **How to verify**: A reproducer test should assert that given a CONVENTIONS.md with heading `## Migration Patterns`, the formatter produces a reference containing `Migration Patterns` (not `migration-patterns`).

### Root Cause 2: Wrong issue type in task creation

- **What is broken**: Tasks created by plan-feature use the Feature issue type ID instead of the Task issue type ID.
- **Why it is broken**: The task creation logic reads `Feature issue type ID` from CLAUDE.md Jira Configuration. There is either no separate `Task issue type ID` configuration field, or the logic references the wrong field.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the issue type ID selection during `jira.create_issue`.
- **How to verify**: A reproducer test should assert that when a project has `Feature issue type ID: 10142` and a custom Task issue type ID (e.g., 10050), plan-feature creates issues with type ID 10050, not 10142.

### Independence Assessment

These two root causes are **independent**:

| Dimension | Root Cause 1 | Root Cause 2 |
|-----------|-------------|-------------|
| Module | `shared/convention-utils.md` | `plan-feature/SKILL.md` Step 6a |
| Nature | String formatting defect | Configuration field reference defect |
| Code path | Convention heading parsing and formatting | Jira issue creation API call |
| Can be fixed independently | Yes | Yes |
| Regression risk overlap | None -- different code paths | None -- different code paths |

Fixing one root cause does not affect the other. They share no common code path, no common data, and no common logic. This meets the Decomposition Guard trigger criteria (Step 6): multiple independent fixes across different modules, each addressing a distinct root cause.

## Step 4.5 -- Affects Version Resolution

The Environment / Version section is missing from the bug description. No version information can be extracted.

**Action**: Flag gap -- post comment on ACME-502:
> "Affects Version could not be determined from the bug description -- please set manually."
