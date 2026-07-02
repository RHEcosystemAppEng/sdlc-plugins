# Cross-Stream Impact Analysis for CVE-2026-55123 (TC-8020)

## Cross-Stream Impact Summary

The version impact analysis (Step 2) reveals that tokio < 1.42.0 affects versions
across **two** streams:

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | **YES** |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | **YES** |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | **YES** |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | **YES** |

- **Current issue stream (rhtpa-2.2):** TC-8020 tracks this stream -- Case A remediation applies
- **Other affected stream (rhtpa-2.1):** No CVE Jira exists -- Case B preemptive remediation applies

## Sibling CVE Jira Search

JQL executed:
```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020
```

**Result:** No results. No sibling Vulnerability issues found for CVE-2026-55123 in any other stream.

Specifically, stream rhtpa-2.1 has no CVE Jira for CVE-2026-55123. This triggers
Case B preemptive remediation for that stream.

## Cross-Stream Impact Comment (to be posted on TC-8020)

```
Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock
file analysis (tokio 1.40.0 shipped in RHTPA 2.1.0 and RHTPA 2.1.1).

No companion CVE Jira exists for stream rhtpa-2.1 -- preemptive remediation tasks
have been created (see below).
```

## Preemptive Remediation Tasks (Case B)

Since stream rhtpa-2.1 is affected but has no CVE Jira, proactive remediation tasks
are created with the following distinguishing characteristics:

- **Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
- **Link type:** "Related" (not "Depend") to originating CVE Jira TC-8020
- **Description prefix:** Includes preemptive remediation note referencing TC-8020 and stream rhtpa-2.2

### Preemptive Task 1: Upstream Backport (rhtpa-2.1)

| Field | Value |
|-------|-------|
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Type | Task |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Repository | backend |
| Target Branch | release/0.3.z |
| Link to TC-8020 | Related |

### Preemptive Task 2: Downstream Propagation (rhtpa-2.1)

| Field | Value |
|-------|-------|
| Summary | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) |
| Type | Task |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Repository | rhtpa-release.0.3.z |
| Target Branch | main |
| Link to TC-8020 | Related |
| Blocked by | Preemptive upstream task (Blocks link) |

## Comment to Post on TC-8020 (Preemptive Task Summary)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-task-key> (upstream backport, security-preemptive)
- rhtpa-2.1: <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Reconciliation Path (Step 4.4)

When PSIRT eventually creates a CVE Jira for CVE-2026-55123 scoped to stream rhtpa-2.1,
the triage of that new issue will:

1. Search for preemptive tasks: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`
2. Find the preemptive tasks created above (matching stream rhtpa-2.1 in summary)
3. Link the new CVE Jira to the preemptive tasks with "Depend" (standard remediation linkage)
4. Remove the `security-preemptive` label from each task
5. Skip new remediation task creation in Step 8 (tasks already exist)
