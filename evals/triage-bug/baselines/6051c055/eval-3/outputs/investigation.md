# Codebase Investigation — ACME-502

## Step 2 — Reproduce/Trace

### Code-path tracing

The bug report describes two distinct problems when running `/plan-feature`:
1. Malformed convention references in Implementation Notes (kebab-case instead of title case)
2. Wrong issue type used for task creation (Feature instead of Task)

Tracing each problem independently:

#### Problem 1: Malformed convention references

1. **Entry point**: User runs `/plan-feature ACME-200` with a CONVENTIONS.md containing `## Migration Patterns`.
2. **Convention extraction**: The plan-feature skill reads CONVENTIONS.md and extracts section headings.
3. **Convention reference formatting** (in `shared/convention-utils.md`): The convention formatter transforms the heading name before inserting it into Implementation Notes. It applies a kebab-case transform, producing `§migration-patterns` instead of preserving the original heading case `§Migration Patterns`.
4. **Expected behavior**: Convention references should preserve the original heading case from CONVENTIONS.md.
5. **Actual behavior**: The formatter lowercases and kebab-cases the heading, producing `§migration-patterns`.

#### Problem 2: Wrong issue type

1. **Entry point**: Same `/plan-feature ACME-200` invocation.
2. **Task creation** (in `plan-feature/SKILL.md Step 6a`): The task creation logic reads the issue type ID from Jira Configuration.
3. **Defect**: The code reads the **Feature issue type ID** (10142) from Jira Configuration instead of using the Task issue type. The project has a custom issue type scheme where Task has ID 10050, but the skill hardcodes/reads the Feature ID.
4. **Expected behavior**: Created issue should be of type Task (ID 10050).
5. **Actual behavior**: Created issue is of type Feature (ID 10142).

## Step 3 — Codebase Investigation

### Root Cause 1: Convention reference formatter (shared/convention-utils.md)

- **Affected module**: `shared/convention-utils.md`
- **Defect**: The convention reference formatter applies an incorrect case transformation (kebab-case) to CONVENTIONS.md section headings. It should preserve the original heading case.
- **Impact**: All convention references in generated task descriptions use the wrong format.

### Root Cause 2: Task creation issue type (plan-feature/SKILL.md Step 6a)

- **Affected module**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a (task creation)
- **Defect**: The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID from the project's custom issue type scheme.
- **Impact**: Tasks are created with the wrong issue type, which affects Jira workflows and issue tracking.

## Independence Assessment

These two root causes are **independent**:

1. They are in **different modules**: `shared/convention-utils.md` vs. `plan-feature/SKILL.md Step 6a`
2. They affect **different code paths**: convention reference formatting vs. Jira issue creation
3. Fixing one does **not** fix the other — each requires a separate code change
4. They can be **tested independently** with separate reproducer tests

This triggers the **Decomposition Guard** (Step 6) because the two root causes are in different modules and represent independent defects.
