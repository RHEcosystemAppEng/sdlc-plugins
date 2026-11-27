# Triage Outcome: TC-8021 (CVE-2026-31812, quinn-proto < 0.11.14) [rhtpa-2.2]

## Decision

**Affected. The issue proceeds to remediation: Case A (cross-stream impact) and Case B (remediation tasks for 2.2.x).**
The issue is **not** closed. Step 7 found no concurrent triage on `quinn-proto`, so the Case A/B/C branching
continues without a concurrent-triage label or pause.

All Jira mutations below are **proposals** that need engineer confirmation. None were executed, because
the eval forbids Jira calls.

## Rationale

1. **Scope:** the summary suffix `[rhtpa-2.2]` maps to stream 2.2.x, so the issue is scoped.
2. **Version impact (2.2.x):** 2.2.0 (0.11.9), 2.2.1 (0.11.12), and 2.2.2 (retag of 2.2.1) ship quinn-proto
   below 0.11.14 and are **affected**. 2.2.3 and 2.2.4 ship 0.11.14 and are **not affected**.
3. **Other streams:** 2.1.0 and 2.1.1 both ship 0.11.9 and are **affected**. 2.1.x is outside this issue's scope,
   which triggers Case A.
4. **PSIRT Affects Versions is wrong:** "RHTPA 2.0.0" corresponds to no configured stream.
5. **Not Case C:** supported versions are affected, so closing as Not a Bug does not apply.

## Step-by-step results

| Step | Result |
|---|---|
| 0 Config | Valid. Upstream Affected Component = customfield_10632 (assumed). PS Component and Stream fields are absent. |
| 0.3 Staleness | Matrix is 152 days old (Last-Updated 2026-06-28). Warned, and the eval assumed "Proceed anyway". |
| 0.8 Assign | Proposed: assign to current user and transition New → Assigned. |
| 1 Extraction | CVE-2026-31812, quinn-proto, < 0.11.14, fixed in 0.11.14, CVSS 7.5. See data-extraction.md. |
| 1.5 Enrichment | Not run (no external calls allowed), so confidence in the Jira description data is reduced. |
| 1.7 Embargo | Skipped: no embargo policy URL is configured. |
| 2 Version impact | 2.2.0, 2.2.1, 2.2.2 YES; 2.2.3, 2.2.4 NO; 2.1.0, 2.1.1 YES (out of scope). The dev stream was not assessed (no data). |
| 3 Affects Versions | Proposed: `[RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`, plus a correction comment with the footnote. |
| 4 Siblings | No sibling search result was supplied, so it is not evaluated. Run the CVE-label JQL to find a 2.1.x companion. |
| 4.3 Cross-CVE overlap | **Skipped**: the PS Component and Stream custom fields are not configured. |
| 4.4 Preemptive reconciliation | No data was supplied. Run the `security-preemptive` + CVE label JQL before creating tasks. |
| 5 Lifecycle | Product pages were not fetched. Assumed supported, pending verification. |
| 6 Already fixed | No resolved siblings are known, so continue. |
| **7 Concurrent triage** | **JQL `cf[10632] ~ 'quinn-proto' AND status IN ('In Progress','Code Review') AND key != TC-8021` returned 0. Proceed silently.** |
| 7.5 Release Jira | 2.2.x family: search for the Epic `RHTPA 2.2.* Release Tasks`. If none exists, propose the next patch, **RHTPA 2.2.5** (latest released is 2.2.4), and create the Task `RHTPA 2.2.5 CVE triage`. Each creation needs individual confirmation. The 7.5.3 dedup check runs because customfield_10632 is configured. |
| 8 Remediation | Case A + Case B (below). |

## Proposed remediation

### Case A: cross-stream impact (2.1.x)

- Comment on TC-8021: "Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x (2.1.0, 2.1.1 ship
  0.11.9) based on lock file analysis. These streams are tracked by companion issues (see Related links) or may
  require separate PSIRT triage." This comment includes the Comment Footnote.
- If no 2.1.x sibling CVE Jira exists, create **preemptive** tasks for 2.1.x. These carry the label `security-preemptive`
  and use a **Related** link to TC-8021. Cargo is a source dependency, so this means 2 tasks: an upstream backport on
  `release/0.3.z` and a downstream propagation in rhtpa-release.0.3.z. Then post the preemptive-task-list comment.
  If a 2.1.x sibling exists, skip these tasks.

### Case B: 2.2.x remediation (2 tasks, Cargo source dependency)

Unless Step 7.5.3 dedup finds an existing remediation Task for `quinn-proto` linked to the release Task:

1. **Upstream task** on rhtpa-backend `release/0.4.z`. If `git show release/0.4.z:Cargo.lock` confirms
   quinn-proto ≥ 0.11.14 (likely, because v0.4.11 and v0.4.12 already ship it), use the **dependency bump / fix-available**
   variant. Otherwise use the **upstream backport** variant (`cargo update -p quinn-proto --precise 0.11.14`).
2. **Downstream propagation** in rhtpa-release.0.4.z (Konflux), **blocked by** task 1.
- Link both tasks to TC-8021 with **Depend**. Link the upstream task to the downstream task with **Blocks**.
  Link each task to the release Task with **Blocks**. Link TC-8021 to the release Task with **Related**.
- Post a description digest comment on each created task.
- Note for the engineer: releases 2.2.3 and 2.2.4 already ship the fixed 0.11.14, so the remaining exposure is customers on
  2.2.0 to 2.2.2. Confirm whether the downstream task reduces to "already fixed in 2.2.3+, no new build needed" before
  creating it.

### Post-triage

- Add the label `ai-cve-triaged` to TC-8021.
- Post a summary comment covering the impact table, the Affects Versions correction, the outcome, the task keys,
  the release Epic and Task keys, and any dedup results. It must @mention the issue reporter (ADF mention node)
  and include the Comment Footnote.

## Open items before executing

- Resolve the issue-key discrepancy (task: TC-8021, file: TC-8001).
- Verify `release/0.4.z` and `release/0.3.z` HEAD quinn-proto versions (Step 2.5), the dev-stream HEAD, the dependency
  chain, sibling and preemptive searches, and lifecycle status. None of these could be verified without external access.
- Refresh the stale security matrix if possible.
