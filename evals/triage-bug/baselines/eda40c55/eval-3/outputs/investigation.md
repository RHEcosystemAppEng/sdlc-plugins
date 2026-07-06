# Investigation Findings — ACME-502

## Step 0 — Configuration Validation

Project configuration validated successfully:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 — Fetch and Parse Bug

**Issue**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) — matches configured Bug issue type ID (10020). Valid.
**Labels**: reported-by-user
**Component**: sdlc-workflow

### Description Parsing

All required sections present per the bug template (`docs/templates/bug-template.md`):

| Required Section | Heading Format | Present |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Attachments | `### **Attachments**` | Yes |

Optional sections:

| Optional Section | Present |
|---|---|
| Root Cause | No |
| Suggested Fix | Yes |

**Parsing result: PASS** — all required sections are present.

### Extracted Content

**Steps to Reproduce**:
1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

**Expected Result**:
- Implementation Notes should reference conventions as `§Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

**Actual Result**:
- Implementation Notes reference conventions as `§migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

**Suggested Fix** (from reporter):
- The convention reference formatter lowercases and kebab-cases headings incorrectly.
- The task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

---

## Step 2 — Code-Path Tracing

This bug involves skill/documentation behavior and cannot be directly reproduced via runnable commands. Code-path tracing was performed instead.

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` skill invocation, specifically the step that generates Implementation Notes with convention references.

Traced path:
1. `/plan-feature` reads the target repo's `CONVENTIONS.md` and identifies section headings (e.g., `## Migration Patterns`).
2. When generating Implementation Notes, convention headings are passed through a reference formatter in `shared/convention-utils.md`.
3. The formatter applies a case transform: it lowercases the heading text and converts spaces to hyphens (kebab-case), producing `§migration-patterns`.
4. The expected behavior is to preserve the original title case from the heading, producing `§Migration Patterns`.

**Divergence point**: The case transform function in `shared/convention-utils.md` applies `lowercase + kebab-case` instead of preserving the original heading text.

### Trace 2: Task Issue Type Selection

Entry point: `/plan-feature` skill invocation, specifically Step 6a where the Task issue is created in Jira.

Traced path:
1. `/plan-feature` reads the Jira Configuration from CLAUDE.md to determine issue type IDs.
2. In Step 6a, the task creation logic selects an issue type ID for the new issue.
3. The logic reads `Feature issue type ID: 10142` from the Jira Configuration instead of the correct `Task issue type ID: 10050`.
4. The Jira `create_issue` call is made with issue type ID 10142 (Feature) instead of 10050 (Task).

**Divergence point**: The issue type ID lookup in `plan-feature/SKILL.md Step 6a` references the wrong configuration field — it uses `Feature issue type ID` instead of the Task issue type ID.

---

## Step 3 — Codebase Investigation

### Root Cause 1: Convention Reference Formatter

- **Affected file**: `shared/convention-utils.md`
- **Affected logic**: The convention reference formatter that converts CONVENTIONS.md section headings into `§`-prefixed references
- **Defect**: Applies `lowercase + kebab-case` transform (e.g., `Migration Patterns` becomes `migration-patterns`) instead of preserving the original title case
- **Module**: `shared/` (shared utilities used across skills)

### Root Cause 2: Task Creation Issue Type

- **Affected file**: `plan-feature/SKILL.md` (Step 6a)
- **Affected logic**: The issue type ID selection when creating a Task via `jira.create_issue`
- **Defect**: Uses `Feature issue type ID` (10142) from Jira Configuration instead of `Task issue type ID` (10050)
- **Module**: `plan-feature/` (plan-feature skill definition)

### Independence Assessment

These two root causes are **independent**:

| Dimension | Root Cause 1 | Root Cause 2 |
|---|---|---|
| **Module** | `shared/convention-utils.md` | `plan-feature/SKILL.md` |
| **Code path** | Convention heading formatting | Jira issue creation |
| **Defect type** | String transform logic | Configuration field lookup |
| **Can be fixed independently** | Yes | Yes |
| **Fixing one affects the other** | No | No |

The two defects are in different modules (`shared/` vs `plan-feature/`), affect different code paths (text formatting vs Jira API calls), and can be fixed and tested independently. This qualifies as **multiple independent root causes**.

---

## Step 4 — Root Cause Analysis

### Root Cause 1: Wrong Case Transform in Convention Reference Formatter

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` transforms CONVENTIONS.md section headings into kebab-case when generating `§`-prefixed references in Implementation Notes.
- **Why it is broken**: The formatter applies `lowercase + kebab-case` conversion (replacing spaces with hyphens and lowercasing) instead of preserving the original title case of the heading text. This produces `§migration-patterns` instead of `§Migration Patterns`.
- **Where it is broken**: `shared/convention-utils.md` — the case transform function/logic that processes heading text into convention references.
- **How to verify the fix**: Create a CONVENTIONS.md with a title-case heading (e.g., `## Migration Patterns`). Run the convention reference formatter. Assert that the output is `§Migration Patterns` (preserving title case), not `§migration-patterns` (kebab-case).

### Root Cause 2: Wrong Issue Type ID in Task Creation

- **What is broken**: The task creation logic in `plan-feature/SKILL.md Step 6a` creates issues with issue type "Feature" (ID 10142) instead of "Task" (ID 10050).
- **Why it is broken**: The Step 6a logic reads the `Feature issue type ID` field from Jira Configuration instead of the Task issue type ID. When the project has a custom issue type scheme with a separate Task type, the wrong type is selected.
- **Where it is broken**: `plan-feature/SKILL.md`, Step 6a — the `jira.create_issue` call's issue type parameter.
- **How to verify the fix**: Configure a project with `Feature issue type ID: 10142` and a Task issue type ID of 10050. Run `/plan-feature`. Assert that the created Jira issue has issue type ID 10050 (Task), not 10142 (Feature).
