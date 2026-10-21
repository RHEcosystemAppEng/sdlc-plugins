# Cross-Stream Impact Analysis: TC-8020

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020 documenting the cross-stream impact:

---

**Cross-stream impact**: tokio (versions before 1.42.0) also affects stream 2.1.x (rhtpa-2.1) based on lock file analysis.

| Stream | Version | tokio version | Affected? |
|--------|---------|---------------|-----------|
| 2.1.x | RHTPA 2.1.0 | 1.40.0 | YES |
| 2.1.x | RHTPA 2.1.1 | 1.40.0 | YES |

Stream 2.1.x ships tokio 1.40.0, which is below the fix threshold of 1.42.0.

Sibling CVE Jira search for stream rhtpa-2.1:
- JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`
- Result: **No sibling Vulnerability issues found** for CVE-2026-55123 in stream rhtpa-2.1

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks have been created.

---

## Preemptive Task Details

### Decision Logic

1. Issue TC-8020 is scoped to stream rhtpa-2.2 (suffix `[rhtpa-2.2]`).
2. Version impact analysis reveals stream 2.1.x is also affected (tokio 1.40.0 < fix threshold 1.42.0).
3. JQL search for sibling CVE Jiras with label CVE-2026-55123 returns **no results** for stream rhtpa-2.1.
4. Per Case A of the triage-security skill: create preemptive remediation tasks for the affected stream that lacks its own CVE Jira.

### Preemptive Tasks Created for Stream 2.1.x

| Task | Type | Summary | Labels |
|------|------|---------|--------|
| Task 3 | Upstream backport (preemptive) | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Task 4 | Downstream propagation (preemptive) | Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

### Preemptive Task Differences from Standard Tasks

| Aspect | Standard (2.2.x) | Preemptive (2.1.x) |
|--------|-------------------|---------------------|
| Labels | ai-generated-jira, Security, CVE-2026-55123 | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** |
| Link to TC-8020 | **Depend** | **Related** |
| Description prefix | (none) | Preemptive remediation notice referencing TC-8020 and stream rhtpa-2.2 |
| Target branch | release/0.4.z | release/0.3.z |
| Konflux release repo | rhtpa-release.0.4.z | rhtpa-release.0.3.z |

### Preemptive Comment on TC-8020

The following comment would be posted to TC-8020 after preemptive task creation:

---

Preemptive remediation tasks created for streams without CVE Jiras:

- **rhtpa-2.1**: Task 3 (upstream backport, security-preemptive), Task 4 (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the `security-preemptive` label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---

## Reconciliation (Step 4.4)

When PSIRT creates a CVE Jira for stream rhtpa-2.1 (e.g., a new Vulnerability issue with summary containing `[rhtpa-2.1]` and label `CVE-2026-55123`), the triage-security skill's Step 4.4 will:

1. Search for preemptive tasks matching CVE-2026-55123 with label `security-preemptive`
2. Find Tasks 3 and 4 whose summaries contain `(rhtpa-2.1)`
3. Link the new CVE Jira to the preemptive tasks with "Depend" (standard remediation linkage)
4. Remove the `security-preemptive` label from Tasks 3 and 4
5. Skip new remediation task creation for stream 2.1.x (already covered)

## Post-Triage Summary Comment

The following post-triage summary comment would be posted to TC-8020:

---

**Triage summary for TC-8020 (CVE-2026-55123 -- tokio use-after-free)**

**Version impact:**

| Version | Stream | tokio | Affected? | Notes |
|---------|--------|-------|-----------|-------|
| RHTPA 2.1.0 | 2.1.x | 1.40.0 | YES | cross-stream |
| RHTPA 2.1.1 | 2.1.x | 1.40.0 | YES | cross-stream |
| RHTPA 2.2.0 | 2.2.x | 1.41.1 | YES | in scope |
| RHTPA 2.2.1 | 2.2.x | 1.41.1 | YES | in scope |
| RHTPA 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |

**Affects Versions correction:** RHTPA 2.2.0, RHTPA 2.2.1 (scoped to stream 2.2.x per issue suffix)

**Triage outcome:** Remediation required

**Standard remediation tasks (stream 2.2.x):**
- Task 1: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2) -- upstream backport
- Task 2: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2) -- downstream propagation (blocked by Task 1)

**Preemptive remediation tasks (stream 2.1.x -- no CVE Jira exists):**
- Task 3: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) -- upstream backport (security-preemptive)
- Task 4: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) -- downstream propagation (security-preemptive, blocked by Task 3)

Label `ai-cve-triaged` added to TC-8020.

---
