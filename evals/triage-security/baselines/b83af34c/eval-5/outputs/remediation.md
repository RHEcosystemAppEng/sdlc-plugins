# Step 8 - Remediation Task for TC-8005

## Triage Outcome

Case B: Affected -- versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship
vulnerable openssl-libs. Create remediation task.

Ecosystem: RPM (system package) -- single task for the Konflux release repo.
No upstream backport + downstream propagation flow.

---

## Remediation Task Description

The following task description follows `task-description-template.md` format and
would be created as a Jira Task.

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)
**Labels**: ai-generated-jira, Security, CVE-2026-40215
**Issue Type**: Task

### Task Description Body

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

The vulnerable RPM package openssl-libs (versions before 3.0.7-28.el9_4) is present
in rpms.lock.yaml for versions 2.2.0, 2.2.1, and 2.2.2 of the 2.2.x stream.
A buffer over-read in X.509 certificate chain verification allows remote attackers
to craft certificates that trigger out-of-bounds reads.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021

## Implementation Notes

- Package origin: explicit install (present in rpms.lock.yaml)
- Update the package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml after updating rpms.in.yaml
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Jira API Call (simulated)

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <system-package-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)

jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```

**Note**: This is a single task for the Konflux release repo (system package
ecosystem). The two-task upstream backport + downstream propagation flow is NOT
used for RPM system packages -- that flow applies only to source dependency
ecosystems (Cargo, npm).
