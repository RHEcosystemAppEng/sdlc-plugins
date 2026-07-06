# Step 8 -- Remediation

## Triage Outcome: Case A -- Affected (create remediation task)

Versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream ship a vulnerable openssl-libs. Remediation is required.

**Ecosystem**: RPM (system package) -- single task created (no upstream backport step).

**Package origin**: Explicit install (openssl-libs present in rpms.lock.yaml).

## Remediation Task Description

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-40215

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs during X.509 certificate chain
verification allows a remote attacker to craft a certificate with a malformed
Subject Alternative Name extension that triggers an out-of-bounds read, potentially
leaking sensitive memory contents or causing a crash.

Affected versions in the 2.2.x stream:
- 2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3
- 2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4
- 2.2.2 (v0.4.9): retag of 2.2.1

Fixed version: openssl-libs 3.0.7-28.el9_4 (available via RHSA-2026:4021)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version in rpms.in.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to pick up the updated package version
- The fix is available via Red Hat errata RHSA-2026:4021
- Verify no other RPM dependencies are broken by the openssl-libs update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Jira Issue Creation (proposed)

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

After task creation:
1. Post description digest comment per description-digest-protocol.md
2. Link the task to TC-8005 with type "Depend"
3. Transition TC-8005 to In Progress
4. Add ai-cve-triaged label to TC-8005
5. Post summary comment to TC-8005 with version impact table, Affects Versions correction, and link to the remediation task

## Cross-Stream Notice (Case B)

The 2.1.x stream is also affected (openssl-libs 3.0.7-24.el9 in both 2.1.0 and 2.1.1). A cross-stream impact comment would be posted to TC-8005. If no companion CVE Jira exists for the 2.1.x stream, a preemptive remediation task would be created with the `security-preemptive` label and linked via "Related" (not "Depend") to TC-8005.
