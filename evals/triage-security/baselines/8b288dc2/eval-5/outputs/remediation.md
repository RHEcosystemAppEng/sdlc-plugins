# Step 8 -- Remediation Task for TC-8005

## Triage Outcome: Case A (Affected -- create remediation task)

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship a vulnerable openssl-libs version. A single remediation task is required (RPM system package ecosystem -- single-task flow, no upstream backport needed).

Cross-stream impact (Case B): The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 ship openssl-libs 3.0.7-24.el9). A cross-stream impact comment would be posted to TC-8005. If no companion CVE Jira exists for the 2.1.x stream, a preemptive remediation task would be created with the `security-preemptive` label.

---

## Remediation Task Description (System Package -- Explicit Install Origin)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
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

A buffer over-read vulnerability was found in openssl-libs in the X509_verify_cert() code path. Versions before 3.0.7-28.el9_4 are vulnerable. The fix is available via RHSA-2026:4021.

Affected versions: RHTPA 2.2.0 (openssl-libs 3.0.7-25.el9_3), RHTPA 2.2.1 (openssl-libs 3.0.7-27.el9_4), RHTPA 2.2.2 (retag of 2.2.1)
Source tags: v0.4.5, v0.4.8, v0.4.9

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

Package origin: explicit install (openssl-libs present in rpms.lock.yaml).

## Implementation Notes

- Update the openssl-libs package version in rpms.in.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated package version
- Verify the Konflux build pipeline triggers successfully with the updated package

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] rpms.lock.yaml regenerated with updated package version
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Jira Linkage

After task creation:

1. Link the remediation task to TC-8005:
   ```
   jira.create_link(
     inwardIssue: "TC-8005",
     outwardIssue: <task-key>,
     type: "Depend"
   )
   ```

2. Transition TC-8005 to In Progress.

3. Assign TC-8005 to the current user.

4. Post comment to TC-8005 listing the created task:
   "Remediation task created: <task-key>"
