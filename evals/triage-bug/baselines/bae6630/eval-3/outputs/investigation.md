# Investigation Report: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- validated against Bug Configuration (Bug issue type ID: 10020)
**Status**: New
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

## Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration.

## Step 1 -- Fetch Bug and Parse Description

### Issue Type Validation

Issue type ID 10020 matches the Bug issue type ID from Bug Configuration. Validated.

### Parsed Bug Description

**Required Sections** (all present per bug-template-mock.md):

- **Issue Description**: Two distinct problems occur when running `/plan-feature`: (1) malformed convention references using wrong heading format (kebab-case instead of title case), and (2) task created with wrong issue type ("Feature" instead of "Task").
- **Steps to Reproduce**: Configure a project with custom issue type scheme (Task ID 10050), add CONVENTIONS.md with `## Migration Patterns` section, run `/plan-feature ACME-200`, observe generated task convention references and issue type.
- **Expected Result**: Convention references should use `Migration Patterns` (title case, matching heading). Created issue should be type Task (ID 10050).
- **Actual Result**: Convention references use `migration-patterns` (kebab-case). Created issue is type Feature (ID 10142) instead of Task.

**Optional Sections**:

- **Suggested Fix**: Reporter notes these are likely two separate bugs -- one in the convention reference formatter and one in the task creation logic.

### Metadata

- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: not set

## Step 2 -- Code-Path Tracing

The bug cannot be directly reproduced (it involves skill invocation behavior), so code-path tracing was performed.

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` skill invocation, Step 5 (Generate Jira Tasks), convention-aware task enrichment.

Execution path:
1. `/plan-feature` Step 3 reads CONVENTIONS.md and discovers section headings (e.g., `## Migration Patterns`).
2. Step 5 applies convention-aware task enrichment, cross-referencing conventions against task scope.
3. The convention formatter in `shared/convention-utils.md` is responsible for producing the `Per CONVENTIONS.md section-name` reference in Implementation Notes.
4. The formatter incorrectly transforms the section heading to kebab-case (lowercasing and replacing spaces with hyphens), producing `migration-patterns` instead of preserving the original heading text `Migration Patterns`.

Divergence: The formatter applies a slug/kebab-case transformation to section headings instead of preserving the original title-case heading text. The convention-applicability-rules.md specifies the format should be `Per CONVENTIONS.md <Section Name>` with the original section name, but the convention-utils formatter normalizes it.

### Trace 2: Task Creation Issue Type

Entry point: `/plan-feature` skill invocation, Step 6a (Create Tasks in Jira).

Execution path:
1. Step 2.5 discovers project issue types and builds a type-to-role mapping (Feature, Epic, Task).
2. Step 6a creates issues using `jira.create_issue`.
3. The task creation logic in `plan-feature/SKILL.md` Step 6a should use the Task issue type ID (level 0) from the type-to-role mapping.
4. Instead, the logic reads the Feature issue type ID (10142) from Jira Configuration rather than the dynamically discovered Task type ID (10050) from Step 2.5.

Divergence: The task creation code path uses the hardcoded Feature issue type ID from CLAUDE.md's Jira Configuration section instead of the Task type ID discovered dynamically in Step 2.5. When a project has a custom issue type scheme, the Task type ID differs from the Feature type ID, but the code does not reference the correct mapping entry.

## Step 3 -- Codebase Investigation

### Target Repository

The bug affects the `sdlc-workflow` plugin within the `sdlc-plugins` repository.

### Affected Files and Modules

#### Root Cause 1: Convention Reference Formatting

- **Affected module**: `shared/convention-utils.md` (the convention formatter utility)
- **Symptom**: Convention section references are output as kebab-case slugs (e.g., `migration-patterns`) instead of the original heading text (e.g., `Migration Patterns`)
- **Related files**:
  - `shared/convention-applicability-rules.md` -- defines the prescribed format: `Per CONVENTIONS.md <Section Name>: <action>` with original section name
  - `plan-feature/SKILL.md` Step 5 -- invokes convention-aware task enrichment which calls the formatter

#### Root Cause 2: Task Creation Issue Type

- **Affected module**: `plan-feature/SKILL.md` Step 6a (task creation logic)
- **Symptom**: Tasks are created with issue type Feature (ID 10142) instead of Task (the level-0 type from the dynamically discovered type-to-role mapping)
- **Related files**:
  - `plan-feature/SKILL.md` Step 2.5 -- discovers issue types and builds type-to-role mapping
  - `plan-feature/SKILL.md` Step 6a -- should use the Task role from the mapping but instead uses the Feature issue type ID from Jira Configuration

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention Reference Formatter (shared/convention-utils.md)

- **What is broken**: The convention reference formatter transforms CONVENTIONS.md section headings into kebab-case slugs instead of preserving the original heading text.
- **Why it is broken**: The formatter applies a normalization function (lowercase + hyphen-replace) to section headings when generating the `Per CONVENTIONS.md section-reference` string. This is incorrect -- the convention-applicability-rules.md prescribes that the section name should match the original heading text verbatim (e.g., `Migration Patterns`, not `migration-patterns`).
- **Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference conversion logic.
- **How to verify the fix**: A reproducer test should:
  1. Provide a CONVENTIONS.md with a section `## Migration Patterns`
  2. Run the convention formatter to produce a reference
  3. Assert the output contains `Migration Patterns` (title case), not `migration-patterns` (kebab-case)

### Root Cause 2: Task Creation Issue Type (plan-feature/SKILL.md Step 6a)

- **What is broken**: The task creation logic uses the Feature issue type ID from static Jira Configuration instead of the Task issue type ID from the dynamically discovered type-to-role mapping.
- **Why it is broken**: Step 6a reads the issue type ID directly from the `Feature issue type ID` field in CLAUDE.md's Jira Configuration, bypassing the type-to-role mapping built in Step 2.5. When the project has a custom issue type scheme where Task has a different ID (e.g., 10050), the wrong type ID is used.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the issue type parameter passed to `jira.create_issue`.
- **How to verify the fix**: A reproducer test should:
  1. Configure a project with a custom issue type scheme (Task ID 10050, Feature ID 10142)
  2. Run `/plan-feature` to create tasks
  3. Assert the created issue's type ID is 10050 (Task), not 10142 (Feature)

## Independence Assessment

These two root causes are **independent**:

1. **Different modules**: Root Cause 1 is in `shared/convention-utils.md` (a shared utility for formatting convention references). Root Cause 2 is in `plan-feature/SKILL.md` Step 6a (the task creation logic specific to plan-feature).
2. **Different code paths**: The convention formatter runs during Step 5 (task description generation), while the issue type selection runs during Step 6a (Jira API call). They do not share state or depend on each other.
3. **Independent fixes**: Fixing the convention formatter does not affect issue type selection, and vice versa. Each can be fixed and tested in isolation.
4. **Different symptoms**: One produces malformed text in task descriptions; the other creates issues with the wrong Jira type.

This triggers the **Decomposition Guard** (Step 6 of the triage-bug skill).

---

*This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/mrizzi/sdlc-plugins) v0.11.0.*
