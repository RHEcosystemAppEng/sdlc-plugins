# Cross-Stream Impact -- Case A

## Cross-Stream Impact Comment (to be posted on TC-8020)

```
Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on
lock file analysis.

Version impact across streams:

| Version     | Stream    | tokio version | Affected? |
|-------------|-----------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |

Sibling CVE Jira search (JQL: project = TC AND labels = 'CVE-2026-55123'
AND issuetype = 10024 AND key != TC-8020):
- Stream rhtpa-2.1: **No sibling CVE Jira found**

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks
have been created (see below).
```

## Preemptive Task Details

Stream **rhtpa-2.1** has no CVE Jira for CVE-2026-55123. Preemptive remediation tasks were created proactively from the cross-stream impact analysis of TC-8020 (stream rhtpa-2.2).

### Preemptive Tasks Created for rhtpa-2.1

| Task | Type | Summary | Labels | Link to TC-8020 |
|------|------|---------|--------|-----------------|
| (new) | Upstream bump | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| (new) | Downstream propagation | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |

### Preemptive Comment (to be posted on TC-8020)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: {{preemptive-upstream-rhtpa-2.1.key}} (upstream bump, security-preemptive)
- rhtpa-2.1: {{preemptive-downstream-rhtpa-2.1.key}} (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Link Topology

### Standard Tasks (rhtpa-2.2 -- current stream)

```
TC-8020 (CVE Vulnerability)
  |
  |-- Depend --> upstream-task-rhtpa-2.2 (Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2))
  |                |
  |                |-- Blocks --> downstream-task-rhtpa-2.2 (Propagate fix to rhtpa-release.0.4.z)
  |
  |-- Depend --> downstream-task-rhtpa-2.2
```

### Preemptive Tasks (rhtpa-2.1 -- no CVE Jira)

```
TC-8020 (CVE Vulnerability, stream rhtpa-2.2)
  |
  |-- Related --> preemptive-upstream-rhtpa-2.1 (Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1))
  |                  |                             Labels: security-preemptive
  |                  |
  |                  |-- Blocks --> preemptive-downstream-rhtpa-2.1 (Propagate fix to rhtpa-release.0.3.z)
  |                                  Labels: security-preemptive
  |
  |-- Related --> preemptive-downstream-rhtpa-2.1
```

## Reconciliation (Step 4.4 -- future)

When PSIRT creates a CVE Jira for stream rhtpa-2.1 with label CVE-2026-55123:

1. Step 4.4 will search for preemptive tasks: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`
2. Filter results to tasks with `(rhtpa-2.1)` in summary
3. For each matching preemptive task:
   - Link the new CVE Jira to the preemptive task with "Depend"
   - Remove the `security-preemptive` label
   - The preemptive task becomes a standard remediation task
4. Skip new remediation task creation for rhtpa-2.1 (already exists)

## Post-Triage Summary Comment (to be posted on TC-8020)

```
Triage summary for TC-8020 (CVE-2026-55123 tokio [rhtpa-2.2]):

Version Impact:
| Version     | Stream    | tokio version | Affected? |
|-------------|-----------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |

Affects Versions: correct as-is (RHTPA 2.2.0, RHTPA 2.2.1)

Triage outcome: remediation required

Remediation tasks (rhtpa-2.2, standard):
- {{upstream-rhtpa-2.2.key}}: upstream bump tokio to 1.42.0 on release/0.4.z
- {{downstream-rhtpa-2.2.key}}: downstream propagation to rhtpa-release.0.4.z
  (blocked by upstream task)

Cross-stream impact:
- rhtpa-2.1 is also affected (tokio 1.40.0 < 1.42.0)
- No CVE Jira exists for rhtpa-2.1

Preemptive remediation tasks (rhtpa-2.1, security-preemptive):
- {{preemptive-upstream-rhtpa-2.1.key}}: upstream bump tokio to 1.42.0 on release/0.3.z
- {{preemptive-downstream-rhtpa-2.1.key}}: downstream propagation to rhtpa-release.0.3.z
  (blocked by upstream preemptive task)
```
