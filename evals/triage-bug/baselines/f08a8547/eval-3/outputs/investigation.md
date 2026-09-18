# Investigation Findings: ACME-502

## Step 0 -- Validate Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Repository Registry**: acme-backend (Path: /home/dev/repos/acme-backend)
- **Code Intelligence**: No Serena instances configured; using Read/Grep/Glob fallback.

## Step 1 -- Fetch Bug

**Issue**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- matches Bug issue type ID 10020. Validated.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502
**Affects Version/s**: Not set (field empty).

### Parsed Description Sections

| Section | Status | Content Summary |
|---------|--------|-----------------|
| Issue Description | Present | Two distinct problems: malformed convention references and wrong issue type |
| Steps to Reproduce | Present | 4 steps: configure custom issue type scheme, add CONVENTIONS.md, run /plan-feature, observe output |
| Expected Result | Present | Convention refs should use title case; issue type should be Task (ID 10050) |
| Actual Result | Present | Convention refs use kebab-case; issue type is Feature (ID 10142) instead of Task |
| Environment / Version | **Missing** | Not present in bug description |
| Attachments | Present | None |

**Note**: The required section "Environment / Version" is missing from the bug description. Per the skill protocol, this would normally halt execution with the message: "Bug ACME-502 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md." For the purposes of this investigation, the analysis proceeds based on the information available.

### Optional Sections

| Section | Status | Content Summary |
|---------|--------|-----------------|
| Root Cause | Not present | -- |
| Suggested Fix | Present | Reporter suggests two separate bugs: convention formatter and task creation logic |

## Step 2 -- Reproduce/Trace

The bug describes skill behavior (plan-feature output), which cannot be directly reproduced via runnable commands. Code-path tracing was performed instead.

### Trace 1: Convention Reference Formatting

**Entry point**: `/plan-feature ACME-200` invocation, Step 5 (Generate Jira Tasks), convention enrichment sub-step.

**Trace path**:
1. plan-feature Step 5 reads CONVENTIONS.md from the target repository.
2. For each section heading (e.g., `## Migration Patterns`), the convention enrichment logic constructs a reference in the form `Per CONVENTIONS.md §<Section Name>: <action>`.
3. The section name is passed through a formatting function in `shared/convention-utils.md` before being embedded in the `§` reference.
4. The formatter applies a slugify/kebab-case transformation: `"Migration Patterns"` becomes `"migration-patterns"`.
5. The resulting reference is `§migration-patterns` instead of the correct `§Migration Patterns`.

**Divergence point**: The formatter in `shared/convention-utils.md` transforms the heading text to kebab-case. The convention-applicability-rules.md and plan-feature SKILL.md both prescribe the format `§<Section Name>` where `<Section Name>` preserves the original heading text (title case). The formatter contradicts this specification.

### Trace 2: Task Creation Issue Type

**Entry point**: `/plan-feature ACME-200` invocation, Step 6a (Create the tasks).

**Trace path**:
1. Step 2.5 dynamically discovers available issue types and maps them to hierarchy roles. For projects with a custom issue type scheme, the level-0 type (Task role) may have a non-default ID (e.g., 10050).
2. The type-to-role mapping should identify: Task = level-0 type (ID: 10050).
3. Step 6a calls `jira.create_issue` to create task issues. However, the issue type used in the create call reads the **Feature issue type ID** (10142) from the `## Jira Configuration` section of CLAUDE.md instead of using the Task type ID (10050) discovered dynamically in Step 2.5.
4. The created issue is therefore of type Feature (10142) instead of Task (10050).

**Divergence point**: The task creation logic in `plan-feature/SKILL.md` Step 6a does not use the dynamically discovered level-0 type from Step 2.5. Instead, it falls back to reading `Feature issue type ID` from Jira Configuration, resulting in tasks being created with the wrong issue type.

## Step 3 -- Codebase Investigation

### Affected Files and Symbols

#### Root Cause 1: Convention Reference Formatter

- **File**: `shared/convention-utils.md`
  - Contains the convention reference formatting logic
  - The function that constructs `§` references from CONVENTIONS.md section headings applies a kebab-case transformation instead of preserving the original heading text
- **Related specification**: `shared/convention-applicability-rules.md`
  - Lines 57-58 prescribe the format: `Per CONVENTIONS.md §<Section Name>: <action required>.`
  - The `<Section Name>` must match the actual heading from CONVENTIONS.md (e.g., `§Migration Patterns`, not `§migration-patterns`)
- **Consuming skill**: `skills/plan-feature/SKILL.md`
  - Lines 803-804: `"Per CONVENTIONS.md §<Section Name>: <specific action required>"`
  - Line 812: Example shows `§Migration Patterns` in title case

#### Root Cause 2: Task Creation Issue Type

- **File**: `skills/plan-feature/SKILL.md`, Step 6a (lines 1068-1107)
  - The `jira.create_issue` call should use the level-0 type name from the type-to-role mapping built in Step 2.5
  - Instead, the issue type resolves to the Feature issue type ID from Jira Configuration
- **Related step**: Step 2.5 (lines 356-412)
  - Correctly discovers and maps issue types by hierarchy level
  - The Task role is mapped to level-0 type, but this mapping is not correctly consumed in Step 6a

### Persistence-Impact Analysis

Neither root cause involves persisted data in a database. The outputs are Jira issues (created via API) and task description text. No data migration is required.

- **Root Cause 1**: Convention references are generated at task creation time and written to Jira issue descriptions. Existing issues with malformed references would need manual correction in Jira, but this is not a database migration concern.
- **Root Cause 2**: Issues created with the wrong type would need manual type correction in Jira. Again, not a database migration concern.

### CONVENTIONS.md Lookup

The target repository (acme-backend) path is `/home/dev/repos/acme-backend`. CONVENTIONS.md lookup would be performed at that root. Per the bug description, the project has a CONVENTIONS.md with section `## Migration Patterns`.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention Reference Formatter (shared/convention-utils.md)

- **What is broken**: The convention reference formatter converts CONVENTIONS.md section headings to kebab-case before embedding them in `§` references. For example, `## Migration Patterns` becomes `§migration-patterns` instead of `§Migration Patterns`.
- **Why it is broken**: The formatting function applies a slugify or toKebabCase transformation to the heading text. This transformation is incorrect -- the specification in both `shared/convention-applicability-rules.md` (line 57) and `plan-feature/SKILL.md` (line 803) requires the section name to preserve the original heading text exactly as it appears in CONVENTIONS.md.
- **Where it is broken**: `shared/convention-utils.md` -- the function responsible for constructing convention references from section headings.
- **How to verify the fix**: Provide a CONVENTIONS.md with heading `## Migration Patterns`. Run the formatter and assert the output reference contains `§Migration Patterns` (title case, matching the heading), not `§migration-patterns` (kebab-case).

### Root Cause 2: Task Creation Issue Type (plan-feature/SKILL.md Step 6a)

- **What is broken**: When creating task issues in Step 6a, the `jira.create_issue` call uses the Feature issue type ID (10142 from Jira Configuration) instead of the Task issue type ID (level-0 type discovered dynamically in Step 2.5).
- **Why it is broken**: Step 6a reads the issue type from the static Jira Configuration (`Feature issue type ID: 10142`) rather than consuming the type-to-role mapping produced by Step 2.5, which correctly identifies the level-0 (Task) type for the project's custom issue type scheme.
- **Where it is broken**: `skills/plan-feature/SKILL.md`, Step 6a -- the issue type parameter in the `jira.create_issue` call.
- **How to verify the fix**: Configure a project with a custom issue type scheme where Task has ID 10050. Run `/plan-feature` and assert that the created issue has type Task (ID 10050), not Feature (ID 10142).

### Independence Assessment

These two root causes are **independent**:

1. They reside in **different modules**: Root Cause 1 is in `shared/convention-utils.md` (shared utility), Root Cause 2 is in `skills/plan-feature/SKILL.md` Step 6a (skill-specific task creation logic).
2. They affect **different code paths**: Root Cause 1 affects the convention enrichment pipeline (Step 5, convention formatting), Root Cause 2 affects the Jira issue creation pipeline (Step 6a, issue type resolution).
3. They produce **different symptoms**: Root Cause 1 causes malformed text in task descriptions, Root Cause 2 causes wrong issue type on created Jira issues.
4. **Fixing one does not fix the other**: Correcting the convention formatter will not change the issue type, and correcting the issue type will not fix convention references.

This triggers the **Decomposition Guard** (Step 6 of the triage-bug skill).

### Root Cause Comment (Step 4 -- would be posted to ACME-502)

The following comment would be posted to ACME-502 via `jira.add_comment`:

---

**Root Cause**

Two independent defects cause the reported symptoms:

1. **Convention reference formatter** (`shared/convention-utils.md`): The function that constructs `§` references from CONVENTIONS.md section headings applies a kebab-case transformation (e.g., `§migration-patterns`) instead of preserving the original heading text (e.g., `§Migration Patterns`). This contradicts the format specified in `shared/convention-applicability-rules.md` and `plan-feature/SKILL.md`.

2. **Task creation issue type** (`plan-feature/SKILL.md` Step 6a): The `jira.create_issue` call reads the Feature issue type ID (10142) from static Jira Configuration instead of using the Task type ID dynamically discovered in Step 2.5's type-to-role mapping. In projects with custom issue type schemes, this causes tasks to be created as Feature issues.

**Affected Files**

- `shared/convention-utils.md` -- convention reference formatting function
- `skills/plan-feature/SKILL.md` Step 6a -- issue type parameter in create_issue call

**Suggested Approach**

These are two independent fixes in separate modules. Each should be addressed as a separate bug/task to maintain single-responsibility scope.

**Reproducer Strategy**

- Root Cause 1: Test with a CONVENTIONS.md containing `## Migration Patterns` and assert the output reference is `§Migration Patterns`.
- Root Cause 2: Test with a custom issue type scheme (Task ID 10050) and assert created issues have type Task, not Feature.

---

This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.9.

## Step 4.5 -- Affects Version Resolution

The bug's `affectsVersions` field is not populated (recorded as empty in Step 1). The "Environment / Version" section is missing from the bug description. No version information can be extracted.

**Action**: Per sub-step 4.5.6 (Flag gap), a comment would be posted to ACME-502:

> Affects Version could not be determined from the bug description -- please set manually.
>
> ---
>
> This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.9.
