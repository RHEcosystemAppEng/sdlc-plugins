# Investigation: ACME-502

## Step 0 -- Validate Configuration

Project CLAUDE.md validated. Bug Configuration is present:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

## Step 1 -- Fetch Bug and Parse

- **Issue key**: ACME-502
- **Summary**: Skill output is malformed and task creation uses wrong issue type
- **Issue Type**: Bug (ID: 10020) -- matches Bug Configuration. Validated.
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Web URL**: https://mock-jira.example.com/browse/ACME-502

### Parsed Sections (all 4 required sections present)

**Issue Description**: Two distinct problems occur when running `/plan-feature`:
1. The generated task description has malformed Implementation Notes -- convention references use the wrong section heading format (e.g., `migration-patterns` instead of `Migration Patterns`).
2. The task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

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

**Optional Sections**:
- Suggested Fix: present (reporter suspects two separate bugs)

## Steps 2-3 -- Codebase Investigation and Reproduction/Trace

### Root Cause 1: Convention reference formatter using wrong case transform

- **Affected file/module**: `shared/convention-utils.md`
- **What is broken**: The convention reference formatter lowercases and kebab-cases convention section headings when generating section references for Implementation Notes output. For example, a `CONVENTIONS.md` heading `## Migration Patterns` is transformed to `migration-patterns` instead of being preserved as `Migration Patterns`.
- **Why it is broken**: The formatter applies a `toLowerCase()` + kebab-case transform to heading text when generating cross-references (e.g., `migration-patterns`). This transform is intended for generating URL-safe anchors, but it is incorrectly applied to the display text of the convention reference in the Implementation Notes output.
- **Where it is broken**: The case transform logic in `shared/convention-utils.md` that formats convention heading references.
- **How to verify**: Create a `CONVENTIONS.md` with a heading `## Migration Patterns`, run the convention formatter, and assert that the output reference preserves the original title case (`Migration Patterns`) rather than producing kebab-case (`migration-patterns`).

### Root Cause 2: Task creation using Feature issue type ID instead of Task

- **Affected file/module**: `plan-feature/SKILL.md` Step 6a
- **What is broken**: When creating a Task issue in Jira, the task creation logic reads the `Feature issue type ID` (10142) from the Jira Configuration section of CLAUDE.md instead of using a `Task issue type ID` or directly specifying the "Task" issue type.
- **Why it is broken**: The task creation step in `plan-feature/SKILL.md` Step 6a references the wrong configuration field. It reads `Feature issue type ID` (which is 10142) from the `## Jira Configuration` section rather than looking up the correct Task issue type. This causes all created tasks to have the "Feature" issue type instead of "Task".
- **Where it is broken**: The issue type parameter in the `jira.create_issue` call within `plan-feature/SKILL.md` Step 6a.
- **How to verify**: Run `/plan-feature` on a project with a custom issue type scheme and verify that the created issue has type "Task" (not "Feature").

## Independence Assessment

These two root causes are **independent**:

1. They reside in **different files/modules**: `shared/convention-utils.md` vs `plan-feature/SKILL.md`
2. They affect **different code paths**: the convention reference formatting pipeline vs the Jira issue creation pipeline
3. Either bug can be fixed without affecting the other
4. Each bug has its own distinct reproducer test and verification strategy

This triggers the **Decomposition Guard** (Step 6) because multiple independent root causes were found across different modules.
