# Cross-Stream Impact — CVE-2026-55123

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

No sibling CVE Jira exists for stream rhtpa-2.1. Preemptive remediation tasks have been created.

---

## Sibling CVE Jira Search Results

**JQL**: `project = TC AND issuetype = 10024 AND labels = "CVE-2026-55123" AND summary ~ "[rhtpa-2.1]"`

**Result**: No issues found. Stream rhtpa-2.1 has no CVE Jira for CVE-2026-55123.

**Action**: Create preemptive remediation tasks for stream rhtpa-2.1 (Case B).

## Preemptive Task Details

### Stream rhtpa-2.1 (no CVE Jira exists)

Since no sibling CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks are created with the following distinguishing characteristics:

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

The `security-preemptive` label distinguishes these from standard remediation tasks created via Case A.

**Link type**: Related (not Depend)

Preemptive tasks are linked to the originating CVE TC-8020 via "Related" link type, not "Depend", because the originating CVE belongs to a different stream (rhtpa-2.2).

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-task-key>,
  type: "Related"
)
```

**Description prefix**: Each preemptive task description includes a prefix noting TC-8020 as the originating CVE:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

### Preemptive Tasks Created

| Task | Type | Stream | Summary | Labels | Link to TC-8020 |
|------|------|--------|---------|--------|-----------------|
| Upstream backport | Task | rhtpa-2.1 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| Downstream propagation | Task | rhtpa-2.1 | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |

The downstream propagation task is also blocked by the upstream backport task (Blocks link).

## Preemptive Task Comment on TC-8020

The following comment would be posted to TC-8020 listing the preemptive tasks:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-task-key> (upstream backport, security-preemptive)
- rhtpa-2.1: <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---

## Reconciliation (Step 4.4)

When PSIRT later creates a stream-specific CVE Jira for rhtpa-2.1 with label CVE-2026-55123, the triage-security skill's Step 4.4 reconciliation will:

1. Search for existing preemptive tasks with labels `CVE-2026-55123` and `security-preemptive`
2. Link the preemptive tasks to the new stream-specific CVE Jira (Depend link)
3. Remove the `security-preemptive` label from each task
4. The tasks transition from preemptive to standard remediation tasks
