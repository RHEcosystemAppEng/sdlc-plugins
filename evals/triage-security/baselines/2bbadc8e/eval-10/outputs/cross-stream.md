# Cross-Stream Impact -- Case A

## Cross-Stream Impact Analysis

TC-8020 is scoped to stream **rhtpa-2.2** (suffix `[rhtpa-2.2]`). The version impact analysis (Step 2) reveals that stream **rhtpa-2.1** is also affected:

| Stream | Versions Affected | tokio version | Fix Threshold |
|--------|-------------------|---------------|---------------|
| rhtpa-2.2 (issue scope) | RHTPA 2.2.0, RHTPA 2.2.1 | 1.41.1 | 1.42.0 |
| rhtpa-2.1 (cross-stream) | RHTPA 2.1.0, RHTPA 2.1.1 | 1.40.0 | 1.42.0 |

## Sibling CVE Jira Search

JQL executed (simulated):
```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020
```

**Result: No sibling Vulnerability issues found** for CVE-2026-55123 in stream rhtpa-2.1.

Since no CVE Jira exists for rhtpa-2.1, **preemptive remediation tasks** must be created (Case A).

## PROPOSAL: Cross-Stream Impact Comment on TC-8020

The following comment would be posted to TC-8020:

---

Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.

| Stream | tokio version | Affected? |
|--------|---------------|-----------|
| rhtpa-2.1 | 1.40.0 | YES |

No sibling CVE Jira exists for stream rhtpa-2.1. This stream is not tracked by a companion issue.

---

## PROPOSAL: Preemptive Remediation Tasks for rhtpa-2.1

Since no CVE Jira exists for rhtpa-2.1, the following preemptive remediation tasks are proposed:

### Preemptive Task 1: Upstream Dependency Bump

| Field | Value |
|-------|-------|
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Labels | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** |
| Repository | backend |
| Target Branch | release/0.3.z |
| Link to TC-8020 | **Related** (not Depend -- originating CVE is in a different stream) |

### Preemptive Task 2: Downstream Propagation

| Field | Value |
|-------|-------|
| Summary | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) |
| Labels | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** |
| Repository | rhtpa-release.0.3.z |
| Target Branch | main |
| Blocked by | Preemptive Task 1 (Blocks link) |
| Link to TC-8020 | **Related** (not Depend) |

## PROPOSAL: Preemptive Task Comment on TC-8020

After creating the preemptive tasks, the following comment would be posted to TC-8020:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: {{preemptive-upstream-task-key}} (upstream bump, security-preemptive), {{preemptive-downstream-task-key}} (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the `security-preemptive` label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---

## Reconciliation Note (Step 4.4)

When PSIRT later creates a CVE Jira for CVE-2026-55123 scoped to rhtpa-2.1, the triage of that new issue will:

1. Search for preemptive tasks matching CVE-2026-55123 with the `security-preemptive` label
2. Find the tasks created above for rhtpa-2.1
3. Link the new CVE Jira to the preemptive tasks with "Depend" (standard remediation linkage)
4. Remove the `security-preemptive` label from the tasks
5. Skip new remediation task creation (tasks already exist)

## Summary of All Proposed Jira Mutations

All mutations below are **PROPOSALS** -- none have been executed.

| # | Action | Target | Type | Details |
|---|--------|--------|------|---------|
| 1 | Create Task | (new) | Remediation | Upstream bump tokio to 1.42.0 (rhtpa-2.2) |
| 2 | Create Task | (new) | Remediation | Downstream propagation rhtpa-release.0.4.z (rhtpa-2.2) |
| 3 | Create Task | (new) | Preemptive Remediation | Upstream bump tokio to 1.42.0 (rhtpa-2.1) |
| 4 | Create Task | (new) | Preemptive Remediation | Downstream propagation rhtpa-release.0.3.z (rhtpa-2.1) |
| 5 | Link | TC-8020 -> Task 1 | Depend | Standard CVE-to-remediation link |
| 6 | Link | TC-8020 -> Task 2 | Depend | Standard CVE-to-remediation link |
| 7 | Link | Task 1 -> Task 2 | Blocks | Upstream blocks downstream (rhtpa-2.2) |
| 8 | Link | TC-8020 -> Task 3 | Related | Preemptive cross-stream link |
| 9 | Link | TC-8020 -> Task 4 | Related | Preemptive cross-stream link |
| 10 | Link | Task 3 -> Task 4 | Blocks | Upstream blocks downstream (rhtpa-2.1) |
| 11 | Comment | TC-8020 | Cross-stream | Cross-stream impact notice |
| 12 | Comment | TC-8020 | Preemptive | Preemptive task creation notice |
| 13 | Label | TC-8020 | Field edit | Add `ai-cve-triaged` label |
| 14 | Comment | TC-8020 | Summary | Post-triage summary comment |
