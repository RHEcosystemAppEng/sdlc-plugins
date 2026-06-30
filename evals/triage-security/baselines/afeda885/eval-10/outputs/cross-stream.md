# Cross-Stream Impact: CVE-2026-55123

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

---

**Cross-stream impact**: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | **YES** |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | **YES** |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | **YES** |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | **YES** |

Stream rhtpa-2.1 has no companion CVE Jira for CVE-2026-55123. Preemptive remediation tasks have been created.

---

## Sibling CVE Jira Search

**JQL executed**: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result**: No sibling Vulnerability issues found.

- Stream rhtpa-2.2: TC-8020 (current issue)
- Stream rhtpa-2.1: **No CVE Jira exists**

Since no CVE Jira covers stream rhtpa-2.1, Case B applies: create preemptive remediation tasks.

## Preemptive Task Details

### Why Preemptive Tasks Are Needed

Stream rhtpa-2.1 ships tokio 1.40.0 in both released versions (RHTPA 2.1.0, RHTPA 2.1.1). The fix threshold is 1.42.0. No sibling CVE Jira exists for this stream, so remediation cannot be tracked through a dedicated Vulnerability issue. Preemptive tasks ensure remediation is not missed.

### Preemptive Tasks Created for Stream rhtpa-2.1

| Task | Type | Summary | Labels | Link to TC-8020 |
|------|------|---------|--------|-----------------|
| Upstream backport | Task | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| Downstream propagation | Task | Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |

### Key Differences from Standard Remediation (Case A)

| Aspect | Case A (rhtpa-2.2) | Case B Preemptive (rhtpa-2.1) |
|--------|-------------------|-------------------------------|
| Labels | ai-generated-jira, Security, CVE-2026-55123 | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** |
| Link type to CVE Jira | Depend | **Related** |
| Description prefix | (none) | Preemptive remediation notice referencing TC-8020 |
| Target branch (upstream) | release/0.4.z | release/0.3.z |
| Konflux release repo | rhtpa-release.0.4.z | rhtpa-release.0.3.z |

### Preemptive Task Comment on TC-8020

The following comment would be posted to TC-8020 after creating preemptive tasks:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: upstream backport task (security-preemptive) — bump tokio to 1.42.0 on release/0.3.z
- rhtpa-2.1: downstream propagation task (security-preemptive) — update rhtpa-backend ref in rhtpa-release.0.3.z

These tasks use the "Related" link type and carry the `security-preemptive` label. When PSIRT creates a stream-specific CVE Jira for rhtpa-2.1, Step 4.4 reconciliation will link the preemptive tasks to the new CVE Jira, change the link type to "Depend", and remove the `security-preemptive` label.

---

## Reconciliation Path (Future Step 4.4)

When PSIRT creates a CVE Jira for CVE-2026-55123 scoped to stream rhtpa-2.1, the next triage run on that issue will:

1. Search for preemptive tasks: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`
2. Filter results for tasks with `(rhtpa-2.1)` in their summary
3. Link the new CVE Jira to the preemptive tasks with "Depend"
4. Remove the `security-preemptive` label from the tasks
5. Skip new remediation task creation (remediation already exists)
