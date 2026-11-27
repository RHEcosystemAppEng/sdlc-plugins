# Idempotency Check: TC-8001 re-run

Each mutation the triage-security workflow would normally make is checked against
the artifacts the prior run (triage-security v0.11.1, 2026-07-01) left on the issue.
If an artifact already exists, the mutation is skipped.

| # | Workflow step / mutation | Pre-existing artifact detected | Decision |
|---|--------------------------|--------------------------------|----------|
| 1 | Step 0.8: transition to Assigned | Status = In Progress (later than Assigned) | **SKIP** ("already in Assigned or later status, skip silently") |
| 2 | Step 0.8: assign to current user | Assignee = engineer-a@example.com | **SKIP** if the runner is engineer-a. Otherwise it is a reassignment that needs explicit confirmation. Not executed. |
| 3 | Step 3: Affects Versions correction | `versions` = [RHTPA 2.2.0, RHTPA 2.2.1]. The prior run's correction is already applied and its summary comment records it. | **No repeat of the prior correction.** See discrepancy D1 below. |
| 4 | Step 3: Affects Versions correction comment | Prior correction is documented in the post-triage summary | **SKIP**. Nothing new was applied, so nothing new to document. |
| 5 | Step 4.1/4.2: Related links to siblings | No sibling data available offline. Existing `issuelinks` hold only Depend links to TC-8100/TC-8101. | No link created. The skill checks `issuelinks` before linking ("Related link to X already exists, skipping"). Sibling search needs live JQL. |
| 6 | Step 4.3: cross-CVE overlap Depend link | Depend links to TC-8100/TC-8101 already exist | **SKIP** ("Depend link to [task] already exists, skipping") |
| 7 | Step 4.4: preemptive task reconciliation | TC-8100/TC-8101 carry `ai-generated-jira, Security, CVE-2026-31812` and no `security-preemptive` label, so they are standard Depend-linked tasks | **SKIP**. Nothing to reconcile and no label to remove. |
| 8 | Step 6: already-fixed closure | Issue has open remediation in progress. 2.2.3/2.2.4 ship 0.11.14, but 2.2.0–2.2.2 are still affected and supported. | **No closure.** |
| 9 | Step 7: concurrent triage | The current issue is excluded (`key != TC-8001`). Its own remediation is TC-8100/TC-8101. | No new label (`concurrent-triage-overlap` not applied). |
| 10 | Step 7.5.3: cross-CVE dedup | Remediation for upstream component `quinn-proto` in 2.2.x already exists: TC-8100 + TC-8101, Depend-linked to this CVE | Stream 2.2.x is **dedup'd**, so Step 8 skips creation for it |
| 11 | Step 8 Case B: create upstream backport task | **TC-8100**: "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]" (In Progress) | **SKIP**. Do not create a duplicate. |
| 12 | Step 8 Case B: create downstream propagation task | **TC-8101**: "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]" (Open) | **SKIP** |
| 13 | Remediation digest comment (per task) | `[sdlc-workflow] Description digest: sha256-md:a1b2...` comment exists from the prior run | **SKIP**. Digests are posted once, at creation. No task is created, so no digest is posted. |
| 14 | Link CVE to task (Depend) ×2 | Depend: TC-8100, Depend: TC-8101 | **SKIP** |
| 15 | Link upstream to downstream (Blocks) | TC-8101 is blocked by TC-8100 | **SKIP** |
| 16 | Remediation linkage: transition to In Progress | Status = In Progress | **SKIP** ("if not already") |
| 17 | Remediation linkage: "Remediation tasks created" comment | Prior summary lists TC-8100 (upstream backport) and TC-8101 (downstream propagation) | **SKIP** |
| 18 | Post-triage: add `ai-cve-triaged` label | Label present | **SKIP**. Jira labels are a set, and re-adding would be a no-op anyway. |
| 19 | Post-triage: summary comment | Post-triage summary comment exists (2026-07-01T10:01Z, with footnote) | **SKIP**. A second identical summary would only add noise. |
| 20 | Case C close / VEX justification | Affected versions exist in scope | Not applicable |

## Discrepancies found during re-verification (reported, not auto-applied)

Re-running the version analysis (Rules 3–5) showed problems with the prior run's
conclusions. Every Jira mutation needs explicit engineer confirmation (Rule 11), and
the eval forbids external calls, so these items are **reported as proposals only**.

- **D1: RHTPA 2.2.2 missing from Affects Versions.** The matrix shows 2.2.2 (build
  0.4.9) pins backend `v0.4.8`, noted as a "backend retag of 2.2.1". That build ships
  quinn-proto 0.11.12, which is below 0.11.14, so 2.2.2 is **affected**. The prior
  summary says "RHTPA 2.2.2 and later ship quinn-proto 0.11.14 (not affected)", which
  contradicts the retag rule. Proposed correction (pending confirmation):
  `Current: [RHTPA 2.2.0, RHTPA 2.2.1] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
- **D2: cross-stream impact (Case A) not recorded.** The 2.1.x stream (2.1.0 and 2.1.1)
  ships quinn-proto 0.11.9 and is also affected. The issue is scoped to 2.2.x, so
  Case A needs a cross-stream impact comment, plus preemptive tasks for 2.1.x if
  there is no sibling CVE Jira. No such comment or preemptive task appears on TC-8001.
  Deciding whether a sibling exists needs the Step 4 JQL, which was not run offline.
  The engineer should verify.
- **D3: digest comment placement (observation).** Per
  `shared/description-digest-protocol.md`, digest comments belong on each remediation
  task (TC-8100 and TC-8101), not on the Vulnerability. The mock shows one digest on
  TC-8001. This does not trigger a mutation, but the engineer may want to check that
  TC-8100 and TC-8101 each carry their own digest so `/implement-task` can verify them.
