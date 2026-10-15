# Cross-Stream Impact Analysis: TC-8020

## Summary

Issue TC-8020 (CVE-2026-55123) is scoped to stream **rhtpa-2.2** via its summary suffix `[rhtpa-2.2]`. Version impact analysis (Step 2) reveals that stream **rhtpa-2.1** also ships tokio < 1.42.0 and is affected by this vulnerability.

A JQL search for sibling CVE Jiras with label `CVE-2026-55123` returned **no results** for stream rhtpa-2.1 -- no CVE Jira exists for that stream.

This triggers **Case A** (cross-stream impact with preemptive remediation).

## Cross-Stream Version Impact

| Version | Stream | tokio version | Fix threshold | Affected? | In issue scope? |
|---------|--------|---------------|---------------|-----------|-----------------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | 1.42.0 | **YES** | No |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | 1.42.0 | **YES** | No |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | 1.42.0 | **YES** | Yes |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | 1.42.0 | **YES** | Yes |
| RHTPA 2.2.2 | rhtpa-2.2 | -- | 1.42.0 | **YES** | Yes (retag of 2.2.1) |

## Sibling CVE Jira Search

**JQL executed:**
```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020
```

**Result:** No sibling Vulnerability issues found.

| Stream | Sibling CVE Jira? | Action |
|--------|-------------------|--------|
| rhtpa-2.2 | TC-8020 (current issue) | Standard remediation (Case B) |
| rhtpa-2.1 | **None found** | Preemptive remediation (Case A) |

## Cross-Stream Impact Comment (Proposed)

The following comment would be posted to TC-8020:

---

**Proposed Jira action -- add comment to TC-8020 (not executed):**

> Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.
>
> | Stream | Versions | tokio version | Sibling CVE Jira? |
> |--------|----------|---------------|-------------------|
> | rhtpa-2.1 | RHTPA 2.1.0, 2.1.1 | 1.40.0 | No |
>
> No sibling CVE Jira exists for stream rhtpa-2.1. Preemptive remediation tasks
> have been created (see below).
>
> These streams may require separate PSIRT triage.

---

## Preemptive Task Details

Since no CVE Jira exists for stream rhtpa-2.1, the following preemptive remediation tasks are proposed. These tasks use the `security-preemptive` label and "Related" link type (not "Depend") to the originating CVE TC-8020.

### Preemptive tasks for stream rhtpa-2.1

| # | Task Type | Summary | Labels | Link to TC-8020 |
|---|-----------|---------|--------|-----------------|
| 1 | Upstream (Cargo) | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| 2 | Downstream propagation | Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |

- Preemptive upstream task targets branch `release/0.3.z` in the `backend` repository
- Preemptive downstream task targets `main` in the `rhtpa-release.0.3.z` Konflux release repo
- Downstream is blocked by upstream (`Blocks` link between the two preemptive tasks)
- Both tasks carry the `security-preemptive` label
- Both tasks include a preemptive remediation prefix in their description noting the originating CVE (TC-8020) and stream (rhtpa-2.2)

## Preemptive Task Comment (Proposed)

The following comment would be posted to TC-8020 after preemptive task creation:

---

**Proposed Jira action -- add comment to TC-8020 (not executed):**

> Preemptive remediation tasks created for streams without CVE Jiras:
> - rhtpa-2.1: <preemptive-upstream-task-key> (upstream bump, security-preemptive), <preemptive-downstream-task-key> (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.

---

## Reconciliation Path (Step 4.4)

When PSIRT eventually creates a CVE Jira for stream rhtpa-2.1 (e.g., TC-XXXX with summary `CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]`), the triage of that issue will:

1. **Step 4.4** will search for preemptive tasks: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`
2. Filter results to tasks whose summary contains `(rhtpa-2.1)`
3. Find the two preemptive tasks created here
4. **Link** the new CVE Jira to the preemptive tasks with "Depend" (standard remediation linkage)
5. **Remove** the `security-preemptive` label from both tasks
6. **Skip** new remediation task creation for rhtpa-2.1 (tasks already exist)

This reconciliation converts preemptive tasks into standard remediation tasks owned by the stream-specific CVE Jira.
