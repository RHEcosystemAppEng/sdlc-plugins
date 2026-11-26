# Triage Investigation — ACME-502

**Bug**: [ACME-502](https://mock-jira.example.com/browse/ACME-502) — Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow
**Labels**: reported-by-user
**Skill**: sdlc-workflow/triage-bug (simulated — no Jira, Serena, or other external calls made)

---

## Step 0 – Configuration Validation

Source: `claude-md-bug-config.md` (mock project CLAUDE.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (serena_backend, /home/dev/repos/acme-backend) | Present |
| Project key | ACME | Present |
| Cloud ID | mock-cloud-id-for-eval | Present |
| Code Intelligence section | Present (no Serena servers configured, so Read/Grep/Glob fallback applies) | Present |
| Bug issue type ID | 10020 | Present |
| Bug template path | docs/templates/bug-template.md (mock: `bug-template-mock.md`) | Present |
| Bug-to-Task link type | Blocks | Present |

Result: configuration is valid, so triage continues.

## Step 0.5 – Jira Access

Simulated. The eval says not to use Jira, so every Jira operation below is written to this file and not executed.

## Step 1 – Fetch Bug

- Issue type check: ACME-502 has issue type Bug (ID 10020). This matches the configured **Bug issue type ID** 10020.
- Description parsed against the template headings:

| Template section | Heading | Found |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **No** |
| Attachments | `### **Attachments**` | Yes ("None.") |
| Root Cause (optional) | `### **Root Cause**` | No |
| Suggested Fix (optional) | `### **Suggested Fix**` | Yes |

> **Template compliance note:** The bug has no `### **Environment / Version**` section. Strictly, Step 1 of the skill says to stop and report:
> "Bug ACME-502 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."
> This eval scenario asks for the investigation and decomposition-guard path, so the triage continues with this gap recorded. In a live run the user would be told about the missing section first. Step 4.5 would also flag the gap ("Affects Version could not be determined from the bug description — please set manually.").

**Metadata**: no Affects Version/s set. The component `sdlc-workflow` points the investigation at the sdlc-workflow plugin skills and shared modules.

## Step 2 – Reproduce/Trace

The Steps to Reproduce call a skill (`/plan-feature ACME-200`) against a configured Jira project. This cannot be run read-only, so **code-path tracing** was used.

Entry point: `/plan-feature` → task description generation (Step 5, convention enrichment) → task creation in Jira (Step 6a).

The bug reports two symptoms. They were traced on their own and do not share a code path:

| # | Symptom | Where behavior diverges |
|---|---|---|
| A | Convention references come out as `§migration-patterns` (kebab-case) instead of `§Migration Patterns` | The convention reference formatter in `shared/convention-utils.md` |
| B | Task created as Feature (ID 10142) instead of Task (ID 10050) | Task creation logic in `plan-feature/SKILL.md` Step 6a |

## Step 3 – Codebase Investigation

No Serena instance is configured (Code Intelligence: "No Serena MCP servers are configured"), so the Read/Grep/Glob fallback was used on the sdlc-workflow plugin.

### Root cause path A — convention reference formatting

- **Module**: `plugins/sdlc-workflow/shared/convention-utils.md` (the convention reference formatter)
- **Consumers**: `plan-feature/SKILL.md` Step 5 (Convention enrichment, the `"Per CONVENTIONS.md §<Section Name>: ..."` line) and the Applicability Rationale format in `shared/convention-applicability-rules.md`.
- **Expected contract**: the docs require the section reference to be the heading text as written. Both `plan-feature/SKILL.md` (Step 5, "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.") and `shared/convention-applicability-rules.md` ("Per CONVENTIONS.md §<Section Name>", example "§Migration Patterns") use the original title-case heading.
- **Defect**: the formatter turns the heading into a slug (lowercase, spaces replaced with hyphens, like a Markdown anchor). It then puts that slug after `§` instead of the original heading text. `## Migration Patterns` becomes `§migration-patterns`.
- **Blast radius**: every convention reference written into Implementation Notes by plan-feature. Any other skill that uses the shared formatter (for example verify-pr upgrade evidence, which uses the same `§...` format through the applicability rules) is affected too.
- **Persistence impact**: none. The output is generated text in new Jira task descriptions, and no database is written. Tasks already created keep the malformed references, but no data migration applies.

### Root cause path B — wrong issue type at task creation

- **Module**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a ("Create the tasks"), the `jira.create_issue` call.
- **Expected contract**: Step 2.5 ("Discover Project Issue Types") finds the project's issue types and maps the `hierarchyLevel` 0 type to the **Task** role. Step 6a should use that discovered Task type ID (10050 in the reproducer's custom scheme).
- **Defect**: Step 6a takes the issue type for created tasks from the **Feature issue type ID** in `## Jira Configuration` (`Feature issue type ID: 10142`). It ignores the Task type found in Step 2.5. Projects whose Task ID happens to match the default don't show the problem. With a custom issue type scheme (Task = 10050), every task is created as a Feature (10142).
- **Blast radius**: issue type selection for every task plan-feature creates. Epic creation (6a.0), task description generation, and convention formatting are not affected.
- **Persistence impact**: none in code. Issues already created with the wrong type must be changed by hand in Jira. No repository data migration applies.

### Independence analysis

| Criterion | Root cause A | Root cause B |
|---|---|---|
| File/module | `shared/convention-utils.md` | `plan-feature/SKILL.md` Step 6a |
| Workflow stage | Task description generation (Step 5) | Jira issue creation (Step 6a) |
| Data involved | CONVENTIONS.md section headings | Jira Configuration / discovered issue type IDs |
| Shared symbol or call chain | None | None |
| Fixing one fixes the other? | No | No |
| Can occur without the other? | Yes (any project with CONVENTIONS.md) | Yes (any project with a custom issue type scheme) |

The two defects have **no shared code path, input, or symbol**. They happened to show up in the same `/plan-feature` run, and that is the only link. This matches the reporter's Suggested Fix ("These are likely two separate bugs").

### Test patterns for reproducers

- Path A: skill evals under `evals/plan-feature/`. Assert that Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns` and do not contain `§migration-patterns`.
- Path B: plan-feature eval with a mock project whose issue types include Task = 10050 and Feature = 10142. Assert that the recorded `create_issue` call uses issue type 10050 (Task), not 10142.

## Step 4 – Root Cause Analysis

**Two independent root causes:**

1. **Convention reference formatter slugifies headings** (`shared/convention-utils.md`)
   - *What*: `§` references are written as kebab-case slugs.
   - *Why*: the formatter applies anchor-style normalization (lowercase + hyphenate) instead of keeping the heading text as written.
   - *Where*: the convention reference formatting logic in `shared/convention-utils.md`, used by plan-feature Step 5 convention enrichment.
   - *Verify*: with a CONVENTIONS.md containing `## Migration Patterns`, the generated Implementation Notes must contain `§Migration Patterns`.

2. **Task creation uses the Feature issue type ID** (`plan-feature/SKILL.md` Step 6a)
   - *What*: tasks are created with issue type Feature (10142).
   - *Why*: Step 6a reads `Feature issue type ID` from Jira Configuration instead of the Task-role type found in Step 2.5.
   - *Where*: the `jira.create_issue` call in `plan-feature/SKILL.md` Step 6a.
   - *Verify*: in a project where Task = 10050, created tasks must have issue type ID 10050.

**Root cause comment (would be posted to ACME-502, ADF, with Comment Footnote — NOT posted):**

> **Root Cause**: ACME-502 has two independent defects. (1) The convention reference formatter in `shared/convention-utils.md` turns CONVENTIONS.md headings into slugs (`§migration-patterns`) instead of keeping the heading text (`§Migration Patterns`). (2) `plan-feature/SKILL.md` Step 6a creates tasks with the configured Feature issue type ID (10142) instead of the Task issue type found in Step 2.5 (10050 in custom schemes).
> **Affected Files**: `plugins/sdlc-workflow/shared/convention-utils.md` (convention reference formatter); `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (Step 6a, `jira.create_issue`).
> **Suggested Approach**: (1) Keep the heading text as written when building `§<Section Name>` references. (2) Use the Task-role issue type ID from Step 2.5 when creating tasks in Step 6a.
> **Reproducer Strategy**: (1) Eval asserting `§Migration Patterns` appears in Implementation Notes. (2) Eval with a custom issue type scheme asserting tasks are created with type ID 10050.
> ---
> This comment was AI-generated by sdlc-workflow/triage-bug v0.14.0.

## Step 4.5 – Affects Version Resolution

No `affectsVersions` set, and there is no Environment / Version section to take a version from. Gap flag (would be posted, NOT posted):

> "Affects Version could not be determined from the bug description — please set manually." + Comment Footnote

## Step 6 – Decomposition Guard triggered

The investigation found **multiple independent fixes in different modules, each for a separate root cause**. This is not one defect showing up in several files. Under Step 6 the skill must not quietly create one Task that bundles unrelated fixes. Task generation (Steps 5, 5b, 5c) is **on hold until the user chooses**. See `decomposition-guard.md` for the prompt.

- If the user picks **Proceed**: create one Task (`ai-generated-jira` label, Target Branch `main`). Its first two acceptance criteria are the two reproducer tests, followed by both fixes and a no-regression check. It also gets a Bug Context section. Then link it "Blocks" → ACME-502 and post the digest comment.
- If the user picks **Split** (recommended): stop and suggest creating two separate Bugs. Each is then triaged on its own with `/triage-bug`.
