# Cross-Stream Impact Analysis: CVE-2026-55123

## Cross-Stream Impact Comment (to be posted on TC-8020)

```
Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1
based on lock file analysis.

Version impact across streams:

| Version     | Stream    | tokio version | Affected? |
|-------------|-----------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |

Stream rhtpa-2.1 does not have a companion CVE Jira for CVE-2026-55123.
Preemptive remediation tasks have been created for this stream
(see below).
```

## Sibling CVE Jira Search Results

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

- Stream rhtpa-2.2: TC-8020 (current issue) -- this is the originating CVE Jira
- Stream rhtpa-2.1: **No CVE Jira exists** -- preemptive remediation required

## Preemptive Task Details (Stream rhtpa-2.1)

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks are created
per Case A of the triage-security skill (SKILL.md Step 8).

### Tasks Created

| Task | Type | Stream | Summary | Labels | Link to TC-8020 |
|------|------|--------|---------|--------|-----------------|
| (preemptive-upstream) | Upstream Backport | rhtpa-2.1 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| (preemptive-downstream) | Downstream Propagation | rhtpa-2.1 | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |

### Key Differences from Standard Remediation Tasks

1. **Labels**: Include `security-preemptive` alongside standard labels
2. **Link type**: "Related" to TC-8020 (not "Depend"), because TC-8020 belongs to stream rhtpa-2.2, not rhtpa-2.1
3. **Description prefix**: Each task includes a preemptive remediation note referencing the originating CVE Jira (TC-8020) and stream (rhtpa-2.2)
4. **Blocking relationship**: The downstream propagation task is blocked by the upstream backport task (same as standard tasks)

### Preemptive Task Comment (to be posted on TC-8020)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: (preemptive-upstream-key) upstream backport (security-preemptive)
- rhtpa-2.1: (preemptive-downstream-key) downstream propagation (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Reconciliation Lifecycle

When PSIRT eventually creates a CVE Jira for stream rhtpa-2.1 (e.g., TC-XXXX with summary
"CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]"), the triage-security
skill's Step 4.4 (Preemptive Task Reconciliation) will:

1. **Search** for preemptive tasks with labels `security-preemptive` and `CVE-2026-55123`
2. **Filter** to tasks whose summary contains `(rhtpa-2.1)`
3. **Link** the new CVE Jira to the preemptive tasks with "Depend" (standard remediation linkage)
4. **Remove** the `security-preemptive` label from the tasks
5. The preemptive tasks become standard remediation tasks for the new CVE Jira

## Affected Versions by Stream

### Stream rhtpa-2.1 (preemptive)
- RHTPA 2.1.0: tokio 1.40.0 -- AFFECTED (tag v0.3.8)
- RHTPA 2.1.1: tokio 1.40.0 -- AFFECTED (tag v0.3.12)
- Upstream branch: release/0.3.z
- Konflux release repo: rhtpa-release.0.3.z

### Stream rhtpa-2.2 (current issue scope)
- RHTPA 2.2.0: tokio 1.41.1 -- AFFECTED (tag v0.4.5)
- RHTPA 2.2.1: tokio 1.41.1 -- AFFECTED (tag v0.4.8)
- Upstream branch: release/0.4.z
- Konflux release repo: rhtpa-release.0.4.z
