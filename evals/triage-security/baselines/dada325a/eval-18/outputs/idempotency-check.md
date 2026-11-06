# Idempotency Check: TC-8001 (re-run)

Each Jira mutation that a first-run triage would perform was checked against the
issue state from Step 1 (labels, status, `issuelinks`, comment history). The table
lists every pre-existing artifact found and what the re-run does with it.

## Pre-existing triage artifacts detected

| # | Artifact (first-run mutation) | Evidence on TC-8001 | Re-run decision |
|---|---|---|---|
| 1 | `ai-cve-triaged` label (Post-Triage Summary 1) | Labels include `ai-cve-triaged` | **Skip.** The label is already present, so no `edit_issue` labels update |
| 2 | Transition to Assigned (Step 0.8) | Status = In Progress, which is later than Assigned | **Skip.** Step 0.8 skips the transition when the issue is already Assigned or later |
| 3 | Transition to In Progress (Jira Linkage 5) | Status = In Progress | **Skip.** Already in the target status |
| 4 | Assignment (Step 0.8 / Linkage 6) | Assignee = engineer-a@example.com | **No-op** if the current user is engineer-a. Otherwise it would be a re-assignment, which needs confirmation and is not done here (see triage-outcome.md) |
| 5 | Upstream backport remediation Task (Case B) | Depend -> **TC-8100** "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]", labels ai-generated-jira, Security, CVE-2026-31812, In Progress | **Skip creation.** A 2.2.x upstream task for this CVE already exists and targets >= 0.11.14 (meets the fix threshold) |
| 6 | Downstream propagation remediation Task (Case B) | Depend -> **TC-8101** "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]", same labels, Open | **Skip creation.** The downstream task already exists |
| 7 | Depend link TC-8001 -> TC-8100 | `issuelinks` has type `Depend`, key TC-8100 | **Skip.** The link already exists |
| 8 | Depend link TC-8001 -> TC-8101 | `issuelinks` has type `Depend`, key TC-8101 | **Skip.** The link already exists |
| 9 | Blocks link TC-8100 -> TC-8101 | TC-8101 shows "Blocks: TC-8100" (upstream blocks downstream) | **Skip.** The link already exists |
| 10 | Description digest comment(s) | Comment 1: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4...a1b2`, posted by sdlc-workflow/triage-security | **Skip.** A digest exists. Digests are posted only right after a task is created, and no task is created on this run, so no digest is recomputed or posted |
| 11 | "Remediation tasks created" list comment (Linkage 7) | Covered by the summary comment's "Remediation tasks created: TC-8100 ..., TC-8101 ..." | **Skip.** No new tasks, so there is nothing new to list |
| 12 | Post-triage summary comment | Comment 2 "Post-triage summary ... Triage complete for CVE-2026-31812", with the triage-security v0.11.1 footnote | **Skip.** A summary comment from this skill already exists. Posting another would duplicate it with no new triage action to report |
| 13 | Affects Versions correction + correction comment (Step 3) | Field = RHTPA 2.2.0, RHTPA 2.2.1. The prior summary says these were corrected | **Prior correction preserved, no automatic write.** Re-verification found a gap: see "Discrepancy" below |

## Steps with nothing to create

| Step | Result |
|---|---|
| 1.7 Embargo | Skipped. No policy URL configured |
| 4.1 / 4.2 Siblings | No sibling Vulnerability issues are in the supplied data, so there are no Related links to create (the existing-link check would skip duplicates anyway) |
| 4.3 Cross-CVE overlap | Skipped. Upstream Affected Component / PS Component / Stream fields are not configured in Security Configuration |
| 4.4 Preemptive reconciliation | No `security-preemptive` tasks for CVE-2026-31812 in the data. Nothing to reconcile |
| 5 Lifecycle | 2.2.x is treated as supported (lifecycle page not fetched in eval). No Won't Do closure |
| 6 Already fixed | No resolved siblings. No closure |
| 7 Concurrent triage | Skipped. Upstream Affected Component field not configured |
| 7.5 Release Jira | Prior triage linked no release Epic or Task. Creating one needs individual engineer confirmation and is not done implicitly on a re-run. 7.5.3 dedup is skipped (field not configured). The existing tasks already cover the stream |
| 8 Case A (cross-stream) | 2.1.x (2.1.0, 2.1.1) is also affected. The cross-stream notice and preemptive tasks are confirmation-gated and need a sibling-CVE lookup first. Neither the prior summary nor the issue links show that this was handled, so it is flagged for the engineer below and not executed silently |
| 8 Case B | **Skipped.** Remediation for 2.2.x already exists (TC-8100 + TC-8101, 2 tasks, which matches the Cargo classification) |

## Discrepancy found during re-verification

- The matrix says **2.2.2 (build 0.4.9) is a backend retag of 2.2.1** (backend tag
  `v0.4.8`, quinn-proto 0.11.12). Under the retag rule, 2.2.2 is **affected**.
- The prior post-triage summary says "RHTPA 2.2.2 and later ship quinn-proto 0.11.14
  (not affected)". That is inconsistent with the current matrix: 2.2.3 is the first
  2.2.x release with 0.11.14.
- The matrix is stale (Last-Updated 2026-06-28, about 131 days old) and predates the
  prior triage on 2026-07-01. The correct Affects Versions should therefore be confirmed
  after a matrix refresh.
- Proposed (not executed): `Current: [RHTPA 2.2.0, RHTPA 2.2.1] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
  This depends on the RHTPA 2.2.2 Jira version ID from `getJiraIssueTypeMetaWithFields`
  (not called in eval).
- Remediation is unaffected. 2.2.2 ships the same backend source (v0.4.8) as 2.2.1, so
  TC-8100/TC-8101 (backport >= 0.11.14 on release/0.4.z, then propagation) already cover
  it. No new task is needed.
