# Triage Investigation — ACME-502

**Bug**: [ACME-502](https://mock-jira.example.com/browse/ACME-502) — Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow
**Labels**: reported-by-user
**Skill**: sdlc-workflow/triage-bug (simulated — no Jira/Serena calls made)

---

## Step 0 — Configuration Validation

Source: `claude-md-bug-config.md`

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (serena_backend, /home/dev/repos/acme-backend) | Present |
| Project key | ACME | Present |
| Cloud ID | mock-cloud-id-for-eval | Present |
| Code Intelligence | Section present; no Serena servers configured | Present (fallback to Read/Grep/Glob) |
| Bug issue type ID | 10020 | Present |
| Bug template path | docs/templates/bug-template.md (mock: `bug-template-mock.md`) | Present |
| Bug-to-Task link type | Blocks | Present |

Result: configuration valid, proceed.

## Step 1 — Fetch Bug (simulated from `bug-issue-multi-root-cause.md`)

- Issue type check: issue type ID `10020` == Bug issue type ID `10020` — **is a Bug, proceed**.
- Section parsing against the template headings:

| Template section | Required? | Found in ACME-502? |
|---|---|---|
| `### **Issue Description**` | Required | Yes |
| `### **Steps to Reproduce**` | Required | Yes |
| `### **Expected Result**` | Required | Yes |
| `### **Actual Result**` | Required | Yes |
| `### **Environment / Version**` | Required | **No — missing** |
| `### **Attachments**` | Required | Yes ("None.") |
| `### **Root Cause**` | Optional | No |
| `### **Suggested Fix**` | Optional | Yes |

> **Template gap:** the required `Environment / Version` section is missing. Per Step 1 of
> the skill, a real run would stop here and tell the user: *"Bug ACME-502 is missing
> required sections: Environment / Version. The bug description does not follow the
> template at docs/templates/bug-template.md."* This eval scenario explicitly asks for
> the investigation and decomposition analysis, so the analysis continues below. The gap
> also means Step 4.5 could not extract a version, so an Affects Version gap comment
> would be posted (4.5.6). `affectsVersions` is not set on the issue.

## Step 2 — Reproduce / Trace

The bug is in skill instructions (markdown-driven agent behavior), so it cannot be run
directly. Code-path tracing was used instead. Entry point: `/plan-feature ACME-200`.

The two symptoms follow **two separate execution paths** inside plan-feature:

| Symptom | Trace path | Divergence point |
|---|---|---|
| (a) Convention refs render as `§migration-patterns` | plan-feature Step 4 (task generation, convention lookup) → convention reference formatting → Implementation Notes text | Convention formatter in `shared/convention-utils.md` normalizes the heading (lowercase + kebab-case) instead of keeping it verbatim |
| (b) Task created as Feature (10142) instead of Task (10050) | plan-feature Step 2.5 (issue type discovery) → Step 6a (`jira.create_issue`) | Step 6a's task creation reads `Feature issue type ID` from Jira Configuration instead of the level-0 Task type discovered in Step 2.5 |

The two paths share no code: (a) is a string-formatting concern that runs during task
*description generation*; (b) is a Jira field-selection concern that runs during task
*creation*. Neither path calls the other, and neither shares input data (CONVENTIONS.md
headings vs. Jira issue type metadata).

## Step 3 — Codebase Investigation

No Serena instance is available (Code Intelligence: none configured), so Read/Grep/Glob
fallback applies.

### Root Cause 1 — Convention reference formatter (`shared/convention-utils.md`)

- **Module**: shared convention utilities (`plugins/sdlc-workflow/shared/convention-utils.md`)
- **Contract it should follow**: plan-feature's convention guidance requires the form
  `Per CONVENTIONS.md §<Section Name>: <specific action required>` with the section
  name matching the heading exactly — e.g. `Per CONVENTIONS.md §Migration Patterns: add
  Index::create() for all FK columns.` (plan-feature `SKILL.md` ~lines 829–838; also
  `shared/convention-applicability-rules.md` lines 52–64).
- **Defect**: the formatter slugifies the heading (`Migration Patterns` → `migration-patterns`,
  lowercased and kebab-cased, i.e. an anchor-style slug) before emitting the `§` reference.
- **Effect**: Implementation Notes contain `§migration-patterns`, which does not match the
  `## Migration Patterns` heading in CONVENTIONS.md, so implementers and downstream
  verification (convention compliance checks) cannot resolve the reference.
- **Consumers to check for regression**: any skill that emits `Per CONVENTIONS.md §...`
  lines — plan-feature (Implementation Notes) and triage-bug/implement-task paths that
  reuse convention-applicability rules.

### Root Cause 2 — Task issue type selection (`skills/plan-feature/SKILL.md` Step 6a)

- **Module**: plan-feature task creation (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`,
  `### 6a – Create the tasks`, ~line 1094).
- **Contract it should follow**: Step 2.5 (`Discover Project Issue Types`) maps the
  project's issue types by `hierarchyLevel`; level `0` is the **Task** role. For ACME's
  custom scheme that is ID `10050`.
- **Defect**: Step 6a's `jira.create_issue` call does not pin the issue type to the
  level-0 Task type from Step 2.5. The only issue type ID available in Jira Configuration
  is `Feature issue type ID: 10142`, and that value is what gets used for the created
  tasks.
- **Effect**: on projects with a custom issue type scheme (where "Task" is not the default
  name/ID), tasks are created as Feature (10142) instead of Task (10050). This also breaks
  the Feature → (Epic) → Task hierarchy, since a Feature cannot be parented under a Feature/Epic.
- **Consumers to check for regression**: 6a.0 Epic creation (uses level-1 type) and
  subtask creation (`jira.create_subtask`) should be checked to confirm they also use
  discovered type IDs.

### Persistence-impact analysis

Neither defect writes to a database. Both affect artifacts at generation time:
- Root Cause 1: already-created Jira tasks carry malformed `§` references in their
  descriptions (manual cleanup or re-plan may be desired; no data migration).
- Root Cause 2: already-created issues have the wrong issue type in Jira (can be fixed
  via Jira "Move"/change-type; no data migration).

No persistence boundary found — no data migration task needed.

### CONVENTIONS.md

Target repo path from registry: `/home/dev/repos/acme-backend` — would be checked for
`CONVENTIONS.md` (not accessible in this simulated run).

## Step 4 — Root Cause Analysis

**Conclusion: two independent root causes.**

| # | What is broken | Why | Where | How to verify |
|---|---|---|---|---|
| 1 | Convention references in Implementation Notes use slug form `§migration-patterns` | Formatter lowercases and kebab-cases the CONVENTIONS.md heading instead of preserving it verbatim | `shared/convention-utils.md` (convention reference formatter) | Reproducer: given CONVENTIONS.md heading `## Migration Patterns`, the generated reference must be `§Migration Patterns` (fails today with `§migration-patterns`) |
| 2 | Tasks are created with issue type Feature (10142) | Step 6a selects the Feature issue type ID from configuration instead of the level-0 Task type discovered in Step 2.5 | `skills/plan-feature/SKILL.md` Step 6a (task creation) | Reproducer: with a custom scheme where Task = 10050, the `create_issue` payload for each task must use issue type 10050 (fails today with 10142) |

Why these are independent and not one root cause manifesting in multiple places:
- Different modules (shared utility vs. plan-feature Step 6a).
- Different phases of the workflow (description generation vs. Jira issue creation).
- Different inputs (CONVENTIONS.md headings vs. Jira issue type metadata/config).
- Fixing either one has no effect on the other; each can be fixed, tested, and released on its own.
- The reporter's Suggested Fix independently reaches the same conclusion ("These are likely two separate bugs").

This meets the Step 6 Decomposition Guard trigger (multiple independent fixes across
different modules, each addressing a distinct root cause), so a single bundled Task
should **not** be created silently. See `decomposition-guard.md`.

## Step 4.5 — Affects Version

`Environment / Version` section missing → no version extractable → would post the gap
comment: "Affects Version could not be determined from the bug description — please set
manually." (with Comment Footnote).

## Steps 5 / 5b / 5c — Deferred

Task generation, linking (Blocks: Task → ACME-502) and digest posting are held pending
the user's decomposition choice:
- **Proceed** → one Task covering both fixes, with two reproducer tests front-loaded
  as the first acceptance criteria.
- **Split** → stop; recommend filing two separate Bugs (one per root cause) and triaging
  each individually.
