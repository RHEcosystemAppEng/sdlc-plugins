# Cross-Stream Impact Analysis: TC-8020

## Cross-Stream Impact Summary

CVE-2026-55123 (tokio < 1.42.0) affects versions across **two** streams:

| Stream | Versions Affected | tokio Version | In Issue Scope? |
|--------|-------------------|---------------|-----------------|
| 2.2.x (rhtpa-2.2) | RHTPA 2.2.0, 2.2.1, 2.2.2 | 1.41.1 | **Yes** (issue stream) |
| 2.1.x (rhtpa-2.1) | RHTPA 2.1.0, 2.1.1 | 1.40.0 | **No** (cross-stream) |

## Sibling CVE Jira Search Results

JQL query (simulated):
```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020
```

**Result: No sibling Vulnerability issues found.**

Specifically, no CVE Jira exists for stream rhtpa-2.1. This triggers Case B
(preemptive remediation) for that stream.

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

---

**Cross-stream impact:** tokio (versions before 1.42.0) also affects stream
**rhtpa-2.1** based on lock file analysis.

| Stream | tokio version | Fix threshold | Affected? |
|--------|---------------|---------------|-----------|
| rhtpa-2.1 | 1.40.0 | 1.42.0 | YES |

No sibling CVE Jira exists for stream rhtpa-2.1. Preemptive remediation tasks
have been created (see below).

---

## Preemptive Task Details

Since stream 2.1.x has no CVE Jira for CVE-2026-55123, the following preemptive
remediation tasks are proposed per Step 7 Case B:

### Preemptive Upstream Backport Task (rhtpa-2.1)

| Field | Value |
|-------|-------|
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Type | Task |
| Labels | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** |
| Repository | rhtpa-backend |
| Target Branch | release/0.3.z |
| Link to TC-8020 | **Related** (not Depend -- cross-stream preemptive) |

Description includes preemptive remediation prefix:
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

### Preemptive Downstream Propagation Task (rhtpa-2.1)

| Field | Value |
|-------|-------|
| Summary | Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) |
| Type | Task |
| Labels | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** |
| Repository | rhtpa-release.0.3.z |
| Target Branch | main |
| Link to TC-8020 | **Related** (not Depend -- cross-stream preemptive) |
| Blocked by | Preemptive upstream backport task (Blocks link type) |

Description includes the same preemptive remediation prefix.

## Preemptive Task Comment

The following comment would be posted to TC-8020 after preemptive task creation:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- **rhtpa-2.1**: upstream backport task (security-preemptive) -- bump tokio to 1.42.0 on release/0.3.z
- **rhtpa-2.1**: downstream propagation task (security-preemptive) -- update rhtpa-backend ref in rhtpa-release.0.3.z

These tasks use the "Related" link type and carry the `security-preemptive`
label. When PSIRT creates stream-specific CVE Jiras for rhtpa-2.1, Step 4.4
reconciliation will link them and remove the label.

---

## Reconciliation Path (Step 4.4)

When PSIRT eventually creates a CVE Jira for stream rhtpa-2.1 (e.g., TC-XXXX
with summary containing `[rhtpa-2.1]`), the triage of that new issue will:

1. Search for preemptive tasks: JQL `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`
2. Filter to tasks whose summary contains `(rhtpa-2.1)`
3. Link the new CVE Jira to the preemptive tasks with "Depend" (standard remediation linkage)
4. Remove the `security-preemptive` label from the tasks
5. The preemptive tasks become standard remediation tasks for the new CVE Jira

This avoids duplicate remediation work -- the fix is already in progress.
