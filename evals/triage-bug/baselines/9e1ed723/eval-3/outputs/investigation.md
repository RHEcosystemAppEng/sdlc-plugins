# Triage Investigation — ACME-502

**Bug**: [ACME-502](https://mock-jira.example.com/browse/ACME-502) — Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow
**Labels**: reported-by-user
**Affects Version/s**: not set

> Eval mode: no Jira MCP, Serena, or external tools were called. All Jira operations
> are described below instead of executed.

---

## Step 0 — Validate Project Configuration

Source: `claude-md-bug-config.md`

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (serena_backend, /home/dev/repos/acme-backend) | present |
| Project key | ACME | present |
| Cloud ID | mock-cloud-id-for-eval | present |
| Code Intelligence | section present (no Serena servers configured) | present |
| Bug issue type ID | 10020 | present |
| Bug template path | docs/templates/bug-template.md (mocked by `bug-template-mock.md`) | present |
| Bug-to-Task link type | Blocks | present |

Result: configuration is valid. Note that Jira Configuration defines only a
`Feature issue type ID` (10142) and no Task issue type ID. That matters for root cause #2.

## Step 1 — Fetch Bug

- Issue type: Bug (ID 10020), which matches Bug Configuration `Bug issue type ID: 10020`. Valid.
- Description parsed against the template heading formats:

| Template section | Heading | Found |
|---|---|---|
| Description | `### **Issue Description**` | yes |
| Steps to reproduce | `### **Steps to Reproduce**` | yes |
| Expected Result | `### **Expected Result**` | yes |
| Actual Result | `### **Actual Result**` | yes |
| Environment / Version | `### **Environment / Version**` | **no** |
| Attachments | `### **Attachments**` | yes ("None.") |
| Root Cause (optional) | `### **Root Cause**` | no |
| Suggested Fix (optional) | `### **Suggested Fix**` | yes |

**Template compliance finding:** the required `### **Environment / Version**` section is
missing. Under strict skill rules (Step 1), triage would stop here with:

> "Bug ACME-502 is missing required sections: Environment / Version. The bug
> description does not follow the template at docs/templates/bug-template.md."

The eval task explicitly asks for the investigation and decomposition-guard outcome, so
the analysis continues below. In Step 4.5 the missing section is treated as a version gap.

## Step 2 — Reproduce / Trace

This is a skill/documentation bug, so it can't be reproduced by running a command.
**Code-path tracing** was used instead.

Entry point: `/plan-feature ACME-200` (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`).

The Steps to Reproduce check two separate observable outputs, (a) the convention
references and (b) the issue type. Tracing each one leads to a different code path:

### Trace A — Convention references in Implementation Notes
1. plan-feature runs a CONVENTIONS.md lookup for the target repository and reads the
   section `## Migration Patterns`.
2. For each applicable convention, plan-feature emits a line
   `Per CONVENTIONS.md §<Section Name>: <action>` in Implementation Notes
   (contract in `shared/convention-applicability-rules.md`, e.g.
   `Per CONVENTIONS.md §Migration Patterns: ...`).
3. The section name is rendered by the convention formatter in
   `shared/convention-utils.md`. The formatter normalizes the heading into a slug
   (lowercase plus spaces replaced by hyphens), which gives `§migration-patterns`
   instead of keeping the heading text verbatim (`§Migration Patterns`).
4. **Divergence:** the formatter uses an anchor/slug transform where the display
   heading text is expected.

### Trace B — Issue type of the created task
1. plan-feature Step 6a creates the Jira issues for the planned tasks.
2. The `create_issue` call in Step 6a takes its issue type ID from the
   Jira Configuration field `Feature issue type ID` (10142).
3. Step 6a ignores the Task-level (hierarchyLevel 0) issue type that the dynamic
   issue-type discovery found (Task = 10050 in the reporter's custom scheme).
4. **Divergence:** Step 6a passes the Feature issue type ID instead of the discovered
   Task issue type ID. Every created task becomes a Feature (10142).

Reproduction outcome: **confirmed by trace**. Both symptoms are explained, and each by
its own code path.

## Step 3 — Codebase Investigation

- Target: the `sdlc-workflow` plugin (from the Component field and the referenced files).
- Serena: none configured (Code Intelligence section), so Read/Grep/Glob is the fallback.
- No persistence boundary: both outputs are generated per skill run and nothing is
  written to a database, so **no data migration is needed**. Tasks already created with
  the wrong type or malformed notes would need manual correction in Jira, but that is
  outside the code fix.

| # | File | Symbol / Section | Role in bug |
|---|---|---|---|
| 1 | `plugins/sdlc-workflow/shared/convention-utils.md` | convention reference formatter (heading to `§<name>` rendering) | Produces kebab-case `§migration-patterns` |
| 1 | `plugins/sdlc-workflow/shared/convention-applicability-rules.md` | `Per CONVENTIONS.md §<Section Name>` contract | Defines the expected format (verbatim heading). Reference only, no change needed |
| 2 | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Step 6a, task issue creation | Uses `Feature issue type ID` for Task creation |
| 2 | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | dynamic issue-type discovery (hierarchyLevel 0 = Task) | Has the correct Task ID, but Step 6a doesn't use it |

### Independence analysis

| Criterion | Root cause #1 | Root cause #2 |
|---|---|---|
| Module | `shared/convention-utils.md` (shared utility) | `skills/plan-feature/SKILL.md` Step 6a |
| Defect type | String formatting / normalization | Wrong configuration field / ID selection |
| Data flow | CONVENTIONS.md heading → Implementation Notes text | Issue-type discovery / Jira Config → `create_issue` issuetype |
| Shared code path? | None. Neither path calls the other or shares state | None |
| Fix one fixes the other? | No | No |
| Blast radius | Every skill using the shared formatter (plan-feature, and any other skill emitting convention references) | plan-feature task creation only |
| Reproducer | Assert that the emitted reference equals `§Migration Patterns` | Assert that the created issue type ID is 10050 (Task), not 10142 |

**Conclusion:** these are **two independent root causes** in different modules. This is
not one defect showing up in several files. The reporter's Suggested Fix says the same
thing ("These are likely two separate bugs").

## Step 4 — Root Cause Analysis

### Root cause #1: Malformed convention references
- **What:** Implementation Notes reference conventions as `§migration-patterns`.
- **Why:** the convention formatter in `shared/convention-utils.md` slugifies the
  CONVENTIONS.md heading (lowercase plus kebab-case) instead of keeping the heading text
  verbatim, which `shared/convention-applicability-rules.md` requires.
- **Where:** `plugins/sdlc-workflow/shared/convention-utils.md`, convention
  reference formatting.
- **Suggested approach:** render `§<Section Name>` from the exact heading text (without
  the leading `## `), keeping case and spaces.
- **Reproducer strategy:** given a CONVENTIONS.md with `## Migration Patterns`, assert
  that the generated Implementation Notes contain `Per CONVENTIONS.md §Migration Patterns:`
  and not `§migration-patterns`. This fails before the fix and passes after.

### Root cause #2: Task created with Feature issue type
- **What:** generated tasks are created as Feature (10142) instead of Task (10050).
- **Why:** plan-feature Step 6a reads `Feature issue type ID` from Jira Configuration
  for the `create_issue` issuetype. It should use the hierarchyLevel-0 (Task) issue type
  ID from dynamic issue-type discovery.
- **Where:** `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a.
- **Suggested approach:** in Step 6a, use the discovered Task issue type ID for task
  creation. Keep `Feature issue type ID` for feature-level operations only.
- **Reproducer strategy:** with a custom issue type scheme where Task = 10050, assert
  that the `create_issue` call for a planned task uses issuetype ID 10050 and not 10142.

### Root cause comment (would be posted to ACME-502 — NOT posted in eval mode)

```
jira.add_comment("ACME-502", <ADF>)
```

Content:
- **Root Cause**: two independent defects. (1) The convention formatter in
  `shared/convention-utils.md` kebab-cases CONVENTIONS.md headings, which gives
  `§migration-patterns` instead of `§Migration Patterns`. (2) plan-feature Step 6a uses the
  Feature issue type ID (10142) instead of the discovered Task issue type ID (10050)
  when creating tasks.
- **Affected Files**: `plugins/sdlc-workflow/shared/convention-utils.md`;
  `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (Step 6a).
- **Suggested Approach**: (1) keep heading text verbatim in convention references;
  (2) use the hierarchyLevel-0 issue type ID in Step 6a.
- **Reproducer Strategy**: as described above for each root cause.
- Footer: rule + "This comment was AI-generated by sdlc-workflow/triage-bug v0.14.0."

## Step 4.5 — Affects Version Resolution

- `affectsVersions` is not set on ACME-502.
- The `### **Environment / Version**` section is missing, so no version can be extracted.
- Action (not executed in eval mode): flag the gap with
  `jira.add_comment("ACME-502", "Affects Version could not be determined from the bug description — please set manually.")`
  plus the Comment Footnote.

## Step 5 / 5b / 5c — Task generation: ON HOLD

Two independent root causes were found, so the **Decomposition Guard (Step 6) applies
before any Task is created**. One Task bundling unrelated fixes would break the rule
"Keep the generated Task scoped to a single fix". No Task, link, or digest is
created until the user responds. See `decomposition-guard.md`.

- If the user picks **Proceed**: create one Task (labels `ai-generated-jira`, Target
  Branch `main`). Acceptance Criteria would start with both reproducer tests, then both
  fixes, then no regressions. Add a Bug Context section, link it with "Blocks"
  (Task = inward, ACME-502 = outward), and post the digest comment.
- If the user picks **Split** (recommended): stop and suggest creating two separate Bugs,
  then triaging each one individually.
