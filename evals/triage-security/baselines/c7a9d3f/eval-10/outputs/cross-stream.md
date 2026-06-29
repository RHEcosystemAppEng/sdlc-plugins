# Cross-Stream Impact — CVE-2026-55123 (tokio < 1.42.0)

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

---

Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES |

Stream rhtpa-2.1 has no companion CVE Jira for CVE-2026-55123. Preemptive remediation tasks have been created (see Related links).

---

## Sibling CVE Jira Search

**JQL Query:**
```
project = TC AND issuetype = 10024 AND labels = "CVE-2026-55123" AND summary ~ "[rhtpa-2.1]"
```

**Result:** No results -- no sibling Vulnerability issue exists for CVE-2026-55123 in stream rhtpa-2.1.

**Action:** Create preemptive remediation tasks for stream rhtpa-2.1 (Case B).

## Preemptive Task Details

### Stream rhtpa-2.1 (no CVE Jira exists)

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks are created with the following characteristics:

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

The `security-preemptive` label distinguishes these tasks from standard remediation tasks. When PSIRT later creates a stream-specific CVE Jira for rhtpa-2.1, Step 4.4 reconciliation will link the preemptive tasks to the new CVE Jira and remove the `security-preemptive` label.

**Link type:** "Related" (not "Depend")

Preemptive tasks are linked to TC-8020 with the "Related" link type because TC-8020 belongs to a different stream (rhtpa-2.2). The "Depend" link type is reserved for tasks that belong to the same stream as their parent CVE Jira.

**Description prefix:**

Each preemptive task description includes the following prefix:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

### Preemptive Tasks Created

| Task | Summary | Stream | Labels | Link to TC-8020 |
|------|---------|--------|--------|-----------------|
| Upstream backport | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | rhtpa-2.1 | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| Downstream propagation | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | rhtpa-2.1 | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |

### Preemptive Task Comment on TC-8020

The following comment would be posted to TC-8020:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: upstream-task-key (security-preemptive) -- bump tokio to 1.42.0
- rhtpa-2.1: downstream-task-key (security-preemptive) -- update backend ref in rhtpa-release.0.3.z

These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---

## Comparison: Case A vs Case B

| Aspect | Case A (rhtpa-2.2) | Case B (rhtpa-2.1) |
|--------|---------------------|---------------------|
| CVE Jira exists? | Yes (TC-8020) | No |
| Labels | ai-generated-jira, Security, CVE-2026-55123 | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** |
| Link type to TC-8020 | **Depend** | **Related** |
| Description prefix | None (standard) | Preemptive remediation prefix noting TC-8020 |
| Upstream branch | release/0.4.z | release/0.3.z |
| Konflux release repo | rhtpa-release.0.4.z | rhtpa-release.0.3.z |
| tokio version shipped | 1.41.1 | 1.40.0 |
