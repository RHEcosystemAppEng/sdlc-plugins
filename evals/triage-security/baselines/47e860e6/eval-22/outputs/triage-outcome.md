# Triage Outcome: TC-8021 (CVE-2026-31812, quinn-proto)

## Decision: AFFECTED → Case A (cross-stream impact) + Case B (remediation for 2.2.x)

The issue is **not** closed. Lock file evidence shows supported versions in the issue's own
stream (2.2.x) ship quinn-proto < 0.11.14. The other supported stream (2.1.x) is also affected.

## Reasoning by step

| Step | Outcome |
|---|---|
| 0 / 0.3 | Config valid. Matrix is 129 days old, so a staleness warning was raised; proceeded with current matrix. |
| 0.8 | Proposed: assign to current user and transition New → Assigned. |
| 1 | CVE-2026-31812, quinn-proto, < 0.11.14, fixed in 0.11.14, scoped to 2.2.x, Cargo. |
| 1.5 | External APIs not queried (eval constraint). Jira data only, with reduced confidence. |
| 1.7 | Skipped (no embargo URL configured). |
| 2 | Affected: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1). Not affected: 2.2.3, 2.2.4 (0.11.14). |
| 3 | Proposed correction: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. |
| 4 | Sibling search `labels = 'CVE-2026-31812' AND key != TC-8021` was not simulated (no data given). Assumed no same-stream duplicate. 4.3 skipped (PS Component/Stream fields not configured). No preemptive task data was available for 4.4. |
| 5 | Lifecycle page not fetched. Assumed 2.1.x and 2.2.x supported (both are in the matrix). |
| 6 | No resolved siblings known, so there is no already-fixed closure. |
| 7 | Upstream Affected Component = quinn-proto. JQL for In Progress / Code Review triages returned **0 results**, so we proceed silently with no `concurrent-triage-overlap` label. See `concurrent-triage.md`. |
| 7.5 | Find or create release Epic/Task for 2.2.x (e.g. "RHTPA 2.2.5 Release Tasks" / "RHTPA 2.2.5 CVE triage"). The proposed default is the next patch after 2.2.4, which needs individual confirmation. 7.5.3 dedup: no existing quinn-proto remediation known, so no dedup. |
| 8 | Affected versions remain in scope, so this is not Case C. The issue is scoped and another stream (2.1.x) is affected, so Case A applies. Case B applies for 2.2.x. |

## Proposed actions (each requires engineer confirmation, none executed)

### Case A – cross-stream (2.1.x)
1. Comment on TC-8021: "Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
   2.1.x (2.1.0, 2.1.1 ship 0.11.9) based on lock file analysis..." plus Comment Footnote.
2. If no 2.1.x sibling CVE Jira exists, create preemptive tasks for 2.1.x with the
   `security-preemptive` label and a **Related** link to TC-8021. Upstream `release/0.3.z`
   is not confirmed to have the fix, so the tasks are an upstream backport (bump quinn-proto
   to 0.11.14 in rhtpa-backend `release/0.3.z`) plus downstream propagation (rhtpa-release.0.3.z),
   where the backport Blocks the propagation task.

### Case B – remediation in scope (2.2.x)
Cargo is a source dependency, so 2 tasks:
1. **Dependency bump** (rhtpa-backend, `release/0.4.z`): ensure quinn-proto ≥ 0.11.14.
   v0.4.11/v0.4.12 already ship 0.11.14, so this is likely already satisfied at branch HEAD.
   Step 2.5 must confirm this with `git show release/0.4.z:Cargo.lock` before choosing the
   bump variant over a backport.
2. **Downstream propagation** (rhtpa-release.0.4.z): ensure the next 2.2.x release pins a
   backend build with quinn-proto ≥ 0.11.14. Blocked by task 1.
- Link both tasks to TC-8021 with **Depend**, and the bump task **Blocks** the propagation task.
- Link remediation tasks to the release Task (**Blocks**), and TC-8021 to the release Task (**Related**).
- Post description digest comments per `shared/description-digest-protocol.md`.
- Coordination guidance: deployment context is `upstream` (default).

### Post-triage
- Add the `ai-cve-triaged` label to TC-8021.
- Post a summary comment with the version impact table, the Affects Versions correction,
  task links, and release Jira refs. Include an @mention of the issue reporter and the
  Comment Footnote (triage-security).

## Caveats
- Issue key mismatch: the mock file says TC-8001, the task says TC-8021. TC-8021 was used.
- Simulated / unverified inputs: the security matrix is stale, branch HEADs were not
  inspected, external CVE databases and the lifecycle page were not queried, and sibling
  and release Jira searches were not simulated.
- Due date 2026-07-15 has already passed.
- No Jira, git, or external calls were made, and no repository files were modified.
