# Triage Investigation — ACME-502

**Bug**: [ACME-502](https://mock-jira.example.com/browse/ACME-502) — Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow
**Labels**: reported-by-user
**Skill**: sdlc-workflow/triage-bug v0.13.10 (eval run — no Jira/Serena calls made)

---

## Step 0 – Configuration Validation

Source: `claude-md-bug-config.md`

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (`serena_backend`, `/home/dev/repos/acme-backend`) | Present |
| Project key | ACME | Present |
| Cloud ID | mock-cloud-id-for-eval | Present |
| Code Intelligence | Section present — "No Serena MCP servers are configured" | Present |
| Bug issue type ID | 10020 | Present |
| Bug template path | docs/templates/bug-template.md (mocked by `bug-template-mock.md`) | Present |
| Bug-to-Task link type | Blocks | Present |

Configuration is valid. Note: the Registry lists a Serena instance `serena_backend` but
Code Intelligence says no Serena servers are configured — investigation therefore uses the
Read/Grep/Glob fallback.

## Step 1 – Fetch Bug and Validate

- **Issue type**: Bug (ID 10020) — matches the configured Bug issue type ID. Valid.
- **Parsed sections** (against the template heading formats):

| Template Section | Required? | Found? |
|---|---|---|
| Issue Description | Required | Yes |
| Steps to Reproduce | Required | Yes |
| Expected Result | Required | Yes |
| Actual Result | Required | Yes |
| Environment / Version | Required | **No** |
| Attachments | Required | Yes ("None.") |
| Root Cause | Optional | No |
| Suggested Fix | Optional | Yes — reporter says "These are likely two separate bugs" |

**Template gap:** the required `### **Environment / Version**` section is missing. Under a
strict reading of Step 1, triage would stop here with:

> "Bug ACME-502 is missing required sections: Environment / Version. The bug description
> does not follow the template at docs/templates/bug-template.md."

This eval asks for the investigation and decomposition outcome, so the analysis continues
below. The gap is recorded so the reporter can add it, and so Step 4.5 (Affects Version)
falls through to gap flagging (4.5.6): "Affects Version could not be determined from the bug
description — please set manually."

## Step 2 – Reproduce / Trace

The bug is in skill/documentation behavior (`/plan-feature`), so a runnable reproduction
isn't possible. I used code-path tracing instead. The entry point is `/plan-feature ACME-200`.
The reporter describes two symptoms, and they diverge at two **separate** points in the
pipeline:

| # | Symptom | Pipeline stage where behavior diverges |
|---|---|---|
| A | Convention references come out as `§migration-patterns` (kebab-case) instead of `§Migration Patterns` | Step 5 (Generate Jira Tasks) → Implementation Notes convention-reference formatting, which delegates to the shared convention formatter |
| B | Task created with issue type Feature (10142) instead of Task (10050) | Step 6a (Create the tasks) → `jira.create_issue` call |

The two stages don't share any data. Symptom A comes from how the task *description text*
is rendered. Symptom B comes from which *issue type ID* is passed to the Jira create call.
Neither one feeds into the other.

## Step 3 – Codebase Investigation

Fallback tools (Read/Grep) were used, since no Serena instance is available.

### Root cause A — convention formatter (`shared/convention-utils.md`)

- **Location**: `plugins/sdlc-workflow/skills/shared/convention-utils.md`, the
  convention reference formatter that turns a CONVENTIONS.md heading into a `§` reference.
- **Expected contract**: `plan-feature/SKILL.md` (Step 5, convention application) requires
  that the Implementation Notes line take the form
  `"Per CONVENTIONS.md §<Section Name>: <specific action required>"`. Its worked example is
  `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
  So the section name has to be kept **verbatim**, exactly as the heading is written.
- **Defect**: the formatter normalizes the heading into a slug/anchor (lowercases it and
  replaces spaces with hyphens: `Migration Patterns` → `migration-patterns`), when it should
  emit the literal heading text. Slug-style normalization works for Markdown anchor links,
  but it's the wrong output for the `§<Section Name>` reference format.
- **Consumers**: every skill that renders convention references in Implementation Notes
  (plan-feature Step 5, and any other skill that uses the shared formatter).
- **Persistence impact**: none. The output is description text in newly generated Jira
  tasks. Tasks created earlier keep the wrong reference, but no database stores a derived
  value, so no data migration is needed. Already-created tasks can be corrected by hand if
  needed.

### Root cause B — task creation issue type (`plan-feature/SKILL.md` Step 6a)

- **Location**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, section
  `### 6a – Create the tasks`.
- **Expected contract**: Step 2.5 (Discover Project Issue Types) builds a type-to-role
  mapping (`Feature`, `Epic`, `Task` → type ID), and says explicitly that "This mapping is
  used in Steps 5 and 6 when creating Jira issues." In a custom issue type scheme, the Task
  role resolves to ID 10050.
- **Defect**: Step 6a calls `jira.create_issue` / `jira.create_subtask` without saying which
  issue type to use, and it never points to the Task entry in the Step 2.5 mapping. The only
  issue type ID in the Jira Configuration is `Feature issue type ID: 10142` (from CLAUDE.md),
  so the agent reads that configured ID and uses it for task creation. This matches the
  reporter's suggested fix ("reads Feature issue type ID instead of Task issue type ID from
  configuration") and the observed result (Feature, ID 10142).
- **Consumers**: the task-creation path in plan-feature Step 6a only. Epic creation (6a.0)
  and link creation (6b) are separate.
- **Persistence impact**: none in a database sense. Issues already created with the wrong
  type need to be re-typed in Jira by hand (Move issue), which is outside a code fix.

### Independence assessment

| Criterion | Root cause A | Root cause B |
|---|---|---|
| File / module | `shared/convention-utils.md` (shared utility) | `plan-feature/SKILL.md` Step 6a (skill-specific) |
| Pipeline stage | Description generation (Step 5) | Jira issue creation (Step 6a) |
| Data involved | CONVENTIONS.md heading text → `§` reference string | Issue type ID from config / Step 2.5 mapping |
| Fix | Keep heading text verbatim in the formatter | Use the Task type ID from the Step 2.5 type-to-role mapping in `create_issue` |
| Reproducer | Assert `§Migration Patterns` appears in Implementation Notes | Assert the created issue type ID is 10050 (Task), not 10142 |
| Can one fix be shipped without the other? | Yes | Yes |
| Shared code path? | No | No |

**Conclusion:** these are **two independent root causes** in different modules. This is not
one defect showing up in several files. It is two unrelated defects that were reported
together because they both show up during a single `/plan-feature` run. The reporter's
Suggested Fix reaches the same conclusion on its own.

## Step 4 – Root Cause Analysis (draft Jira comment — not posted)

**Root Cause**
1. *Malformed convention references*: the shared convention formatter turns CONVENTIONS.md
   headings into kebab-case slugs (`migration-patterns`) when it should keep the literal
   heading (`Migration Patterns`). That breaks the `Per CONVENTIONS.md §<Section Name>`
   contract that plan-feature defines.
2. *Wrong issue type*: plan-feature Step 6a creates tasks without using the Task type ID from
   the Step 2.5 type-to-role mapping. It falls back to the only configured ID (Feature,
   10142), so in custom issue type schemes, tasks get created as Features.

**Affected Files**
- `plugins/sdlc-workflow/skills/shared/convention-utils.md` — convention reference formatter
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — `### 6a – Create the tasks`
  (and its reliance on the `### Store the type-to-role mapping` output of Step 2.5)

**Suggested Approach**
1. Change the formatter to emit the heading text verbatim after `§` (trim it, but don't
   change case or replace characters).
2. Change Step 6a to pass the Task role's type ID from the Step 2.5 mapping explicitly to
   `jira.create_issue` (and the REST fallback `--issue-type`). It should never use
   `Feature issue type ID` for tasks.

**Reproducer Strategy**
1. Use a fixture CONVENTIONS.md containing `## Migration Patterns`. Assert that the
   generated Implementation Notes contain `§Migration Patterns` and do not contain
   `§migration-patterns`.
2. Use a mocked project issue type scheme with Task = 10050 and Feature = 10142. Assert
   that the task-creation call uses issue type ID 10050.

---
*This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.*

## Step 4.5 – Affects Version

The Environment / Version section is missing, so no version can be extracted. Per 4.5.6, I
would post this gap comment: "Affects Version could not be determined from the bug
description — please set manually." (with footnote).

## Step 5 / 6 – Next Action

Because the investigation found two independent root causes, the **Decomposition Guard
(Step 6)** comes into play before any Task is created. That way the skill doesn't silently
bundle two unrelated fixes into one Task. See `decomposition-guard.md`. No Task, link, or
digest comment has been created while the user's choice is pending.
