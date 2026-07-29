# Step 8 -- Remediation

## Triage Outcome

The version impact analysis shows that supported versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2). This is **Case B** (affected -- create remediation tasks). Additionally, the 2.1.x stream is also affected, triggering **Case A** (cross-stream impact).

## Case A: Cross-Stream Impact

Cross-stream impact: openssl-libs versions before 3.0.7-28.el9_4 also affects stream 2.1.x based on rpms.lock.yaml analysis. Versions 2.1.0 and 2.1.1 both ship openssl-libs 3.0.7-24.el9 (vulnerable).

A search for sibling Vulnerability issues with the CVE-2026-40215 label and stream suffix `[rhtpa-2.1]` would determine whether a companion CVE Jira exists for the 2.1.x stream. If no sibling exists, a preemptive remediation task would be created for 2.1.x with the `security-preemptive` label and "Related" link type to TC-8005.

## Case B: Remediation Task for 2.2.x Stream

Since openssl-libs is an RPM system package (explicit install via rpms.lock.yaml), **one** remediation task is created for the 2.2.x stream.

### Remediation Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

The vulnerable package (openssl-libs, versions before 3.0.7-28.el9_4) must be
updated to the fixed version (3.0.7-28.el9_4) in the Konflux release repo.

A buffer over-read vulnerability exists in X.509 certificate chain verification.
A remote attacker can craft a certificate with a malformed extension that triggers
an out-of-bounds read, potentially leaking sensitive memory contents or causing a crash.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1/2.2.2)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install (present in rpms.lock.yaml)
- Update the openssl-libs package version in rpms.in.yaml / rpms.lock.yaml
  to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml if the project uses a lock file generation workflow
- Verify the Konflux build pipeline triggers successfully after the update
- Note: versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship
  openssl-libs 3.0.7-28.el9_4 and are not affected

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

### Jira Creation Call

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```

## Pre-Creation Checklist

- [x] **Task count per stream**: 1 task for 2.2.x (RPM system package ecosystem = 1 task)
- [x] **Cross-stream coverage**: 2.1.x stream is also affected; would check for sibling CVE Jira with `[rhtpa-2.1]` suffix. If none exists, create a preemptive task with `security-preemptive` label.
- [x] **Link types**: "Depend" for the task linked to TC-8005; "Related" for any preemptive tasks linked to TC-8005 (cross-stream)
- [x] **Preemptive labels**: any tasks created for 2.1.x (if no sibling CVE exists) would carry `security-preemptive`
- [x] **Coordination guidance**: Deployment Context column is absent from Source Repositories table; coordination guidance subsection is omitted
