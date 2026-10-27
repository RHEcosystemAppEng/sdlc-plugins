# Cross-Stream Impact — CVE-2026-55123 (tokio)

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

---

Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.

| Version     | Stream    | tokio version | Affected? |
|-------------|-----------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |

Stream rhtpa-2.1 has no existing CVE Jira for CVE-2026-55123. Preemptive
remediation tasks have been created for that stream.

---

## Sibling CVE Jira Search Results

JQL: `project = TC AND issuetype = 10024 AND labels = CVE-2026-55123 ORDER BY created DESC`

| Stream    | Sibling CVE Jira | Result |
|-----------|------------------|--------|
| rhtpa-2.2 | TC-8020          | Current issue (scoped to this stream) |
| rhtpa-2.1 | (none)           | No sibling found -- preemptive tasks required |

## Preemptive Task Details

Since no CVE Jira exists for stream rhtpa-2.1, preemptive remediation tasks
are created with the following distinguishing characteristics:

### Differences from Standard Remediation

| Attribute | Standard (Case A, rhtpa-2.2) | Preemptive (Case B, rhtpa-2.1) |
|-----------|------------------------------|--------------------------------|
| Labels | `ai-generated-jira`, `Security`, `CVE-2026-55123` | `ai-generated-jira`, `Security`, `CVE-2026-55123`, **`security-preemptive`** |
| Link to TC-8020 | **Depend** | **Related** |
| Description prefix | (none) | Preemptive remediation note referencing TC-8020 |
| Reconciliation | N/A | When PSIRT creates a stream-specific CVE Jira for rhtpa-2.1, Step 4.4 reconciliation will link the tasks and remove the `security-preemptive` label |

### Preemptive Tasks Created for rhtpa-2.1

#### Task: Upstream Backport (Preemptive)

- **Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Repository**: backend
- **Target Branch**: release/0.3.z
- **Link to TC-8020**: Related (not Depend -- different stream)
- **Description prefix**:
  > **Preemptive remediation**: This task was created proactively from cross-stream
  > impact analysis of TC-8020 (stream rhtpa-2.2).
  > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
  > this task will be linked and the `security-preemptive` label removed.

#### Task: Downstream Propagation (Preemptive)

- **Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Repository**: rhtpa-release.0.3.z
- **Target Branch**: main
- **Link to TC-8020**: Related (not Depend -- different stream)
- **Blocked by**: Upstream backport task for rhtpa-2.1 (Blocks link)
- **Description prefix**:
  > **Preemptive remediation**: This task was created proactively from cross-stream
  > impact analysis of TC-8020 (stream rhtpa-2.2).
  > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
  > this task will be linked and the `security-preemptive` label removed.

## Preemptive Task Comment on TC-8020

The following comment would be posted to the originating CVE Jira (TC-8020):

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: upstream backport task (security-preemptive), downstream propagation task (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---

## Reconciliation Path

When PSIRT eventually creates a Vulnerability issue for CVE-2026-55123
scoped to stream rhtpa-2.1, the triage-security skill's Step 4.4
(Preemptive Task Reconciliation) will:

1. Search for existing tasks with labels `CVE-2026-55123` and `security-preemptive`
2. Find the two preemptive tasks created here
3. Link them to the new stream-specific CVE Jira with Depend link type
4. Remove the `security-preemptive` label from each task
5. Post a reconciliation comment on both the new CVE Jira and TC-8020
