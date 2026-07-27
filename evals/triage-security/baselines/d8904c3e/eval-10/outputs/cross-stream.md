# Cross-Stream Impact — CVE-2026-55123 (TC-8020)

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020:

---

Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.

| Stream    | Versions Affected         | tokio version | Fix Threshold | Sibling CVE Jira |
|-----------|---------------------------|---------------|---------------|------------------|
| rhtpa-2.1 | RHTPA 2.1.0, RHTPA 2.1.1 | 1.40.0        | 1.42.0        | None found       |
| rhtpa-2.2 | RHTPA 2.2.0, RHTPA 2.2.1 | 1.41.1        | 1.42.0        | TC-8020 (this issue) |

Stream rhtpa-2.1 has no companion CVE Jira and may require separate PSIRT triage.

---

## Sibling CVE Jira Search Results

JQL query executed:
```
project = TC AND issuetype = 10024 AND labels = "CVE-2026-55123" AND summary ~ "[rhtpa-2.1]"
```

**Result**: No issues found. No sibling CVE Jira exists for stream rhtpa-2.1.

## Preemptive Task Creation (Case A)

Since stream rhtpa-2.1 is affected but has no CVE Jira, preemptive remediation tasks
are created using the `security-preemptive` variant:

### Preemptive Tasks Created for Stream rhtpa-2.1

| Task | Type | Summary | Labels | Link to TC-8020 |
|------|------|---------|--------|-----------------|
| (upstream) | Upstream Backport | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive` | Related |
| (downstream) | Downstream Propagation | Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive` | Related |

### Preemptive Task Details

**Upstream Backport (rhtpa-2.1)**:
- Repository: rhtpa-backend
- Target branch: release/0.3.z
- Fix: bump tokio to >= 1.42.0
- Affected versions: RHTPA 2.1.0 (v0.3.8, tokio 1.40.0), RHTPA 2.1.1 (v0.3.12, tokio 1.40.0)
- Description includes preemptive remediation prefix noting originating CVE TC-8020 from stream rhtpa-2.2
- Link type: Related (not Depend) to TC-8020

**Downstream Propagation (rhtpa-2.1)**:
- Repository: rhtpa-release.0.3.z
- Target branch: main
- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- Blocked by: preemptive upstream backport task
- Description includes preemptive remediation prefix noting originating CVE TC-8020 from stream rhtpa-2.2
- Link type: Related (not Depend) to TC-8020
- Labels include `security-preemptive`

### Key Differences from Standard Remediation Tasks

| Aspect | Standard (Case B) | Preemptive (Case A) |
|--------|-------------------|---------------------|
| Labels | `ai-generated-jira`, `Security`, `CVE-2026-55123` | `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive` |
| Link type to CVE Jira | Depend | Related |
| Description prefix | None | Preemptive remediation note referencing originating CVE and stream |
| Reconciliation | N/A | When PSIRT creates stream-specific CVE Jira, Step 4.4 links and removes `security-preemptive` label |

## Preemptive Task Comment on TC-8020

The following comment would be posted to TC-8020 after preemptive task creation:

---

Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: upstream backport task (security-preemptive) + downstream propagation task (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---
