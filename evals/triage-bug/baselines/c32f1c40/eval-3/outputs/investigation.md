# Investigation Report: ACME-502

## Bug Summary

**Issue**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow

## Step 0 -- Validate Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020 (matches issue type on ACME-502)
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142 (from Jira Configuration)

## Step 1 -- Fetch and Parse Bug

All required sections present per the bug template:

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Attachments | Present (None) |
| Suggested Fix | Present (optional) |

### Parsed Description

**Steps to Reproduce:**
1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

**Expected Result:**
- Implementation Notes should reference conventions as `Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

**Actual Result:**
- Implementation Notes reference conventions as `migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

## Step 2 -- Code-Path Tracing

The bug involves the `/plan-feature` skill. Since this is a skill/documentation bug that affects how the skill generates output and creates Jira issues, direct reproduction is not applicable. Instead, the two reported problems were traced through the relevant code paths.

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` invocation. During Implementation Notes generation, the skill calls a convention reference formatter to produce `Per CONVENTIONS.md` section references. The formatter is responsible for converting CONVENTIONS.md section headings into the reference notation used in task descriptions.

Traced to: `shared/convention-utils.md` -- the convention reference formatting logic. The formatter applies a kebab-case transform (lowercasing and replacing spaces with hyphens) to section headings before inserting them into the `Per CONVENTIONS.md` reference. This produces `migration-patterns` instead of preserving the original title-case heading text `Migration Patterns`. The correct format, as defined in `shared/convention-applicability-rules.md`, is `Per CONVENTIONS.md §<Section Name>: <action required>` where `<Section Name>` preserves the original heading case.

### Trace 2: Task Issue Type Selection

Entry point: `/plan-feature` invocation, at the point where task issues are created in Jira. The skill reads the issue type ID from the project configuration to determine what type of Jira issue to create.

Traced to: `plan-feature/SKILL.md` Step 6a -- the task creation logic. The code reads the `Feature issue type ID` (10142) from the CLAUDE.md Jira Configuration instead of using the Task issue type ID derived from the project's issue type scheme (Step 2.5 type-to-role mapping). This causes all generated tasks to be created as Feature issues regardless of the project's actual Task issue type configuration.

## Step 3 -- Codebase Investigation

### Affected Files and Modules

| # | File / Module | Affected Symbol / Section | Issue |
|---|---------------|--------------------------|-------|
| 1 | `shared/convention-utils.md` | Convention reference formatter (case transform logic) | Applies kebab-case transform to section headings instead of preserving original title case |
| 2 | `plan-feature/SKILL.md` Step 6a | Task creation issue type selection | Reads `Feature issue type ID` (10142) instead of using the Task type from the issue type scheme |

### Related Files (context)

- `shared/convention-applicability-rules.md` -- defines the correct convention reference format (`Per CONVENTIONS.md §<Section Name>: <action required>`) which the formatter should produce
- `plan-feature/SKILL.md` Step 2.5 -- defines the type-to-role mapping that Step 6a should use to determine the Task issue type ID
- `plan-feature/SKILL.md` Step 5 -- convention-aware task enrichment that consumes the formatted convention references

### Independence Assessment

These two problems are **independent**:

- **Different modules**: Root cause 1 is in `shared/convention-utils.md` (shared formatting utilities), while root cause 2 is in `plan-feature/SKILL.md` (feature planning skill logic).
- **Different code paths**: The convention formatter runs during Implementation Notes generation (Step 5 convention enrichment); the issue type selection runs during Jira issue creation (Step 6a). These are separate phases of the `/plan-feature` execution.
- **No shared state**: The convention formatting output does not influence the issue type selection, and vice versa. Fixing one does not affect the other.
- **Independent fixes**: Each root cause requires a separate, self-contained change to a different file.

### Persistence-Impact Analysis

Neither defect involves data persistence in a database. The convention references are generated inline in Jira task descriptions, and the issue type is set at task creation time. No data migration is needed -- fixing the code will correct all future outputs. Existing tasks created with the wrong convention format or wrong issue type would need manual correction in Jira, but this is a Jira content issue rather than a database migration.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Wrong Case Transform in Convention Reference Formatter

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` applies a kebab-case transform to CONVENTIONS.md section headings when generating `Per CONVENTIONS.md §...` notation for Implementation Notes.
- **Why it is broken**: The formatter normalizes headings to a URL-slug format (lowercase, hyphens instead of spaces), but convention references in Implementation Notes must preserve the original heading text in its original case to match the source document. The `shared/convention-applicability-rules.md` specifies the format as `Per CONVENTIONS.md §<Section Name>` where `<Section Name>` is the exact heading text.
- **Where it is broken**: `shared/convention-utils.md` -- the case transform function applied to section heading text before insertion into the reference string.
- **How to verify**: A reproducer test should create a CONVENTIONS.md with a multi-word titled section (e.g., `## Migration Patterns`), run the convention reference formatter, and assert the output contains `§Migration Patterns` (preserving the original case) rather than `§migration-patterns` (kebab-case).

### Root Cause 2: Wrong Issue Type ID in Task Creation

- **What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a uses the `Feature issue type ID` (10142) from CLAUDE.md Jira Configuration when creating task issues, instead of using the Task type discovered through the issue type scheme in Step 2.5.
- **Why it is broken**: The code path that selects the issue type for task creation references the wrong configuration field. It reads `Feature issue type ID` unconditionally from CLAUDE.md rather than using the Task role type ID from the type-to-role mapping built in Step 2.5. The type-to-role mapping correctly identifies the Task type (level 0) from the project's issue type scheme, but Step 6a does not consume it.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `jira.create_issue` call's issue type parameter.
- **How to verify**: A reproducer test should configure a project with a custom issue type scheme where Task has a distinct ID (e.g., 10050, different from the Feature type ID 10142), run `/plan-feature`, and assert the created issue has `issuetype.id` equal to the Task ID (10050), not the Feature ID (10142).

## Conclusion

The investigation reveals **two independent root causes** in **different modules** with **different code paths**. This triggers the Decomposition Guard (Step 6) -- the skill must pause and present the user with the option to proceed with a single bundled Task or split into separate Bug issues for each independent fix. See `decomposition-guard.md` for the guard prompt.
