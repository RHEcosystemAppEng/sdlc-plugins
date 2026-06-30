# Step 7 -- Remediation for TC-8005

## Triage Outcome: Case A (Affected) + Case B (Cross-Stream Impact)

### Case A -- Affected versions in scoped stream (2.2.x)

Versions 2.2.0, 2.2.1, and 2.2.2 ship openssl-libs below the fix threshold. Versions 2.2.3 and 2.2.4 already ship the fixed version (3.0.7-28.el9_4). Since the ecosystem is RPM (system package) with the package present in rpms.lock.yaml (explicit install origin), one remediation task is created for the 2.2.x stream.

### Case B -- Cross-stream impact (2.1.x)

The version impact analysis shows that the 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship openssl-libs 3.0.7-24.el9). A cross-stream impact comment would be posted. If no sibling CVE Jira exists for 2.1.x, a preemptive remediation task (with `security-preemptive` label) would be created for that stream.

---

## Remediation Task: 2.2.x Stream (RPM Explicit Install)

### Proposed Jira Issue

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs (versions before 3.0.7-28.el9_4)
affects X.509 certificate chain verification. A remote attacker can craft a
certificate with a malformed extension that triggers an out-of-bounds read.

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Fixed in versions: RHTPA 2.2.3+ (already ship 3.0.7-28.el9_4)
Advisory: https://access.redhat.com/errata/RHSA-2026:4021

## Implementation Notes

- Update openssl-libs package version to >= 3.0.7-28.el9_4 in rpms.in.yaml
- Regenerate rpms.lock.yaml to reflect the updated package version
- The patched package is available via RHSA-2026:4021
- Verify no other packages have conflicting dependencies on the older openssl-libs version

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

### Proposed Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<new-task-key>",
  type: "Depend"
)
```

### Proposed Transition

```
Transition TC-8005 to "In Progress"
Assign TC-8005 to current user
Add label "ai-cve-triaged" to TC-8005
```

---

## Preemptive Remediation Task: 2.1.x Stream (if no sibling CVE Jira exists)

If the Step 4 sibling search finds no CVE Jira for CVE-2026-40215 scoped to the 2.1.x stream, a preemptive task would be created:

### Proposed Jira Issue

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.1.x)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215", "security-preemptive"]
)
```

### Preemptive Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8005 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs (versions before 3.0.7-28.el9_4)
affects X.509 certificate chain verification.

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Advisory: https://access.redhat.com/errata/RHSA-2026:4021

## Implementation Notes

- Update openssl-libs package version to >= 3.0.7-28.el9_4 in rpms.in.yaml
- Regenerate rpms.lock.yaml to reflect the updated package version
- The patched package is available via RHSA-2026:4021

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

### Proposed Linkage (Preemptive)

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<preemptive-task-key>",
  type: "Related"
)
```

Note: Preemptive tasks use "Related" link type (not "Depend") because the originating CVE belongs to a different stream.

---

## Post-Triage Summary Comment (proposed for TC-8005)

```
Triage complete for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4).

Version impact (2.2.x stream):
| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0   | 3.0.7-25.el9_3 | YES    |       |
| 2.2.1   | 3.0.7-27.el9_4 | YES    |       |
| 2.2.2   | --             | YES    | retag of 2.2.1 |
| 2.2.3   | 3.0.7-28.el9_4 | NO     | at fix version |
| 2.2.4   | 3.0.7-28.el9_4 | NO     | at fix version |

Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Remediation task created: <task-key> (update openssl-libs in rhtpa-release.0.4.z)

Cross-stream impact: openssl-libs < 3.0.7-28.el9_4 also affects stream 2.1.x
(2.1.0: 3.0.7-24.el9, 2.1.1: 3.0.7-24.el9).

@<reporter-name> (reporter mention via ADF)
```
