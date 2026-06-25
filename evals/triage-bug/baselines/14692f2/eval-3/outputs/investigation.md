# triage-bug Investigation: ACME-502

## Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

| Field | Value |
|-------|-------|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Feature issue type ID | 10142 |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration. Configuration is valid.

## Step 1 -- Fetch Bug

**Issue**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

### Issue type validation

Issue type ID 10020 matches Bug issue type ID 10020 from Bug Configuration. Validated.

### Parse bug description

Template defines Required Sections and Optional Sections. Parsing bug description against template headings:

**Required Sections** (all present):

| Section | Heading | Status |
|---------|---------|--------|
| Description | `### **Issue Description**` | Present |
| Steps to Reproduce | `### **Steps to Reproduce**` | Present |
| Expected Result | `### **Expected Result**` | Present |
| Actual Result | `### **Actual Result**` | Present |

All required sections are present. No missing sections.

**Optional Sections:**

| Section | Heading | Status |
|---------|---------|--------|
| Root Cause | `### **Root Cause**` | Not present |
| Suggested Fix | `### **Suggested Fix**` | Present |

### Parsed content

**Description**: Two distinct problems occur when running `/plan-feature`: (1) generated task descriptions have malformed Implementation Notes where convention references use wrong section heading format (e.g., `migration-patterns` instead of `Migration Patterns`), and (2) the task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

**Steps to Reproduce**:
1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

**Expected Result**:
- Implementation Notes should reference conventions as `Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

**Actual Result**:
- Implementation Notes reference conventions as `migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

**Suggested Fix**: These are likely two separate bugs: the convention reference formatter lowercases and kebab-cases headings incorrectly; the task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

## Step 2 -- Reproduce/Trace

This bug affects skill behavior and documentation/configuration logic, so direct runnable reproduction is not feasible. Code-path tracing is used instead.

### Trace 1: Convention reference formatting

**Entry point**: `/plan-feature` skill invocation, specifically the step that generates Implementation Notes with convention references.

**Trace path**:
1. When `/plan-feature` generates task descriptions, it reads `CONVENTIONS.md` from the target repository.
2. Convention section headings (e.g., `## Migration Patterns`) are extracted and formatted as convention references (e.g., `Migration Patterns`) in the Implementation Notes.
3. The convention reference formatter in `shared/convention-utils.md` applies a kebab-case transform to the heading text: it lowercases the text and replaces spaces with hyphens.
4. This produces `migration-patterns` instead of preserving the original heading text `Migration Patterns`.

**Divergence**: The formatter should preserve the original heading text as-is for the convention reference. Instead, it applies an unnecessary kebab-case normalization that corrupts the reference.

### Trace 2: Issue type selection

**Entry point**: `/plan-feature` skill invocation, specifically the task creation step.

**Trace path**:
1. When `/plan-feature` creates a task in Jira (Step 6a of plan-feature/SKILL.md), it needs the issue type ID for "Task".
2. The task creation logic reads the issue type ID from Jira Configuration in CLAUDE.md.
3. However, it reads the **Feature issue type ID** (10142) instead of the **Task issue type ID** (10050).
4. This causes the created issue to have type "Feature" rather than "Task".

**Divergence**: The task creation logic should read a Task issue type ID (10050) from the configuration, but it reads the Feature issue type ID (10142) instead.

## Step 3 -- Codebase Investigation

### Affected Module 1: shared/convention-utils.md

- **File**: `shared/convention-utils.md`
- **Issue**: The convention reference formatter applies a kebab-case transform (lowercase + replace spaces with hyphens) to CONVENTIONS.md section headings when generating convention references for task Implementation Notes.
- **Impact**: All convention references in generated task descriptions are malformed -- they use kebab-case (e.g., `migration-patterns`) instead of preserving the original heading text (e.g., `Migration Patterns`).
- **Correct behavior**: The formatter should emit the heading text exactly as it appears in the CONVENTIONS.md file, without any case or formatting transform.

### Affected Module 2: plan-feature/SKILL.md Step 6a

- **File**: `plan-feature/SKILL.md`, Step 6a (task creation)
- **Issue**: The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID (10050).
- **Impact**: Tasks created by `/plan-feature` have the wrong issue type ("Feature" instead of "Task"), which breaks downstream workflows that filter or process by issue type.
- **Correct behavior**: Step 6a should read a dedicated Task issue type ID from the configuration, not reuse the Feature issue type ID.

### Existing test patterns

No automated tests were found for convention reference formatting or issue type selection in task creation. The reproducer tests would be novel additions.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention reference formatter uses wrong case transform

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` applies a kebab-case transform to CONVENTIONS.md section headings, producing references like `migration-patterns` instead of `Migration Patterns`.
- **Why it is broken**: The formatter applies `toLowerCase()` and replaces spaces with hyphens, which is appropriate for URL slugs or CSS class names but incorrect for convention references that should preserve human-readable heading text.
- **Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference formatting logic.
- **How to verify the fix**: A reproducer test should assert that given a CONVENTIONS.md heading `## Migration Patterns`, the generated convention reference is `Migration Patterns` (preserving original case and spacing), not `migration-patterns`.

### Root Cause 2: Task creation uses Feature issue type ID instead of Task

- **What is broken**: Task creation in `plan-feature/SKILL.md` Step 6a creates issues with the Feature issue type ID (10142) instead of the Task issue type ID (10050).
- **Why it is broken**: The task creation step reads `Feature issue type ID` from Jira Configuration rather than a dedicated `Task issue type ID` field. The configuration either lacks a Task issue type ID field, or the code references the wrong field.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the issue type ID selection for `jira.create_issue`.
- **How to verify the fix**: A reproducer test should assert that when `/plan-feature` creates a task, the `issuetype.id` in the Jira API call is the Task issue type ID (10050), not the Feature issue type ID (10142).

### Independence assessment

These two root causes are **independent**:

- **Different modules**: Root cause 1 is in `shared/convention-utils.md`; root cause 2 is in `plan-feature/SKILL.md` Step 6a.
- **Different code paths**: Root cause 1 affects the convention reference formatting pipeline; root cause 2 affects the Jira issue creation pipeline. They share no code.
- **Can be fixed independently**: Fixing the convention formatter does not affect issue type selection, and vice versa. Each fix can be developed, tested, and merged independently.
- **Different reproducer strategies**: Root cause 1 requires testing string formatting output; root cause 2 requires testing Jira API call parameters. The tests have no overlap.

This independence triggers the **Decomposition Guard** (Step 6).
