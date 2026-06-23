# Cross-Stream Impact Analysis

## Cross-Stream Impact Detection

TC-8020 (CVE-2026-55123) is scoped to stream **rhtpa-2.2**. Version impact analysis across all configured Version Streams reveals that stream **rhtpa-2.1** is also affected.

| Stream | Versions Affected | tokio Version | Fix Threshold | Status |
|--------|-------------------|---------------|---------------|--------|
| rhtpa-2.2 (issue stream) | RHTPA 2.2.0, RHTPA 2.2.1 | 1.41.1 | 1.42.0 | Affected -- standard remediation (Case A) |
| rhtpa-2.1 (other stream) | RHTPA 2.1.0, RHTPA 2.1.1 | 1.40.0 | 1.42.0 | Affected -- no CVE Jira exists (Case B) |

## Sibling CVE Jira Search

JQL executed (simulated):
```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020
```

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in any stream.

- Stream rhtpa-2.2: Covered by TC-8020 (the current issue)
- Stream rhtpa-2.1: **No CVE Jira exists** -- triggers preemptive task creation

## Cross-Stream Impact Comment

The following comment is posted to TC-8020:

---

Cross-stream impact: tokio (versions before 1.42.0) also affects stream(s) rhtpa-2.1 based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

---

## Preemptive Task Details (rhtpa-2.1)

Since no sibling CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks are created per Step 7 Case B.

### Preemptive Task Characteristics

| Property | Standard (Case A) | Preemptive (Case B) |
|----------|-------------------|---------------------|
| Labels | ai-generated-jira, Security, CVE-2026-55123 | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** |
| Link to TC-8020 | Depend | **Related** |
| Description prefix | (none) | Preemptive remediation note referencing TC-8020 as originating CVE |

### Preemptive Tasks Created

**Task 1 (Upstream Backport -- rhtpa-2.1):**
- Summary: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)`
- Labels: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
- Repository: rhtpa-backend
- Target branch: release/0.3.z
- Link to TC-8020: **Related** (not Depend -- because TC-8020 belongs to a different stream)
- Description includes preemptive prefix:
  > **Preemptive remediation**: This task was created proactively from cross-stream
  > impact analysis of TC-8020 (stream rhtpa-2.2).
  > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
  > this task will be linked and the `security-preemptive` label removed.

**Task 2 (Downstream Propagation -- rhtpa-2.1):**
- Summary: `Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- Labels: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
- Repository: rhtpa-release.0.3.z
- Target branch: main
- Link to TC-8020: **Related** (not Depend)
- Blocked by: upstream preemptive task (Blocks link)
- Description includes same preemptive prefix referencing TC-8020

### Preemptive Task Comment on TC-8020

The following comment is posted to TC-8020 after preemptive task creation:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-task-key> (security-preemptive), <preemptive-downstream-task-key> (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---

## Reconciliation Notes

When PSIRT eventually creates a CVE Jira for CVE-2026-55123 scoped to stream rhtpa-2.1, Step 4.4 (Preemptive Task Reconciliation) of the triage on that new issue will:

1. Find the existing preemptive tasks via JQL: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`
2. Filter to tasks matching stream rhtpa-2.1 (summary contains `(rhtpa-2.1)`)
3. Link the new CVE Jira to the preemptive tasks with "Depend" (standard remediation linkage)
4. Remove the `security-preemptive` label from the tasks
5. Skip new remediation task creation since tasks already exist
