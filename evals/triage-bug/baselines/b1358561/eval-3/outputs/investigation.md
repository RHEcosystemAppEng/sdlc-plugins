# Triage Investigation — ACME-502

**Bug**: [ACME-502](https://mock-jira.example.com/browse/ACME-502) — Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow
**Labels**: reported-by-user
**Skill**: sdlc-workflow/triage-bug (v0.14.0)
**Mode**: Eval / dry run — no Jira, Serena, or other external calls were made.

---

## Step 0 – Configuration Validation

Source: `claude-md-bug-config.md`

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (serena_backend, /home/dev/repos/acme-backend) | Present |
| Project key | ACME | Present |
| Cloud ID | mock-cloud-id-for-eval | Present |
| Code Intelligence | Section present (no Serena configured, fallback to Read/Grep/Glob) | Present |
| Bug issue type ID | 10020 | Present |
| Bug template path | docs/templates/bug-template.md (mock: `bug-template-mock.md`) | Present |
| Bug-to-Task link type | Blocks | Present |

Result: Configuration is valid.

Note for later: Jira Configuration defines only `Feature issue type ID: 10142`.
It does **not** define a Task issue type ID. That turns out to matter for root cause #2.

## Step 1 – Fetch Bug & Validate

- Issue type: Bug (ID 10020). Matches the configured Bug issue type ID. **Valid.**
- Sections parsed against the template headings:

| Template Section | Required? | Present in ACME-502? |
|---|---|---|
| Issue Description | Required | Yes |
| Steps to Reproduce | Required | Yes |
| Expected Result | Required | Yes |
| Actual Result | Required | Yes |
| Environment / Version | Required | **No — missing** |
| Attachments | Required | Yes ("None.") |
| Root Cause | Optional | No |
| Suggested Fix | Optional | Yes |

> **Template compliance gap:** ACME-502 has no `### **Environment / Version**`
> section. Under strict Step 1 rules, triage-bug would stop here and tell the user:
> "Bug ACME-502 is missing required sections: Environment / Version. The bug
> description does not follow the template at docs/templates/bug-template.md."
> This eval scenario says to carry on with the investigation, so the analysis below
> continues. Step 4.5 cannot extract an Affects Version and would flag the gap.

Metadata: Affects Version/s is not set. There is no version info to scope the investigation.

## Step 2 – Reproduce / Trace

These are skill and documentation defects in `/plan-feature`, so they can't be run
directly. Code-path tracing was used instead.

Entry point: `/plan-feature ACME-200`, run on a project that has a custom issue type
scheme (Task = 10050) and a `CONVENTIONS.md` with the heading `## Migration Patterns`.

The bug report describes two divergent behaviors (they were traced separately):

| # | Symptom | Expected | Actual |
|---|---|---|---|
| A | Convention reference in Implementation Notes | `§Migration Patterns` | `§migration-patterns` |
| B | Issue type of created task | Task (10050) | Feature (10142) |

### Trace A — convention references
`plan-feature/SKILL.md` (convention-matching step, "Per CONVENTIONS.md §<Section Name>")
→ the section name is passed to the convention formatter in
`shared/convention-utils.md` → the formatter lowercases and kebab-cases the heading
(slug style, like a markdown anchor) and does not keep the literal heading text →
Implementation Notes get `§migration-patterns`.
The contract in `plan-feature/SKILL.md` and `shared/convention-applicability-rules.md`
(e.g. `Per CONVENTIONS.md §Migration Patterns: ...`) requires the exact heading text.
**Behavior diverges at the formatter.**

### Trace B — task issue type
`plan-feature/SKILL.md` Step 6a ("Create the tasks") → `jira.create_issue` is called
with the issue type taken from the `Feature issue type ID` (10142) in CLAUDE.md
Jira Configuration. It should use the Task-level issue type, either from the
dynamic issue-type discovery step (hierarchyLevel 0) or from a configured Task
issue type ID. The default "Task" happens to work in projects with a standard
scheme, which hides the bug. With a custom scheme (Task = 10050), the task gets
created as a Feature.
**Behavior diverges at Step 6a issue creation.**

## Step 3 – Codebase Investigation

- Target repository: sdlc-workflow plugin (Component = sdlc-workflow). No Serena
  instance is available, so the Read/Grep/Glob fallback applies.
- Affected modules:

| Root cause | File / module | Symbol / section |
|---|---|---|
| RC-1 | `plugins/sdlc-workflow/shared/convention-utils.md` | Convention reference formatter (heading → `§<Section Name>` rendering) |
| RC-2 | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Step 6a – Create the tasks (`jira.create_issue` issue type selection) |

- Related contracts and references:
  - `plugins/sdlc-workflow/shared/convention-applicability-rules.md` sets the output
    format `Per CONVENTIONS.md §<Section Name>: <action>`, with examples using title
    case (`§Migration Patterns`, `§Commit Messages`).
  - `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` has the issue-type discovery
    step (classifies issue types by `hierarchyLevel`: 0 = Task). Its output should
    feed Step 6a.
- Coupling analysis: the two code paths share no symbol, data structure, or
  configuration value. The formatter works on CONVENTIONS.md heading text while the
  task description is being generated (Step 5-ish, description content). Step 6a
  works on Jira issue type IDs at issue-creation time. Fixing one does not touch or
  fix the other. Neither defect causes the other.
- Persistence-impact analysis: neither path writes to a database. Already-created
  Jira issues with the wrong type or malformed references would need manual
  correction in Jira. No data migration is needed.
- Existing tests / patterns: plan-feature eval scenarios under `evals/` are the
  relevant reproducer harness for both defects.

## Step 4 – Root Cause Analysis

### Root Cause 1 — Convention reference formatter slugifies headings
- **What**: Convention references in generated Implementation Notes are written
  in kebab-case (`§migration-patterns`) when they should be the literal heading
  (`§Migration Patterns`).
- **Why**: The formatter in `shared/convention-utils.md` applies slug-style
  normalization (lowercase + spaces → hyphens) to the CONVENTIONS.md heading. It
  should keep the heading text exactly as written.
- **Where**: `plugins/sdlc-workflow/shared/convention-utils.md` — convention
  reference formatter.
- **Verify**: Reproducer: a CONVENTIONS.md with `## Migration Patterns` must give
  `Per CONVENTIONS.md §Migration Patterns:` in Implementation Notes. Assert that
  `§migration-patterns` does not appear.

### Root Cause 2 — Step 6a uses Feature issue type ID for task creation
- **What**: Tasks created by `/plan-feature` get issue type Feature (10142)
  instead of Task (10050).
- **Why**: Step 6a resolves the issue type for `jira.create_issue` from the
  `Feature issue type ID` field in Jira Configuration. It does not use the
  Task-level (hierarchyLevel 0) issue type found by dynamic issue-type discovery.
- **Where**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Step 6a,
  "Create the tasks".
- **Verify**: Reproducer: with a custom issue type scheme where Task = 10050,
  the `create_issue` payload for each generated task must use issue type ID 10050.
  Assert it is not 10142.

### Independence verdict
These are **two independent root causes**. They live in different modules, run at
different phases (description content generation vs. Jira issue creation), and
need separate fixes. A fix to either one leaves the other symptom unchanged. The
reporter's Suggested Fix ("These are likely two separate bugs") agrees.
This is not one defect showing up in several files. **Step 6 Decomposition Guard
is triggered.**

### Root cause comment (would be posted to ACME-502 via `jira.add_comment`, ADF)

> **Root Cause**: ACME-502 comes from two independent defects in `/plan-feature`:
> (1) the convention reference formatter in `shared/convention-utils.md` slugifies
> CONVENTIONS.md headings (`§migration-patterns`) when it should keep the literal
> heading (`§Migration Patterns`). (2) `plan-feature/SKILL.md` Step 6a creates tasks
> using the Feature issue type ID (10142) when it should use the Task-level issue type
> (10050 in custom schemes).
>
> **Affected Files**:
> - `plugins/sdlc-workflow/shared/convention-utils.md` — convention reference formatter
> - `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Step 6a (Create the tasks)
>
> **Suggested Approach**:
> - RC-1: Keep the exact heading text when rendering `§<Section Name>`. Remove the
>   lowercase/kebab-case normalization.
> - RC-2: Have Step 6a use the hierarchyLevel-0 (Task) issue type from dynamic
>   issue-type discovery, or a configured Task issue type ID. Never use the Feature
>   issue type ID.
>
> **Reproducer Strategy**:
> - RC-1: Assert that `Per CONVENTIONS.md §Migration Patterns:` appears for a
>   `## Migration Patterns` heading.
> - RC-2: Assert that the task `create_issue` payload uses issue type 10050 under a
>   custom scheme.
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.

## Step 4.5 – Affects Version Resolution

- `affectsVersions` is not set.
- No `Environment / Version` section exists, so no version could be extracted
  (sub-step 4.5.2 → 4.5.6).
- Would post to ACME-502: "Affects Version could not be determined from the bug
  description — please set manually." (with Comment Footnote v0.14.0).

## Next: Step 6 – Decomposition Guard

Two independent root causes were found, so the triage does **not** silently create
a single bundled Task. The decomposition guard prompt is in `decomposition-guard.md`.
Task creation (Steps 5/5b/5c) waits on the user's choice:
- **Proceed** → one Task (reproducer tests for both defects listed first in AC and
  Test Requirements), linked as Task *Blocks* ACME-502, plus a digest comment.
- **Split** → stop. Suggest the user file two separate Bugs (one per root cause) and
  triage each one on its own.
