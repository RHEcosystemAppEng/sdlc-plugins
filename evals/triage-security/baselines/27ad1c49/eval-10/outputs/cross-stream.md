# Cross-Stream Impact — CVE-2026-55123 (tokio)

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020 (the originating CVE Jira
scoped to rhtpa-2.2) documenting the cross-stream impact finding:

---

**Cross-stream impact**: tokio (versions before 1.42.0) also affects stream
rhtpa-2.1 based on lock file analysis.

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |

Stream rhtpa-2.1 ships tokio 1.40.0, which is below the fix threshold of
1.42.0. No sibling CVE Jira exists for stream rhtpa-2.1 (confirmed by JQL
search for label CVE-2026-55123 with stream suffix rhtpa-2.1 returning no
results).

Preemptive remediation tasks have been created for stream rhtpa-2.1 (see below).
These tasks carry the `security-preemptive` label. When PSIRT creates a
stream-specific CVE Jira for rhtpa-2.1, Step 4.4 reconciliation will link
the new CVE Jira to these tasks and remove the `security-preemptive` label.

---

## Sibling CVE Jira Search Results

**JQL executed** (simulated):
```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020
```

**Results**: No sibling Vulnerability issues found.

Specifically, no CVE Jira exists for stream rhtpa-2.1. Stream rhtpa-2.2 is
tracked by the current issue TC-8020.

## Preemptive Task Details

Since stream rhtpa-2.1 is affected but has no CVE Jira, preemptive
remediation tasks are created with the following characteristics:

### Preemptive task differences from standard tasks

| Attribute | Standard (rhtpa-2.2) | Preemptive (rhtpa-2.1) |
|-----------|---------------------|------------------------|
| Labels | ai-generated-jira, Security, CVE-2026-55123 | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** |
| Link to CVE | **Depend** (to TC-8020) | **Related** (to TC-8020) |
| Description prefix | (none) | Preemptive remediation notice referencing TC-8020 |
| Remediation variant | Dependency bump (fix available upstream) | Upstream backport (fix NOT available on release/0.3.z) |

### Preemptive tasks created for rhtpa-2.1

1. **Upstream backport task**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
   - Repository: backend
   - Target branch: release/0.3.z
   - Labels: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
   - Link: Related to TC-8020
   - Reason: upstream branch release/0.3.z ships tokio 1.40.0 (not fixed);
     requires an upstream backport to bump tokio

2. **Downstream propagation task**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
   - Repository: rhtpa-release.0.3.z
   - Target branch: main
   - Labels: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
   - Link: Related to TC-8020; Blocks (blocked by upstream backport task)
   - Source pinning method: artifacts.lock.yaml

### Preemptive remediation comment on TC-8020

The following comment would be posted to TC-8020 after preemptive task creation:

---

Preemptive remediation tasks created for streams without CVE Jiras:

- **rhtpa-2.1**: upstream backport task (security-preemptive) -- bump tokio to 1.42.0 on release/0.3.z
- **rhtpa-2.1**: downstream propagation task (security-preemptive) -- update backend ref in rhtpa-release.0.3.z

These tasks use the "Related" link type to TC-8020 and carry the
`security-preemptive` label. When PSIRT creates a stream-specific CVE Jira
for rhtpa-2.1, Step 4.4 reconciliation will:
1. Link the new CVE Jira to these tasks with "Depend"
2. Remove the `security-preemptive` label from each task

---

## Reconciliation Path (Step 4.4)

When PSIRT creates a CVE Jira for stream rhtpa-2.1 (e.g., TC-XXXX with
summary "CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]"),
the triage of that issue will:

1. Search for preemptive tasks matching CVE-2026-55123 with label
   `security-preemptive` and stream rhtpa-2.1 in the summary
2. Find the preemptive upstream backport and downstream propagation tasks
3. Link the new CVE Jira to each task with "Depend" (standard remediation link)
4. Remove the `security-preemptive` label from each task
5. Skip creating new remediation tasks for rhtpa-2.1 (already covered)

The preemptive tasks become standard remediation tasks for the new CVE Jira,
avoiding duplicate work.

## Cross-Stream Summary

| Stream | Affected? | CVE Jira | Remediation | Task Type |
|--------|-----------|----------|-------------|-----------|
| rhtpa-2.2 | YES (2.2.0, 2.2.1, 2.2.2) | TC-8020 | Dependency bump + downstream propagation | Standard |
| rhtpa-2.1 | YES (2.1.0, 2.1.1) | None | Upstream backport + downstream propagation | Preemptive (security-preemptive) |
