# Step 8 -- Remediation Task

## Triage Outcome

**Case A**: affected versions exist in the scoped 2.2.x stream (2.2.0, 2.2.1,
2.2.2). Remediation task required.

**Case B**: cross-stream impact detected. The 2.1.x stream (2.1.0, 2.1.1) is
also affected. A cross-stream impact comment would be posted to TC-8005. Since
no sibling CVE Jira exists for the 2.1.x stream, a preemptive remediation task
would be created for that stream with the `security-preemptive` label.

## Remediation Task Description (2.2.x stream -- single RPM task)

Ecosystem: RPM (system package). Single task targeting the Konflux release repo.
Origin: explicit install (openssl-libs present in rpms.lock.yaml).

---

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-40215

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs affects X.509 certificate
chain verification. Versions before 3.0.7-28.el9_4 are vulnerable to an
out-of-bounds read via a malformed Subject Alternative Name extension,
potentially leaking sensitive memory contents or causing a crash (CVSS 7.1).

Affected versions in the 2.2.x stream:
- 2.2.0 (build 0.4.5): openssl-libs 3.0.7-25.el9_3
- 2.2.1 (build 0.4.8): openssl-libs 3.0.7-27.el9_4
- 2.2.2 (build 0.4.9): openssl-libs 3.0.7-27.el9_4 (retag of 2.2.1)

Already fixed in:
- 2.2.3 (build 0.4.11): openssl-libs 3.0.7-28.el9_4
- 2.2.4 (build 0.4.12): openssl-libs 3.0.7-28.el9_4

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install (openssl-libs present in rpms.lock.yaml)
- The fix (3.0.7-28.el9_4) is already present in builds 0.4.11+ (versions 2.2.3+)
- For affected builds (0.4.5 through 0.4.9): if a z-stream respin is required
  for versions 2.2.0-2.2.2, regenerate rpms.lock.yaml to pick up
  openssl-libs >= 3.0.7-28.el9_4
- If lock file exists: regenerate rpms.lock.yaml
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

---

## Jira API Call

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <system-package-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

## Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```
