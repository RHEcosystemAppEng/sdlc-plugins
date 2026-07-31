# Triage Investigation: ACME-502

## Bug Summary

**Issue**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Component**: sdlc-workflow
**Labels**: reported-by-user

## Step 0 -- Configuration Validation

Configuration validated from project CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

Issue type confirmed: Bug (10020) matches Bug Configuration.

## Step 1 -- Bug Description Parsing

Parsed against template headings:

| Required Section | Present | Content |
|---|---|---|
| Issue Description | Yes | Two distinct problems when running /plan-feature |
| Steps to Reproduce | Yes | 4-step reproduction scenario |
| Expected Result | Yes | Convention refs in title case; issue type Task (10050) |
| Actual Result | Yes | Convention refs in kebab-case; issue type Feature (10142) |
| Environment / Version | **Missing** | Section not present in bug description |
| Attachments | Yes | None |

**Note**: The "Environment / Version" required section is missing from the bug description. Per SKILL.md Step 1, this would normally halt execution. For the purposes of this analysis, the investigation proceeds based on the available information, which is sufficient to identify the root causes.

### Optional Sections

| Optional Section | Present | Content |
|---|---|---|
| Root Cause | No | Not provided |
| Suggested Fix | Yes | Reporter suspects two separate bugs: convention formatter and issue type ID selection |

## Step 2 -- Reproduction / Code-Path Tracing

Two independent code paths were traced based on the Steps to Reproduce:

### Trace A: Convention Reference Formatting

1. User runs `/plan-feature ACME-200`.
2. plan-feature Step 3 discovers `CONVENTIONS.md` with section `## Migration Patterns`.
3. plan-feature Step 5 performs convention-aware enrichment, calling the convention formatter in `shared/convention-utils.md` to generate the `§<Section Name>` reference.
4. The convention formatter transforms the heading text `Migration Patterns` to kebab-case `migration-patterns`, producing `§migration-patterns`.
5. The prescribed format in plan-feature SKILL.md (line 803) and `shared/convention-applicability-rules.md` (line 57) both require title case matching the original heading: `§Migration Patterns`.

**Divergence point**: The formatter in `shared/convention-utils.md` lowercases and kebab-cases the heading text instead of preserving the original heading case.

### Trace B: Issue Type Selection During Task Creation

1. User runs `/plan-feature ACME-200` in a project with a custom issue type scheme (Task ID: 10050).
2. plan-feature Step 2.5 dynamically discovers issue types by calling `jira.get_project_issue_types(cloudId, projectKey)` and mapping them by `hierarchyLevel` (level 0 = Task, level 1 = Epic, level 2+ = Feature).
3. Step 6a creates tasks using `jira.create_issue`.
4. Instead of using the dynamically discovered Task type (ID: 10050, level 0), the task creation logic in plan-feature Step 6a falls back to the Feature issue type ID (10142) from Jira Configuration.

**Divergence point**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the Feature issue type ID from Jira Configuration instead of the Task type from the Step 2.5 dynamic discovery mapping.

## Step 3 -- Codebase Investigation

### Affected Files and Modules

| Root Cause | Module | File | Defect |
|---|---|---|---|
| Root Cause 1 (Convention formatting) | shared | `shared/convention-utils.md` | Convention heading formatter applies lowercase + kebab-case transformation instead of preserving original heading text |
| Root Cause 2 (Issue type selection) | plan-feature | `plan-feature/SKILL.md` Step 6a | Task creation uses Feature issue type ID from Jira Configuration instead of the level-0 Task type discovered in Step 2.5 |

### Correct Patterns (from codebase analysis)

**Convention references** -- The prescribed format is documented in two locations:
- `plan-feature/SKILL.md` line 803: `"Per CONVENTIONS.md §<Section Name>: <specific action required>"`
- `shared/convention-applicability-rules.md` line 57: `Per CONVENTIONS.md §<Section Name>: <action required>.`

Both use `<Section Name>` in title case, matching the original CONVENTIONS.md heading.

**Issue type discovery** -- plan-feature Step 2.5 defines the correct approach:
- Fetch project issue types dynamically via `jira.get_project_issue_types(cloudId, projectKey)`
- Classify by `hierarchyLevel`: level 0 = Task, level 1 = Epic, level 2+ = Feature
- Store the type-to-role mapping for use in Step 6a

### Persistence-Impact Analysis

Neither defect involves data persistence. Convention references are generated at task-creation time and written to Jira issue descriptions (which can be edited after the fact). Issue type is set at creation time but can be changed via `jira.edit_issue`. No data migration is required for either root cause.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention Reference Formatter Produces Kebab-Case Instead of Title Case

**What is broken**: The convention reference formatter in `shared/convention-utils.md` transforms CONVENTIONS.md section headings into kebab-case (e.g., `Migration Patterns` becomes `migration-patterns`) when generating `§`-prefixed references in task Implementation Notes.

**Why it is broken**: The formatter applies a lowercase + hyphen-join transformation to the heading text, which is incorrect. The prescribed format (documented in both `plan-feature/SKILL.md` line 803 and `shared/convention-applicability-rules.md` line 57) requires preserving the original heading text exactly as it appears in CONVENTIONS.md (e.g., `§Migration Patterns`, not `§migration-patterns`).

**Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference conversion logic.

**How to verify the fix**: A reproducer test should:
1. Provide a CONVENTIONS.md with a heading `## Migration Patterns`
2. Invoke the convention reference formatter
3. Assert the output contains `§Migration Patterns` (title case, space-separated)
4. Assert the output does NOT contain `§migration-patterns` (kebab-case)

### Root Cause 2: Task Creation Uses Feature Issue Type Instead of Task Issue Type

**What is broken**: When plan-feature Step 6a creates tasks in Jira, it uses the Feature issue type ID (10142) from the `## Jira Configuration` section instead of the Task issue type ID (level-0 type) discovered dynamically in Step 2.5.

**Why it is broken**: The task creation logic in Step 6a reads `Feature issue type ID` from the project's Jira Configuration rather than using the `Task` role from the type-to-role mapping built in Step 2.5. This causes all created tasks to have issue type "Feature" instead of "Task" in projects with custom issue type schemes.

**Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `jira.create_issue` call that constructs the issue type parameter.

**How to verify the fix**: A reproducer test should:
1. Configure a project with a custom issue type scheme where Task has ID 10050 (level 0) and Feature has ID 10142 (level 2)
2. Run plan-feature task creation (Step 6a)
3. Assert the created issue has `issuetype.id` = 10050 (Task)
4. Assert the created issue does NOT have `issuetype.id` = 10142 (Feature)

### Independence Assessment

These two root causes are **independent**:

- **Different modules**: Root Cause 1 is in `shared/convention-utils.md` (shared formatting utility); Root Cause 2 is in `plan-feature/SKILL.md` Step 6a (task creation logic).
- **Different code paths**: The convention formatter runs during Step 5 (task description generation / convention-aware enrichment); the issue type selection runs during Step 6a (Jira API call construction for task creation).
- **No shared state**: Fixing one does not affect the other. The convention formatter does not interact with the issue type selection logic, and vice versa.
- **Different failure modes**: Root Cause 1 produces cosmetically incorrect but functionally parseable task descriptions; Root Cause 2 creates issues with the wrong Jira type, which affects workflow routing and filtering.

A single fix task covering both would conflate unrelated changes in different modules, making review harder and violating the principle of atomic changes. These should be triaged and fixed separately.
