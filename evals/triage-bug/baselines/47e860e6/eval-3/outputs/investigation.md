# Triage Investigation — ACME-502

**Bug**: [ACME-502](https://mock-jira.example.com/browse/ACME-502) — Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow
**Labels**: reported-by-user
**Status**: New
**Affects Version/s**: not set

---

## Step 0 — Configuration Validation

Source: `claude-md-bug-config.md` (project CLAUDE.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | acme-backend (serena_backend, /home/dev/repos/acme-backend) | present |
| Project key | ACME | present |
| Cloud ID | mock-cloud-id-for-eval | present |
| Code Intelligence | section present (no Serena configured, so Read/Grep/Glob is used instead) | present |
| Bug issue type ID | 10020 | present |
| Bug template path | docs/templates/bug-template.md (mocked by `bug-template-mock.md`) | present |
| Bug-to-Task link type | Blocks | present |

Result: the configuration is complete, so the skill can proceed.

## Step 1 — Fetch Bug and Validate

- **Issue type check**: ACME-502 has issue type Bug (ID 10020). This matches the configured Bug issue type ID 10020. **Pass.**
- **Template section parse** (checked against `bug-template-mock.md`):

| Required Section | Heading | Found |
|---|---|---|
| Description | `### **Issue Description**` | yes |
| Steps to reproduce | `### **Steps to Reproduce**` | yes |
| Expected Result | `### **Expected Result**` | yes |
| Actual Result | `### **Actual Result**` | yes |
| Environment / Version | `### **Environment / Version**` | **no** |
| Attachments | `### **Attachments**` | yes ("None.") |

| Optional Section | Found |
|---|---|
| Root Cause | no |
| Suggested Fix | yes (the reporter thinks these are "two separate bugs") |

> **Note on a template gap:** the `### **Environment / Version**` section is missing.
> Under a strict reading of Step 1, the skill would stop here and tell the user:
> "Bug ACME-502 is missing required sections: Environment / Version. The bug
> description does not follow the template at docs/templates/bug-template.md."
> This eval scenario says the investigation goes ahead, so the analysis below
> continues. The gap still matters later: Step 4.5 cannot get a version from the
> description, so it would post the "Affects Version could not be determined"
> gap comment.

## Step 2 — Reproduce / Trace

The bug is in skill and documentation logic (`/plan-feature`), so it cannot be reproduced by running a command. I traced the code path instead.

Entry point: `/plan-feature ACME-200`. The bug describes two symptoms, and each one follows its own path through the code:

**Trace A (convention reference format):**
`plan-feature/SKILL.md` Step 3 (CONVENTIONS.md lookup) reads the `## Migration Patterns` heading
-> Step 5 "Convention-aware task enrichment" builds the `Per CONVENTIONS.md §<Section Name>: ...` lines
-> the section name goes through the convention formatter in `shared/convention-utils.md`
-> the formatter **lowercases and kebab-cases** the heading, so the output is `§migration-patterns`.
The expected format comes from `shared/convention-applicability-rules.md`, which says the verbatim heading is used (`Per CONVENTIONS.md §Migration Patterns: ...`). This trace diverges from expected behavior **at the formatter**.

**Trace B (wrong issue type):**
`plan-feature/SKILL.md` Step 2.5 discovers the project issue types and maps hierarchyLevel 0 to the Task role (custom scheme: Task = 10050)
-> Step 6a "Create the tasks" calls `jira.create_issue`
-> Step 6a uses the **Feature issue type ID** (10142, from the `## Jira Configuration` section) instead of the Task type ID from the Step 2.5 type-to-role mapping
-> the issue is created as type Feature (10142).
This trace diverges from expected behavior **at the issue-type selection in Step 6a**.

Reproduction outcome: **confirmed by trace** for both symptoms. The two traces have no shared code; the only thing they share is the `/plan-feature` entry point.

## Step 3 — Codebase Investigation

Target repository: the component is `sdlc-workflow`, and the affected files are sdlc-workflow plugin skill and shared files. No Serena instance is configured, so I used Read/Grep/Glob.

### Affected files and symbols

| # | File | Symbol / Section | Defect |
|---|---|---|---|
| 1 | `shared/convention-utils.md` | Convention reference formatter (heading-to-`§` reference rendering) | Normalizes the heading to lowercase kebab-case (`Migration Patterns` becomes `migration-patterns`) instead of keeping the verbatim heading text |
| 2 | `skills/plan-feature/SKILL.md` | Step 6a – "Create the tasks" (`jira.create_issue` issue-type argument) | Reads `Feature issue type ID` from Jira Configuration instead of the Task-role type ID from the Step 2.5 type-to-role mapping |

### Related references
- `shared/convention-applicability-rules.md` (`Per CONVENTIONS.md §<Section Name>` format, with the example `§Migration Patterns`) is the authoritative spec for root cause 1.
- `skills/plan-feature/SKILL.md` Step 2.5 ("Map types to hierarchy roles" and "Store the type-to-role mapping") already produces the correct Task type ID that Step 6a should use. This is the correct pattern for root cause 2.
- `skills/plan-feature/SKILL.md` Step 5 "Convention enrichment verification" is a natural place to assert that `§` references match a CONVENTIONS.md heading exactly.

### Persistence-impact analysis
Neither defect writes to a database. Both outputs are Jira artifacts (the task description text and the issue type). **No data migration is needed.** Tasks already created with the wrong type or malformed references would need manual cleanup in Jira. That cleanup is operational and out of scope for a code fix.

### Dependency check between the two defects
- Root cause 1 is only about how text is rendered in the task description. It does not touch issue-type selection.
- Root cause 2 is only about which issue type ID is passed to `jira.create_issue`. It does not touch description content.
- Fixing either one leaves the other symptom unchanged. Each one can be reproduced and verified separately: (a) a CONVENTIONS.md heading-format test and (b) a custom issue-type-scheme test.
- They are in **different modules** (a shared utility vs. a skill's Jira creation step).

## Step 4 — Root Cause Analysis

### Root Cause 1 — Convention reference formatter kebab-cases headings
- **What**: Implementation Notes render convention references as `§migration-patterns`.
- **Why**: The convention formatter treats the heading like a URL slug or anchor (lowercase plus hyphens). The spec requires the verbatim heading text.
- **Where**: `shared/convention-utils.md`, convention reference formatter.
- **Verify**: Use a CONVENTIONS.md that contains `## Migration Patterns`. The generated Implementation Notes must contain `Per CONVENTIONS.md §Migration Patterns:` and must not contain `§migration-patterns`.

### Root Cause 2 — Task creation uses the Feature issue type ID
- **What**: Tasks are created with issue type Feature (10142) instead of Task (10050).
- **Why**: Step 6a takes the issue type from the `Feature issue type ID` configuration field. It should use the Task-role type found in Step 2.5. The bug is hidden in projects where the default scheme happens to line up, and it shows up with custom issue type schemes.
- **Where**: `skills/plan-feature/SKILL.md`, Step 6a – Create the tasks.
- **Verify**: Use a project whose custom scheme has Task = 10050. The `jira.create_issue` call for each generated task must use issue type ID 10050, and must never use 10142.

### Conclusion
**This bug has two independent root causes** in different modules, with separate fixes and separate reproducers. It is not one defect that shows up in several files. This **triggers the Step 6 Decomposition Guard** (see `decomposition-guard.md`). The user's answer decides whether one bundled Task or separate Bugs are created. Task generation (Step 5) is paused until the user answers.

### Root cause comment (would be posted to ACME-502 via `jira.add_comment`, ADF)

> **Root Cause**: The two reported symptoms come from two independent defects.
> (1) The convention reference formatter in `shared/convention-utils.md` lowercases
> and kebab-cases CONVENTIONS.md headings (`§migration-patterns`) instead of keeping
> the verbatim heading (`§Migration Patterns`).
> (2) `plan-feature/SKILL.md` Step 6a creates tasks with the Feature issue type ID
> (10142) from Jira Configuration instead of the Task-role type ID discovered in Step 2.5
> (10050 in custom schemes).
>
> **Affected Files**:
> - `plugins/sdlc-workflow/shared/convention-utils.md` (convention reference formatter)
> - `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (Step 6a – Create the tasks)
>
> **Suggested Approach**: (1) Render `§` references with the exact heading text, following
> `shared/convention-applicability-rules.md`. (2) In Step 6a, take the issue type from the
> Step 2.5 type-to-role mapping (Task role, hierarchyLevel 0), never from Feature issue type ID.
>
> **Reproducer Strategy**: (1) Use a CONVENTIONS.md with `## Migration Patterns` and assert that the
> Implementation Notes contain `§Migration Patterns`. (2) Use a custom issue type scheme with Task = 10050
> and assert that the created issues use type 10050.
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.

## Step 4.5 — Affects Version (expected behavior)
Affects Version/s is not set, and the description has no `Environment / Version` section, so there is no version to extract. Per 4.5.6, the skill would post this gap comment: "Affects Version could not be determined from the bug description — please set manually." (with the footnote).

## Next step
Steps 5, 5b, 5c and 7 are **on hold** until the user answers the decomposition guard prompt in `decomposition-guard.md`.
