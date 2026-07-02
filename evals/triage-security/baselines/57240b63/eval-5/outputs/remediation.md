# Step 8 -- Remediation: TC-8005

## Triage Outcome: Case A -- Affected (create remediation task)

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship a vulnerable version of openssl-libs. A single remediation task is required (RPM ecosystem -- Konflux release repo fix only, no upstream backport needed).

### Cross-Stream Impact (Case B)

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 ship openssl-libs 3.0.7-24.el9). A cross-stream impact comment would be posted to TC-8005. If no companion CVE Jira exists for the 2.1.x stream, a preemptive remediation task would be created with the `security-preemptive` label and "Related" link type.

---

## PROPOSAL: Remediation Task (2.2.x stream)

### Jira Issue Creation

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <task-description-below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability was found in openssl-libs during X.509 certificate chain verification. Versions before 3.0.7-28.el9_4 are vulnerable. A remote attacker can craft a certificate with a malformed Subject Alternative Name extension that triggers an out-of-bounds read, potentially leaking sensitive memory contents or causing a crash.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4), RHTPA 2.2.2 (retag of 2.2.1)
Source commits: v0.4.5, v0.4.8, v0.4.9

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

Package origin: explicit install (openssl-libs found in rpms.lock.yaml)

## Implementation Notes

- Update the openssl-libs package version specification to >= 3.0.7-28.el9_4 in rpms.in.yaml (or equivalent package spec)
- Regenerate rpms.lock.yaml to pick up the updated version
- Verify the RHSA-2026:4021 advisory confirms 3.0.7-28.el9_4 is available in the configured RPM repositories
- Verify the Konflux build pipeline triggers successfully after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] rpms.lock.yaml regenerated with updated package version
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

### PROPOSAL: Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<remediation-task-key>",
  type: "Depend"
)
```

### PROPOSAL: Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8005
2. Post summary comment to TC-8005 with version impact table, Affects Versions correction, remediation task link, and @mention of reporter
3. Post description digest comment to the remediation task (before links or other comments)
4. Transition TC-8005 to In Progress

### PROPOSAL: Cross-Stream Impact Comment on TC-8005

```
Cross-stream impact: openssl-libs versions before 3.0.7-28.el9_4 also affects
stream 2.1.x based on rpms.lock.yaml analysis.
- 2.1.0 (v0.3.8): openssl-libs 3.0.7-24.el9 -- affected
- 2.1.1 (v0.3.12): openssl-libs 3.0.7-24.el9 -- affected

This stream is tracked by a companion issue (see Related links)
or may require separate PSIRT triage.
```
