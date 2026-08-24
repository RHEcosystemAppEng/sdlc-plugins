# Investigation Findings: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow

## Step 0 -- Validate Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

Issue type validation: ACME-502 has issue type ID 10020, which matches the Bug issue type ID from Bug Configuration. Confirmed as Bug.

## Step 1 -- Parse Bug Description

### Required Sections Extracted

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Environment / Version | **Missing** |

**Note**: The "Environment / Version" required section is missing from the bug description. Per the skill's Step 1 rules, this would normally halt execution. For this analysis, the finding is recorded and investigation proceeds based on the eval directive.

### Optional Sections

| Section | Status |
|---------|--------|
| Suggested Fix | Present -- reporter suspects two separate bugs |

## Step 2 -- Code-Path Tracing

Two distinct code paths were traced from the Steps to Reproduce:

### Trace A: Convention Reference Formatting

1. **Entry point**: `/plan-feature ACME-200` invocation
2. **Path**: plan-feature reads `CONVENTIONS.md` to discover section headings (e.g., `## Migration Patterns`)
3. **Transformation**: The convention reference formatter in `shared/convention-utils.md` converts section headings to reference format
4. **Defect location**: The formatter applies lowercase + kebab-case transformation (`Migration Patterns` -> `migration-patterns`), producing `section-migration-patterns` instead of preserving the original title-case heading text
5. **Output**: Implementation Notes in the generated task contain `section-migration-patterns` instead of `section-Migration Patterns`

### Trace B: Issue Type Selection

1. **Entry point**: `/plan-feature ACME-200` invocation
2. **Path**: plan-feature Step 6a creates Jira issues for planned tasks
3. **Defect location**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the **Feature issue type ID** (10142) from Jira Configuration instead of using the **Task issue type ID** when creating sub-tasks
4. **Output**: Created issue has type Feature (ID 10142) instead of Task (ID 10050, as configured in the project's custom issue type scheme)

## Step 3 -- Codebase Investigation

### Affected Files and Symbols

| # | File | Module | Symbol/Area | Issue |
|---|------|--------|-------------|-------|
| 1 | `shared/convention-utils.md` | Convention utilities | Convention reference formatter | Incorrectly lowercases and kebab-cases CONVENTIONS.md section headings when generating `section-` references |
| 2 | `plan-feature/SKILL.md` | Plan Feature skill | Step 6a -- Task creation | Reads Feature issue type ID from config instead of Task issue type ID |

### Persistence-Impact Analysis

Neither defect writes incorrect values to a persistent database. Both produce incorrect output in Jira issue descriptions at creation time. Since the Jira issue content is the final output (not an intermediate value stored in a separate database), no data migration is needed beyond correcting the code paths and re-running the affected skill invocations.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Malformed Convention References

- **What is broken**: The convention reference formatter transforms CONVENTIONS.md section headings into kebab-case slugs instead of preserving the original heading text.
- **Why it is broken**: The formatter applies a `toLowerCase()` + kebab-case transformation that is appropriate for URL slugs but incorrect for human-readable convention references in Implementation Notes.
- **Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference conversion function.
- **How to verify**: A reproducer test should parse a CONVENTIONS.md with a heading `## Migration Patterns`, invoke the formatter, and assert the output contains `section-Migration Patterns` (title case preserved), not `section-migration-patterns`.

### Root Cause 2: Wrong Issue Type in Task Creation

- **What is broken**: Tasks created by plan-feature use the Feature issue type instead of the Task issue type.
- **Why it is broken**: The task creation logic in Step 6a references the `Feature issue type ID` field from Jira Configuration rather than looking up or using a Task-specific issue type ID.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `create_issue` call's issue type parameter.
- **How to verify**: A reproducer test should configure a project with Task issue type ID 10050 and Feature issue type ID 10142, run plan-feature, and assert the created issue's `issuetype.id` equals 10050 (Task), not 10142 (Feature).

## Independence Assessment

These two root causes are **independent**:

1. They reside in **different modules** (`shared/convention-utils.md` vs. `plan-feature/SKILL.md`).
2. They affect **different code paths** (convention formatting vs. issue creation).
3. Fixing one does **not** fix or affect the other.
4. They can be **tested independently** with separate reproducer tests.
5. They have **no shared state** or coupling between them.

This triggers the **Decomposition Guard** (Step 6) -- see `decomposition-guard.md` for the user prompt.
