# Cross-Stream Impact — TC-8020

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

---

Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES |

Stream rhtpa-2.1 has no companion CVE Jira for CVE-2026-55123. Preemptive remediation tasks have been created (see below).

---

## Sibling CVE Jira Search Results

JQL query: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result**: No sibling Vulnerability issues found. Stream rhtpa-2.1 has no CVE Jira for CVE-2026-55123.

## Preemptive Task Creation (Case B)

Since no CVE Jira exists for stream rhtpa-2.1, proactive preemptive remediation tasks are created per Step 7 Case B.

### Preemptive Task Details

#### Upstream Backport Task (rhtpa-2.1)

- **Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
- **Repository**: backend
- **Target Branch**: release/0.3.z
- **Link to TC-8020**: "Related" (not "Depend" -- because the originating CVE belongs to a different stream)
- **Description prefix**: Preemptive remediation note referencing TC-8020 (stream rhtpa-2.2)

#### Downstream Propagation Subtask (rhtpa-2.1)

- **Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
- **Repository**: rhtpa-release.0.3.z
- **Target Branch**: main
- **Link to TC-8020**: "Related" (not "Depend")
- **Blocked by**: Preemptive upstream backport task (Blocks link)
- **Description prefix**: Preemptive remediation note referencing TC-8020 (stream rhtpa-2.2)

### Key Differences from Standard (Case A) Tasks

| Attribute | Case A (rhtpa-2.2) | Case B Preemptive (rhtpa-2.1) |
|-----------|-------------------|-------------------------------|
| Labels | `["ai-generated-jira", "Security", "CVE-2026-55123"]` | `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]` |
| Link to CVE TC-8020 | "Depend" | "Related" |
| Description prefix | None | Preemptive remediation note citing TC-8020 and originating stream rhtpa-2.2 |
| Reconciliation | N/A | When PSIRT creates a CVE Jira for rhtpa-2.1, Step 4.4 will link it, convert to "Depend", and remove `security-preemptive` label |

### Preemptive Task Comment on TC-8020

The following comment would be posted to TC-8020 after preemptive task creation:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-task-key> (upstream backport, security-preemptive), <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---
