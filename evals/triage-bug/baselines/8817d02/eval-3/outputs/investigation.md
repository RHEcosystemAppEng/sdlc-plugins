# Investigation: ACME-502

## Bug Summary

| Field | Value |
|-------|-------|
| **Key** | ACME-502 |
| **Summary** | Skill output is malformed and task creation uses wrong issue type |
| **Issue Type** | Bug (ID: 10020) |
| **Status** | New |
| **Labels** | reported-by-user |
| **Component** | sdlc-workflow |
| **Web URL** | https://mock-jira.example.com/browse/ACME-502 |

## Step 0 -- Configuration Validation

Project CLAUDE.md validated successfully. Extracted configuration:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration.

## Step 1 -- Bug Parsing

**Issue type validation**: Issue type ID 10020 matches Bug Configuration. Confirmed Bug.

**Parsed sections** (from bug description template):

| Section | Status | Type |
|---------|--------|------|
| Issue Description | Present | Required |
| Steps to Reproduce | Present | Required |
| Expected Result | Present | Required |
| Actual Result | Present | Required |
| Attachments | Present (None) | Required |
| Root Cause | Not present | Optional |
| Suggested Fix | Present | Optional |

All required sections are present. Bug description follows the template.

**Extracted metadata**:
- Issue key: ACME-502
- Web URL: https://mock-jira.example.com/browse/ACME-502
- Summary: Skill output is malformed and task creation uses wrong issue type
- Labels: reported-by-user
- Component: sdlc-workflow

## Step 2 -- Code-Path Tracing

The bug describes two distinct symptoms that occur when running `/plan-feature`. Since this is a skill/documentation bug, direct reproduction is not applicable -- code-path tracing is used instead.

### Trace 1: Convention Reference Formatting

**Entry point**: `/plan-feature ACME-200` -- during task description generation, Implementation Notes reference conventions from `CONVENTIONS.md`.

**Trace path**:
1. `/plan-feature` generates a task description with Implementation Notes.
2. Implementation Notes include convention references using the `§` notation.
3. The convention reference formatter in `shared/convention-utils.md` is responsible for transforming section headings from `CONVENTIONS.md` into `§`-prefixed references.
4. The formatter applies a kebab-case transform to the heading text (e.g., `## Migration Patterns` becomes `§migration-patterns`).
5. The expected behavior is to preserve the original title case from the heading (e.g., `§Migration Patterns`).

**Defect location**: `shared/convention-utils.md` -- the convention reference formatter applies `kebab-case` transform instead of preserving the original title case of the heading.

**Divergence**: The formatter lowercases and hyphenates the heading text, producing `§migration-patterns` instead of the expected `§Migration Patterns`.

### Trace 2: Task Creation Issue Type

**Entry point**: `/plan-feature ACME-200` -- during task creation in Jira.

**Trace path**:
1. `/plan-feature` proceeds to create a Task issue in Jira at Step 6a.
2. Step 6a reads the issue type ID to use for the created issue.
3. The logic reads the **Feature issue type ID** (10142) from Jira Configuration instead of reading the **Task issue type ID** from the project's issue type scheme.
4. The created issue is therefore of type Feature (ID 10142) rather than Task.

**Defect location**: `plan-feature/SKILL.md` Step 6a -- the task creation logic references the Feature issue type ID (10142) from CLAUDE.md Jira Configuration instead of the correct Task issue type ID.

**Divergence**: When the project has a custom issue type scheme where Task has ID 10050, the skill ignores this and hardcodes/reads the Feature issue type ID (10142), resulting in the wrong issue type.

## Step 3 -- Codebase Investigation

### Root Cause 1: Convention Reference Formatting

**Affected files**:
- `shared/convention-utils.md` -- contains the convention reference formatter logic that transforms `CONVENTIONS.md` headings into `§`-prefixed references
- Any skill that generates Implementation Notes with convention references (consumer of the utility)

**Pattern**: The formatter has a case transform function that converts heading text to kebab-case. This should instead preserve the original case of the heading as it appears in `CONVENTIONS.md`.

### Root Cause 2: Task Creation Issue Type

**Affected files**:
- `plan-feature/SKILL.md` Step 6a -- the task creation step that reads the issue type ID
- CLAUDE.md Jira Configuration -- provides the Feature issue type ID (10142) but does not provide a separate Task issue type ID

**Pattern**: Step 6a reads `Feature issue type ID` from the Jira Configuration section. It should instead use the correct Task issue type ID for the project's issue type scheme, or there should be a separate `Task issue type ID` configuration entry.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention Reference Case Transform

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` applies a kebab-case transform to `CONVENTIONS.md` section headings when generating `§`-prefixed references in Implementation Notes.
- **Why it is broken**: The formatter lowercases the heading text and replaces spaces with hyphens, producing references like `§migration-patterns` instead of preserving the original title case as `§Migration Patterns`. The transform was likely implemented for URL-safe anchors but is incorrectly applied to human-readable convention references.
- **Where it is broken**: `shared/convention-utils.md` -- the case transform function within the convention reference formatter.
- **How to verify the fix**: Create a `CONVENTIONS.md` with a section heading `## Migration Patterns`. Run the convention reference formatter and assert that the output is `§Migration Patterns` (title case preserved), not `§migration-patterns` (kebab-case).

### Root Cause 2: Task Creation Issue Type Mismatch

- **What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a creates issues using the Feature issue type ID (10142) instead of the Task issue type ID.
- **Why it is broken**: Step 6a reads `Feature issue type ID` from the Jira Configuration section in CLAUDE.md. When the project has a custom issue type scheme, the Task issue type has a different ID (e.g., 10050), but the skill does not read or use this value.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the issue type ID selection during task creation.
- **How to verify the fix**: Configure a project with a custom issue type scheme where Task has ID 10050. Run `/plan-feature` and verify the created issue has issue type Task (ID 10050), not Feature (ID 10142).

## Independence Assessment

The two root causes are **independent**:

1. **Different modules**: Root Cause 1 is in `shared/convention-utils.md` (shared utility); Root Cause 2 is in `plan-feature/SKILL.md` Step 6a (skill-specific logic).
2. **Different code paths**: Root Cause 1 affects the convention reference formatting pipeline; Root Cause 2 affects the Jira issue creation pipeline. These are separate execution paths with no shared logic.
3. **Can be fixed independently**: Fixing the case transform in `shared/convention-utils.md` has no effect on the issue type selection in `plan-feature/SKILL.md`, and vice versa.
4. **Different symptoms**: Root Cause 1 produces malformed convention references in the task description; Root Cause 2 produces issues with the wrong Jira issue type.

Because these are independent root causes in different modules affecting different code paths, the **Decomposition Guard (Step 6)** is triggered. A single Task should not be created without user confirmation.
