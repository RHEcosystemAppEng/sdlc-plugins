# Triage Investigation — ACME-502

**Bug**: [ACME-502](https://mock-jira.example.com/browse/ACME-502) — Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow
**Labels**: reported-by-user
**Affects Version/s**: not set

---

## Step 0 – Configuration Validation

Source: `claude-md-bug-config.md` (project CLAUDE.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (serena_backend, /home/dev/repos/acme-backend) | present |
| Project key | ACME | present |
| Cloud ID | mock-cloud-id-for-eval | present |
| Code Intelligence | section present (no Serena servers configured) | present |
| Bug issue type ID | 10020 | present |
| Bug template path | docs/templates/bug-template.md (mock: `bug-template-mock.md`) | present |
| Bug-to-Task link type | Blocks | present |

Configuration is complete. Proceeding.

## Step 1 – Fetch Bug (simulated from `bug-issue-multi-root-cause.md`)

- **Issue type check**: issue type ID 10020 == Bug issue type ID 10020 — valid Bug.
- **Section parsing** (against template heading formats):

| Template section | Required? | Found in ACME-502 |
|---|---|---|
| Issue Description | Required | yes |
| Steps to Reproduce | Required | yes |
| Expected Result | Required | yes |
| Actual Result | Required | yes |
| Environment / Version | Required | **no** |
| Attachments | Required | yes ("None.") |
| Root Cause | Optional | no |
| Suggested Fix | Optional | yes |

> **Note:** the `### **Environment / Version**` section is missing. In a live run,
> Step 1 of the skill would stop here and report:
> "Bug ACME-502 is missing required sections: Environment / Version. The bug
> description does not follow the template at docs/templates/bug-template.md."
> Per the eval scenario instructions, the investigation continues so that the
> Decomposition Guard (Step 6) can be shown. The missing section also means
> Step 4.5 could not extract an Affects Version (gap would be flagged on the Bug).

## Step 2 – Reproduce / Trace

The bug is about skill behavior (Markdown skill definitions), so it cannot be run as a
command. Code-path tracing from the entry point `/plan-feature ACME-200` was used instead.

The Steps to Reproduce test two **unrelated observations** on one generated task:

- (a) Convention references in Implementation Notes
- (b) The Jira issue type of the created task

The two observations follow separate execution paths inside `/plan-feature`:

```
/plan-feature ACME-200
 ├── Task description generation (Step 5: Implementation Notes)
 │     └── convention reference formatting  ──► shared/convention-utils.md      [Observation (a)]
 └── Jira task creation (Step 6a: jira.create_issue)
       └── issue type selection             ──► plan-feature/SKILL.md Step 6a   [Observation (b)]
```

Neither path's output feeds into the other: the formatter produces description text,
and Step 6a picks the issue type from configuration or issue-type discovery. Fixing one
does not change the other's behavior.

## Step 3 – Codebase Investigation

No Serena instance is configured (Code Intelligence section), so Read/Grep/Glob were used.

### Root cause path 1 — convention reference formatter

- **Module**: `plugins/sdlc-workflow/skills/shared/convention-utils.md` (convention formatter)
- **Behavior**: when a `CONVENTIONS.md` heading (e.g. `## Migration Patterns`) is turned
  into a `§` reference for Implementation Notes, the formatter normalizes the heading
  into a slug (lowercase + spaces replaced with hyphens) and outputs `§migration-patterns`.
- **Expected**: the reference keeps the heading text exactly as written:
  `§Migration Patterns`.
- **Consumers**: any skill that writes convention references into task descriptions
  (plan-feature Implementation Notes; triage-bug / triage-security task generation
  through the shared template).

### Root cause path 2 — task issue type selection

- **Module**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a ("Create the tasks")
- **Behavior**: Step 6a calls `jira.create_issue` but does not explicitly tie the
  `issuetype` to the Task type (hierarchyLevel 0) found by the earlier
  "Dynamic issue type discovery" step. The only issue type ID in Jira Configuration
  is `Feature issue type ID: 10142`, so task creation falls back to that value.
  As a result, tasks are created as Feature (10142) instead of Task (10050) in
  projects with a custom issue type scheme.
- **Expected**: Step 6a uses the discovered Task issue type ID (10050 in the reproduction).

### Persistence-impact analysis

- Path 1: description text written into Jira issue descriptions at creation time.
  There is no database. Tasks already created keep the malformed references; they can
  be corrected by hand if needed. No data migration applies.
- Path 2: issues already created with the wrong type must have their type changed by
  hand in Jira. No data migration applies.

### Test patterns

- Skill-level behavior is checked through `evals/` scenarios (e.g. `evals/plan-feature/`).
  Each fix would need its own reproducer eval scenario.

## Step 4 – Root Cause Analysis

The investigation found **two independent root causes**, not one defect showing up in
several places.

### Root Cause 1 — Malformed convention references

| Aspect | Finding |
|---|---|
| What | Convention references in Implementation Notes use kebab-case slugs (`§migration-patterns`) |
| Why | The convention formatter slugifies headings (lowercase + hyphenate) instead of keeping the heading text |
| Where | `shared/convention-utils.md` — convention reference formatting logic |
| Verify | Reproducer: with `CONVENTIONS.md` containing `## Migration Patterns`, the generated Implementation Notes contain `§Migration Patterns` and do not contain `§migration-patterns` |

### Root Cause 2 — Wrong issue type on created tasks

| Aspect | Finding |
|---|---|
| What | Tasks are created with issue type Feature (10142) |
| Why | Step 6a takes the issue type from `Feature issue type ID` instead of the discovered Task-level (hierarchyLevel 0) issue type ID |
| Where | `plan-feature/SKILL.md` Step 6a — `jira.create_issue` issue type selection |
| Verify | Reproducer: with a custom scheme where Task = 10050, the `create_issue` call for each task uses issuetype 10050 and never 10142 |

### Independence assessment

| Criterion | Root Cause 1 | Root Cause 2 |
|---|---|---|
| Module | `shared/convention-utils.md` | `plan-feature/SKILL.md` Step 6a |
| Concern | Text formatting of description content | Jira API field selection |
| Trigger condition | `CONVENTIONS.md` present | Custom issue type scheme |
| Shared code path | none | none |
| Fix affects the other? | no | no |
| Blast radius | All skills using the shared formatter | plan-feature only |

The two defects share only the entry point (`/plan-feature`) and the artifact they show
up on (the generated task). Each has its own trigger, its own module, and its own fix.
This matches the reporter's Suggested Fix ("These are likely two separate bugs").

**Conclusion**: this meets the Step 6 Decomposition Guard trigger. These are multiple
independent fixes across different modules, each for a distinct root cause. A single
bundled Task should not be created silently. See `decomposition-guard.md`.

### Root cause comment (would be posted to ACME-502 via `jira.add_comment`, ADF, with Comment Footnote)

> **Root Cause**: Two independent defects.
> (1) The convention formatter in `shared/convention-utils.md` slugifies `CONVENTIONS.md`
> headings, which produces `§migration-patterns` instead of `§Migration Patterns`.
> (2) plan-feature Step 6a creates tasks with the Feature issue type ID (10142)
> instead of the discovered Task issue type ID (10050 in custom schemes).
>
> **Affected Files**: `plugins/sdlc-workflow/skills/shared/convention-utils.md`
> (convention reference formatting); `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
> (Step 6a – Create the tasks).
>
> **Suggested Approach**: (1) Keep the original heading text when building `§`
> references. (2) Have Step 6a use the hierarchyLevel-0 issue type ID from dynamic
> issue type discovery for `issuetype`, never the Feature issue type ID.
>
> **Reproducer Strategy**: one eval scenario per defect. One checks the generated
> Implementation Notes for `§Migration Patterns`. The other checks the `create_issue`
> issuetype under a custom scheme (Task = 10050).
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/RHEcosystemAppEng/sdlc-plugins) v{version}.

## Step 4.5 – Affects Version

No `Environment / Version` section and no existing Affects Version, so no version can be
extracted. The gap comment would be posted: "Affects Version could not be determined
from the bug description — please set manually."

## Steps 5 / 5b / 5c – Deferred

Task generation, linking (Blocks), and digest posting are **on hold until the user answers**
the Decomposition Guard prompt. If the user chooses Proceed, one Task covering both
fixes is created, with one reproducer criterion per root cause first in the list. If the
user chooses Split, no Task is created and the user is asked to file two separate Bugs.
