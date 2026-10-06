# Step 8 -- Remediation

## Triage Outcome: Case B (Affected -- create remediation task)

Versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream ship a vulnerable
openssl-libs version. Ecosystem classification: **RPM (system package)** --
create **1 task** (Konflux release repo fix).

**Note**: Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs
(3.0.7-28.el9_4). The fix was incorporated in build v0.4.11. The remediation
task documents the vulnerability for tracking and ensures no regression occurs.

## Cross-Stream Impact (Case A)

The 2.1.x stream is also affected (openssl-libs 3.0.7-24.el9 in both 2.1.0
and 2.1.1). A cross-stream impact comment would be posted to TC-8005:

> Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also
> affects stream 2.1.x based on rpms.lock.yaml analysis. This stream is
> tracked by a companion issue (see Related links) or may require separate
> PSIRT triage.

If no companion CVE Jira exists for the 2.1.x stream, a preemptive remediation
task with the `security-preemptive` label would be created for that stream.

---

## Remediation Task Description (2.2.x stream)

**Task type**: System package -- explicit install origin (RPM in rpms.lock.yaml)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <see below>,
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

A buffer over-read vulnerability was found in openssl-libs during X.509
certificate chain verification. Versions before 3.0.7-28.el9_4 are vulnerable.
A remote attacker can craft a certificate with a malformed extension that
triggers an out-of-bounds read, potentially leaking sensitive memory contents
or causing a crash. CVSS: 7.1 (High).

Affected versions in the 2.2.x stream:
- 2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3
- 2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4
- 2.2.2 (v0.4.9): openssl-libs 3.0.7-27.el9_4 (retag of 2.2.1)

Fixed in: 2.2.3+ (v0.4.11): openssl-libs 3.0.7-28.el9_4

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: **explicit install** (openssl-libs found in rpms.lock.yaml)
- Update the openssl-libs package version in rpms.in.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated package version
- The fix was already incorporated in build v0.4.11 (version 2.2.3). Verify
  that rpms.lock.yaml on the current branch HEAD reflects >= 3.0.7-28.el9_4
  to prevent regression.

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

### Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <new-task-key>,
  type: "Depend"
)
```
