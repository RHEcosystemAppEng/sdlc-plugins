# Triage Investigation: ACME-502

## Step 0 -- Config Validation

Configuration extracted from CLAUDE.md (`claude-md-bug-config.md`):

| Field | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Feature issue type ID | 10142 |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |
| Repository Registry | Present (acme-backend) |
| Code Intelligence | Present (no Serena instances) |

All required sections are present and valid. Configuration validation passed.

## Step 1 -- Fetch Bug

### Issue Metadata

| Field | Value |
|---|---|
| Key | ACME-502 |
| Summary | Skill output is malformed and task creation uses wrong issue type |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Web URL | https://mock-jira.example.com/browse/ACME-502 |

**Issue type validation**: Issue type ID 10020 matches Bug issue type ID 10020 from Bug Configuration. Validated.

### Parsed Description Sections

**Required Sections** (all present):

- **Description**: Two distinct problems occur when running `/plan-feature`: (1) generated task description has malformed Implementation Notes with convention references using the wrong section heading format (e.g., `migration-patterns` instead of `Migration Patterns`); (2) task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.
- **Steps to Reproduce**: Configure a project with custom issue type scheme (Task ID 10050), add CONVENTIONS.md with `## Migration Patterns`, run `/plan-feature ACME-200`, observe the generated task for convention references and issue type.
- **Expected Result**: Convention references should be `Migration Patterns` (title case). Created issue should be type Task (ID 10050).
- **Actual Result**: Convention references are `migration-patterns` (kebab-case). Created issue is type Feature (ID 10142) instead of Task.

**Optional Sections** (present):

- **Suggested Fix**: Present. Reporter suggests two separate bugs -- convention reference formatter issue and task creation issue type logic.

No required sections are missing. Bug description is well-formed per the template.

## Step 2 -- Reproduce/Trace

The bug involves skill/documentation behavior that cannot be directly executed. Code-path tracing is used instead.

### Trace 1 -- Convention Reference Formatting

Entry point: `/plan-feature ACME-200` generates a task description with Implementation Notes that reference CONVENTIONS.md sections.

Trace path:
1. `/plan-feature` reads the target repository's `CONVENTIONS.md` file.
2. When generating Implementation Notes, convention section headings are formatted as references (e.g., `Migration Patterns`).
3. The convention reference formatter in `shared/convention-utils.md` applies a kebab-case transform to section headings.
4. The transform lowercases the text and replaces spaces with hyphens.
5. This produces `migration-patterns` instead of preserving the original heading text `Migration Patterns`.

**Divergence**: The formatter applies a kebab-case transform when it should preserve the original heading text as-is. The output `migration-patterns` does not match the heading `Migration Patterns`.

### Trace 2 -- Issue Type Selection

Entry point: `/plan-feature ACME-200` creates a Jira issue for the generated task.

Trace path:
1. Task creation in `plan-feature/SKILL.md` Step 6a reads the issue type ID from Jira Configuration.
2. The code reads the **Feature issue type ID** (10142) from the Jira Configuration section.
3. It should instead use a **Task issue type ID** (10050) for creating task issues.
4. This causes the created issue to have type Feature (ID 10142) instead of Task (ID 10050).

**Divergence**: The task creation logic reads the wrong configuration field. It uses `Feature issue type ID: 10142` when it should use a Task issue type ID (10050).

## Step 3 -- Codebase Investigation

### Affected Module 1: `shared/convention-utils.md`

- **Role**: Convention reference formatter -- transforms CONVENTIONS.md section headings into reference strings for use in generated task descriptions.
- **Defect**: The formatter applies a kebab-case transform (lowercase + hyphen-separated) to section headings. This produces `migration-patterns` from `## Migration Patterns`.
- **Expected behavior**: The formatter should preserve the original heading text as-is, producing `Migration Patterns`.

### Affected Module 2: `plan-feature/SKILL.md` Step 6a

- **Role**: Task creation logic -- creates Jira issues for planned tasks.
- **Defect**: Step 6a reads the Feature issue type ID (10142) from the Jira Configuration section when creating task issues. It should use the Task issue type ID (10050).
- **Expected behavior**: Task creation should use the Task issue type ID, not the Feature issue type ID.

### Independence Assessment

These two modules are in different parts of the codebase:
- `shared/convention-utils.md` handles text formatting for convention references.
- `plan-feature/SKILL.md` Step 6a handles Jira issue creation parameters.

They have no shared code paths, no shared data structures, and no causal relationship. A fix to one does not affect the other.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention reference formatter uses wrong case transform

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` transforms section headings to kebab-case.
- **Why it is broken**: The formatter applies `toLowerCase()` and replaces spaces with hyphens, producing `migration-patterns` from `Migration Patterns`. It should preserve the original heading text.
- **Where it is broken**: `shared/convention-utils.md` -- the kebab-case transform function.
- **How to verify**: A reproducer test should assert that given a CONVENTIONS.md with `## Migration Patterns`, the formatter outputs `Migration Patterns` (not `migration-patterns`).

### Root Cause 2: Task creation uses Feature issue type ID instead of Task

- **What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a creates issues with the wrong issue type.
- **Why it is broken**: Step 6a reads the `Feature issue type ID` (10142) from Jira Configuration instead of using a Task issue type ID (10050).
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the issue type ID field reference in the task creation call.
- **How to verify**: A reproducer test should assert that when creating a task, the issue type ID used is the Task type (10050), not the Feature type (10142).

### Independence Determination

| Criterion | Root Cause 1 | Root Cause 2 |
|---|---|---|
| Module | `shared/convention-utils.md` | `plan-feature/SKILL.md` Step 6a |
| Code path | Convention formatting pipeline | Jira issue creation pipeline |
| Can be fixed independently | Yes | Yes |
| Reproducer strategy | Format a heading and assert output | Create an issue and assert type ID |

The two root causes are in different modules, follow different code paths, can be fixed independently, and require different reproducer strategies. This independence triggers the **Decomposition Guard** (Step 6).
