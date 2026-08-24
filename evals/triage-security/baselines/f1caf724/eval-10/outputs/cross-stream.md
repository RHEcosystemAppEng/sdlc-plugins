# Cross-Stream Impact Analysis: CVE-2026-55123

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

---

Cross-stream impact: tokio (versions before 1.42.0) also affects stream rhtpa-2.1 based on lock file analysis.

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES |

Stream rhtpa-2.1 ships tokio 1.40.0, which is below the fix threshold of 1.42.0.

---

## Sibling CVE Jira Search Results

JQL executed: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks are created per Case A.

## Preemptive Task Details

### Stream rhtpa-2.1 -- No CVE Jira exists

Preemptive remediation tasks created for stream rhtpa-2.1:

| Task | Type | Summary | Labels | Link to TC-8020 |
|------|------|---------|--------|-----------------|
| (upstream) | Upstream Backport | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| (downstream) | Downstream Propagation | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |

### Preemptive Task Characteristics

- **Labels**: Include `security-preemptive` alongside standard labels (`ai-generated-jira`, `Security`, `CVE-2026-55123`)
- **Link type**: "Related" (not "Depend") to TC-8020, because TC-8020 belongs to stream rhtpa-2.2, not rhtpa-2.1
- **Description prefix**: Each task includes a preemptive remediation note referencing TC-8020 (stream rhtpa-2.2) as the originating CVE Jira
- **Blocking relationship**: The downstream propagation task is blocked by the upstream backport task within the rhtpa-2.1 stream
- **Reconciliation**: When PSIRT creates a stream-specific CVE Jira for rhtpa-2.1, Step 4.4 reconciliation will link the preemptive tasks to the new CVE Jira and remove the `security-preemptive` label

## Comment to TC-8020 (Preemptive Task Notification)

The following comment would be posted to TC-8020:

---

Preemptive remediation tasks created for streams without CVE Jiras:

- **rhtpa-2.1**: upstream backport task (security-preemptive) -- bump tokio to 1.42.0 on release/0.3.z
- **rhtpa-2.1**: downstream propagation task (security-preemptive) -- update backend ref in rhtpa-release.0.3.z

These tasks use the "Related" link type and carry the `security-preemptive` label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---

## Summary

| Stream | CVE Jira Exists? | Action Taken | Task Count |
|--------|-----------------|--------------|------------|
| rhtpa-2.2 | Yes (TC-8020) | Standard remediation (Case B) | 2 (upstream + downstream) |
| rhtpa-2.1 | No | Preemptive remediation (Case A) | 2 (upstream + downstream) |

Total tasks: 4 (2 standard for rhtpa-2.2 + 2 preemptive for rhtpa-2.1)
