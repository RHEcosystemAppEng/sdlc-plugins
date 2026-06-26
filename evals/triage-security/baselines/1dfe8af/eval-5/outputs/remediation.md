# Step 7 -- Remediation Task Description

Ecosystem: RPM (system package, explicit install) -- single task for Konflux release repo.

## Jira Task Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

## Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

## Implementation Notes

- Update the openssl-libs package version in rpms.lock.yaml (or rpms.in.yaml) to >= 3.0.7-28.el9_4
- If lock file exists: regenerate rpms.lock.yaml
- Advisory: https://access.redhat.com/errata/RHSA-2026:4021

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
