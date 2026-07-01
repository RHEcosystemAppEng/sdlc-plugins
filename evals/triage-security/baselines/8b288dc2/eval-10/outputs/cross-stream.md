# Cross-Stream Impact — CVE-2026-55123 (TC-8020)

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

---

Cross-stream impact: tokio (versions before 1.42.0) also affects stream rhtpa-2.1 based on lock file analysis. Stream rhtpa-2.1 ships tokio 1.40.0 across all versions (RHTPA 2.1.0, RHTPA 2.1.1), which is below the fix threshold of 1.42.0.

No sibling CVE Jira exists for stream rhtpa-2.1. Preemptive remediation tasks have been created (see below).

---

## Sibling CVE Jira Search Results

JQL query:
```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020
```

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

## Preemptive Task Details

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks are created per Step 8 Case B.

### Preemptive Task Characteristics

- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Link type to TC-8020**: `Related` (not `Depend`, because the originating CVE belongs to a different stream)
- **Description prefix**: Includes preemptive remediation note referencing TC-8020 (stream rhtpa-2.2) as the originating CVE

### Preemptive Tasks Created for rhtpa-2.1

| Task | Summary | Labels | Link to TC-8020 |
|------|---------|--------|-----------------|
| Upstream backport | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| Downstream propagation | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |

### Description Prefix (included in all preemptive task descriptions)

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
```

### Upstream Backport Task (rhtpa-2.1)

- **Repository**: backend
- **Target Branch**: release/0.3.z (from Ecosystem Mappings for stream 2.1.x)
- **Fix**: Bump tokio to >= 1.42.0 in Cargo.lock
- **Affected versions**: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
- **Source commits**: v0.3.8, v0.3.12

### Downstream Propagation Task (rhtpa-2.1)

- **Repository**: rhtpa-release.0.3.z
- **Target Branch**: main
- **Source pinning method**: artifacts.lock.yaml (download URL contains tag)
- **Blocked by**: Upstream backport task (rhtpa-2.1)

## Preemptive Tasks Comment (posted to TC-8020)

The following comment would be posted to TC-8020 after preemptive task creation:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <upstream-task-preemptive-key> (upstream backport, security-preemptive)
- rhtpa-2.1: <downstream-task-preemptive-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---

## Reconciliation Path (Step 4.4)

When PSIRT eventually creates a CVE Jira for stream rhtpa-2.1 with label CVE-2026-55123, the triage of that new issue will:

1. **Search** for preemptive tasks: JQL `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`
2. **Filter** to tasks whose summary contains `(rhtpa-2.1)`
3. **Link** the new CVE Jira to the preemptive tasks with "Depend" (standard remediation linkage)
4. **Remove** the `security-preemptive` label from the tasks
5. The preemptive tasks become standard remediation tasks for the new CVE Jira
