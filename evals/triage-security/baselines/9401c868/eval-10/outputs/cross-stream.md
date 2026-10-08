# Cross-Stream Impact Analysis: CVE-2026-55123

## Cross-Stream Impact Comment (to be posted on TC-8020)

Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on
lock file analysis.

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES |

Stream rhtpa-2.1 ships tokio 1.40.0, which is below the fix threshold of
1.42.0. This stream is tracked by companion issues (see Related links) or
may require separate PSIRT triage.

## Sibling CVE Jira Search Results

JQL query:
```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020
```

**Result: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.**

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks
are created per Case A of the triage-security skill.

## Preemptive Remediation Tasks for Stream rhtpa-2.1

### Preemptive Task 1: Upstream backport (rhtpa-2.1)

| Field | Value |
|-------|-------|
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Issue Type | Task |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Repository | backend |
| Target Branch | release/0.3.z |
| Link to TC-8020 | Related |
| Affected versions | RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0) |

Description prefix:
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for stream rhtpa-2.1. When PSIRT creates one, this task will be
> linked and the `security-preemptive` label removed.

### Preemptive Task 2: Downstream propagation (rhtpa-2.1)

| Field | Value |
|-------|-------|
| Summary | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) |
| Issue Type | Task |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Repository | rhtpa-release.0.3.z |
| Target Branch | main |
| Link to TC-8020 | Related |
| Blocked by | Preemptive Task 1 (upstream backport must merge first) |
| Source pinning method | artifacts.lock.yaml (download URL contains tag) |

Description prefix:
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for stream rhtpa-2.1. When PSIRT creates one, this task will be
> linked and the `security-preemptive` label removed.

## Preemptive Task Comment (to be posted on TC-8020)

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: [upstream-task-key] (Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)) -- security-preemptive
- rhtpa-2.1: [downstream-task-key] (Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)) -- security-preemptive

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

## Jira Linkage for Preemptive Tasks

```
# Link preemptive upstream task to originating CVE (Related, not Depend)
jira.create_link(
  inwardIssue: TC-8020,
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)

# Link preemptive downstream task to originating CVE (Related, not Depend)
jira.create_link(
  inwardIssue: TC-8020,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

# Link preemptive upstream blocks downstream (Blocks)
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

## Reconciliation Notes

When PSIRT creates a CVE Jira for stream rhtpa-2.1 with label CVE-2026-55123,
Step 4.4 (Preemptive task reconciliation) will:

1. Search for tasks with labels `security-preemptive` AND `CVE-2026-55123`
2. Filter to tasks whose summary contains `(rhtpa-2.1)`
3. Link the new CVE Jira to the preemptive tasks with "Depend" (standard remediation linkage)
4. Remove the `security-preemptive` label from both tasks
5. The preemptive tasks become standard remediation tasks for the new CVE Jira
