# Investigation — ACME-502

**Bug**: [ACME-502](https://mock-jira.example.com/browse/ACME-502) — Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow
**Labels**: reported-by-user
**Affects Version/s**: not set

---

## Step 0 — Configuration Validation

Source: `claude-md-bug-config.md` (mock project CLAUDE.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (`serena_backend`, `/home/dev/repos/acme-backend`) | present |
| Project key | ACME | present |
| Cloud ID | mock-cloud-id-for-eval | present |
| Code Intelligence | section present; no Serena servers configured | present |
| Bug issue type ID | 10020 | present |
| Bug template path | docs/templates/bug-template.md (mocked by `bug-template-mock.md`) | present |
| Bug-to-Task link type | Blocks | present |

Configuration is complete. Code Intelligence says no Serena servers are configured, so the investigation used Read, Grep and Glob instead.

## Step 1 — Fetch Bug and Validate

- **Issue type check**: the issue type ID is 10020 and the Bug issue type ID is also 10020. It matches.
- **Section parsing** (heading formats taken from the bug template):

| Required Section | Present | Content (condensed) |
|---|---|---|
| Issue Description | yes | Two problems when running `/plan-feature`: malformed convention references; wrong issue type |
| Steps to Reproduce | yes | Custom issue type scheme (Task ID 10050), CONVENTIONS.md with `## Migration Patterns`, run `/plan-feature ACME-200`, inspect the task |
| Expected Result | yes | `§Migration Patterns`; issue type Task (10050) |
| Actual Result | yes | `§migration-patterns`; issue type Feature (10142) |
| Environment / Version | **no** | — |
| Attachments | yes | None |

| Optional Section | Present |
|---|---|
| Root Cause | no |
| Suggested Fix | yes. The reporter suspects two separate bugs: the heading formatter and the issue-type ID lookup |

> **Note:** The required `### **Environment / Version**` section is missing. Under a strict reading of Step 1, the skill would stop here and tell the user:
> "Bug ACME-502 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."
> This eval tests the decomposition guard, so the investigation continues as instructed. The missing section also matters for Step 4.5: no version can be extracted, so the Affects Version gap would be flagged (sub-step 4.5.6).

## Step 2 — Reproduce / Trace

This bug is in skill and documentation logic, so it cannot be reproduced by running a command. The investigation traced the code paths instead.

Entry point: running `/plan-feature ACME-200` with (a) a `CONVENTIONS.md` that contains `## Migration Patterns` and (b) a custom issue type scheme where Task = 10050.

### Trace A — Convention reference rendering

1. plan-feature Step 3 (CONVENTIONS.md lookup) reads the target repo's `CONVENTIONS.md` and collects its section headings.
2. plan-feature Step 5 (convention enrichment) calls the shared convention formatter in `shared/convention-utils.md` to turn each matched heading into a reference string.
3. The formatter normalizes the heading into a slug: it lowercases it and replaces spaces with hyphens (`Migration Patterns` becomes `migration-patterns`). It then puts `§` in front.
4. The expected format is defined in `plan-feature/SKILL.md` (around line 829: `"Per CONVENTIONS.md §<Section Name>: ..."`; example on line 838: `§Migration Patterns`) and in `shared/convention-applicability-rules.md` (lines 52–64). Both require the heading text exactly as written.
5. **Divergence**: the formatter outputs an anchor-style slug where it should keep the heading text unchanged.

### Trace B — Task issue type selection

1. plan-feature Step 2.5 discovers the project's issue types and classifies them by `hierarchyLevel`. The level-0 issue type should be resolved as Task (10050 in this project).
2. plan-feature Step 6a ("Create the tasks") calls `jira.create_issue` for each task.
3. The issue type that Step 6a passes to `jira.create_issue` comes from the `Feature issue type ID` in Jira Configuration (10142). It should come from the Task issue type ID that Step 2.5 discovered.
4. **Divergence**: tasks are created with the Feature issue type (10142) instead of Task (10050). The bug is only visible in projects with a custom issue type scheme. In schemes where the default would otherwise be picked, nobody notices it.

### Reproduction outcome

Both symptoms are confirmed by code-path tracing. **The two traces share no code.** Trace A is limited to the convention formatter and the Step 5 enrichment that uses it. Trace B is limited to the issue-type resolution between Step 2.5 and Step 6a.

## Step 3 — Codebase Investigation

### Affected files and symbols

| # | File / Module | Symbol / Section | Defect |
|---|---|---|---|
| 1 | `plugins/sdlc-workflow/skills/shared/convention-utils.md` | Convention reference formatter (heading → `§` reference) | Lowercases and kebab-cases the heading instead of keeping its original text |
| 2 | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Step 6a — Create the tasks (`jira.create_issue` issue type argument) | Reads `Feature issue type ID` from Jira Configuration instead of the Task issue type ID discovered in Step 2.5 |

### Impact analysis

- **Formatter (`shared/convention-utils.md`)**: every skill that produces `Per CONVENTIONS.md §...` lines uses this formatter. That includes plan-feature Step 5 Implementation Notes, and possibly triage-bug and triage-security Implementation Notes too. It does not touch Jira issue creation.
- **Step 6a issue type**: only issue creation in plan-feature uses this. It does not touch description content or convention handling.
- **Shared state**: neither fix touches the other's files or symbols. They have no shared variables or data flow. Fixing one does not change how the other behaves, and either can ship by itself.

### Reference patterns for fixes

- Convention reference format: `shared/convention-applicability-rules.md` lines 52–64, and `plan-feature/SKILL.md` lines 829–838 (`§Migration Patterns`).
- Issue type resolution: `plan-feature/SKILL.md` Step 2.5 ("Discover Project Issue Types"), which maps hierarchyLevel 0 to Task.

### Persistence-impact analysis

There is no database persistence boundary. Both defects affect Jira content produced each time the skill runs. Data migration is not applicable. Jira issues that were already created with the wrong type or malformed references would need manual cleanup. That is outside what a code fix covers.

### CONVENTIONS.md

Neither defect needs repository conventions to inform the fix itself.

## Step 4 — Root Cause Analysis

### Root Cause 1 — Malformed convention references

- **What**: Implementation Notes contain `§migration-patterns` when they should contain `§Migration Patterns`.
- **Why**: the convention reference formatter turns headings into slugs (lowercase plus hyphens) as if it were building a URL anchor. It should keep the heading text exactly as written.
- **Where**: `plugins/sdlc-workflow/skills/shared/convention-utils.md`, convention reference formatter.
- **Verify**: a reproducer feeds in a CONVENTIONS.md heading `## Migration Patterns` and asserts that the generated reference is exactly `§Migration Patterns`. Before the fix the output is `§migration-patterns`.

### Root Cause 2 — Wrong issue type for created tasks

- **What**: tasks are created as Feature (10142) when they should be Task (10050).
- **Why**: Step 6a takes the `Feature issue type ID` from Jira Configuration as the issue type for `jira.create_issue`. It should use the level-0 (Task) issue type ID discovered in Step 2.5.
- **Where**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a (Create the tasks).
- **Verify**: a reproducer uses a mock project whose Task issue type ID is 10050 and asserts that the `jira.create_issue` call made by Step 6a uses issue type 10050. Before the fix it uses 10142.

### Assessment

These are **two independent root causes**:

- They are in different modules: a shared formatter utility, and the plan-feature task creation step.
- They have different causes: a string normalization error, and a configuration-key lookup error.
- They share no code path or data flow, and either can be fixed and verified without the other.
- They show up as independent symptoms in the same skill run, which is the only reason they were reported together.

This is **not** one root cause that shows up across several files. It is two separate defects. The **Decomposition Guard (Step 6) is triggered**. The prompt for the user is in `decomposition-guard.md`.

### Root cause comment (would be posted to ACME-502 via `jira.add_comment`, ADF)

> **Root Cause**: Two independent defects.
> (1) The convention reference formatter in `shared/convention-utils.md` kebab-cases and lowercases CONVENTIONS.md headings, so it produces `§migration-patterns` where it should produce `§Migration Patterns`.
> (2) plan-feature Step 6a passes the Feature issue type ID (10142) to `jira.create_issue` where it should pass the discovered Task issue type ID (10050).
>
> **Affected Files**:
> - `plugins/sdlc-workflow/skills/shared/convention-utils.md` — convention reference formatter
> - `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Step 6a, issue type for task creation
>
> **Suggested Approach**:
> (1) Keep the original heading text when building `§` references.
> (2) Resolve the issue type for created tasks from the hierarchyLevel-0 type discovered in Step 2.5, not from `Feature issue type ID`.
>
> **Reproducer Strategy**:
> (1) Assert that `## Migration Patterns` produces `§Migration Patterns`.
> (2) With Task = 10050, assert that the issue type of the created issue is 10050.
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.

## Step 4.5 — Affects Version

The bug has no `### **Environment / Version**` section, so no version can be extracted. A gap comment would be posted (sub-step 4.5.6):
"Affects Version could not be determined from the bug description — please set manually." (with the Comment Footnote).

## Next

Task generation (Step 5) is held until the user answers the decomposition guard prompt (Step 6). If the user chooses **Split**, the skill stops and recommends filing two separate Bugs. If the user chooses **Proceed**, one Task covering both fixes is created and linked to ACME-502 with link type Blocks.
