# Cross-Stream Impact — TC-8020

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

---

Cross-stream impact: tokio (versions before 1.42.0) also affects stream rhtpa-2.1
based on lock file analysis.

Version impact across streams:

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES |

Stream rhtpa-2.1 ships tokio 1.40.0, which is below the fix threshold of 1.42.0.
No companion CVE Jira exists for stream rhtpa-2.1 (JQL search for label CVE-2026-55123
with stream suffix [rhtpa-2.1] returned no results).

These streams are tracked by companion issues (see Related links) or may require
separate PSIRT triage.

---

## Sibling CVE Jira Search Results

**JQL**: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result**: No sibling Vulnerability issues found.

- Stream rhtpa-2.2: covered by TC-8020 (current issue)
- Stream rhtpa-2.1: **no CVE Jira exists** -- preemptive remediation required

## Preemptive Task Details

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks are
created per Case A of the triage-security skill. These tasks carry the
`security-preemptive` label and use "Related" link type (not "Depend") to
TC-8020 because the originating CVE belongs to a different stream.

### Preemptive Tasks Created for rhtpa-2.1

| Task | Summary | Labels | Link to TC-8020 |
|------|---------|--------|-----------------|
| Upstream backport | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| Downstream propagation | Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |

### Preemptive Task Comment

The following comment would be posted to TC-8020 after creating preemptive tasks:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: upstream backport task (security-preemptive) -- bump tokio to 1.42.0 on release/0.3.z
- rhtpa-2.1: downstream propagation task (security-preemptive) -- update rhtpa-backend ref in rhtpa-release.0.3.z

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation
will link them and remove the label.

---

## Link Topology

### Standard remediation (rhtpa-2.2)

```
TC-8020 (CVE Vulnerability)
  |-- Depend --> upstream backport task (rhtpa-2.2)
  |-- Depend --> downstream propagation task (rhtpa-2.2)
                    |-- Blocks --> upstream backport task (rhtpa-2.2)
```

### Preemptive remediation (rhtpa-2.1)

```
TC-8020 (CVE Vulnerability, stream rhtpa-2.2)
  |-- Related --> preemptive upstream backport task (rhtpa-2.1)
  |-- Related --> preemptive downstream propagation task (rhtpa-2.1)
                    |-- Blocks --> preemptive upstream backport task (rhtpa-2.1)
```

## Reconciliation (Step 4.4)

When PSIRT creates a CVE Jira for stream rhtpa-2.1 (e.g., TC-XXXX with
summary `CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]`),
the triage of that issue will:

1. Search for preemptive tasks: JQL `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`
2. Filter to tasks with `(rhtpa-2.1)` in summary
3. Link the new CVE Jira to the preemptive tasks with "Depend"
4. Remove the `security-preemptive` label from the tasks
5. Skip new remediation task creation (tasks already exist)
