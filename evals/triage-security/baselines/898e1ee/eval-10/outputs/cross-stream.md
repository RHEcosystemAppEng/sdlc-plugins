# Cross-Stream Impact — CVE-2026-55123 (tokio)

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

**JQL executed:**

```
project = TC AND issuetype = 10024 AND labels = "CVE-2026-55123" AND summary ~ "[rhtpa-2.1]"
```

**Result:** No issues found. Stream rhtpa-2.1 has no CVE Jira for CVE-2026-55123.

## Preemptive Task Details

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks are created per Step 7 Case B.

### Preemptive tasks for stream rhtpa-2.1

| Task | Summary | Labels | Link to TC-8020 |
|------|---------|--------|-----------------|
| Upstream backport | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive` | Related |
| Downstream propagation | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive` | Related |

### Key differences from standard (Case A) tasks

| Attribute | Case A (rhtpa-2.2) | Case B Preemptive (rhtpa-2.1) |
|-----------|-------------------|-------------------------------|
| Labels | `ai-generated-jira`, `Security`, `CVE-2026-55123` | `ai-generated-jira`, `Security`, `CVE-2026-55123`, **`security-preemptive`** |
| Link type to TC-8020 | **Depend** | **Related** |
| Description prefix | _(none)_ | Preemptive remediation note referencing TC-8020 (stream rhtpa-2.2) |
| Target branch (upstream) | release/0.4.z | release/0.3.z |
| Konflux repo (downstream) | rhtpa-release.0.4.z | rhtpa-release.0.3.z |

### Description prefix used in preemptive tasks

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
```

### Preemptive Task Comment

The following comment would be posted to TC-8020 after creating the preemptive tasks:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-task-key> (upstream backport, security-preemptive), <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---

### Reconciliation (Step 4.4)

When PSIRT eventually creates a CVE Jira for stream rhtpa-2.1 (e.g., `TC-XXXX` with summary `CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]`), the triage-security skill's Step 4.4 reconciliation will:

1. Find the preemptive tasks via JQL search for label `security-preemptive` + `CVE-2026-55123`
2. Re-link the preemptive tasks from "Related" to TC-8020 to "Depend" on the new stream-specific CVE Jira
3. Remove the `security-preemptive` label from the preemptive tasks
4. Post a reconciliation comment on the new CVE Jira noting the linked preemptive tasks
