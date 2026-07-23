# Step 8 -- Remediation

## Triage Outcome

**Case A: Affected -- create remediation task**

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship a vulnerable version of openssl-libs (< 3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 already ship the fixed version.

Since this is an RPM (system package) ecosystem, a single remediation task is created for the Konflux release repo. No upstream backport task is needed.

## Cross-Stream Impact (Case B)

The 2.1.x stream is also affected (openssl-libs 3.0.7-24.el9 in both 2.1.0 and 2.1.1). Since this issue is scoped to 2.2.x, a cross-stream impact comment would be posted:

> Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also
> affects stream 2.1.x based on rpms.lock.yaml analysis. This stream is tracked
> by companion issues (see Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for the 2.1.x stream, a preemptive remediation task would be created with the `security-preemptive` label.

## Remediation Task Description (2.2.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <see-below>,
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
certificate chain verification. Versions of openssl-libs before 3.0.7-28.el9_4
are vulnerable. A remote attacker can craft a certificate with a malformed
Subject Alternative Name extension that triggers an out-of-bounds read,
potentially leaking sensitive memory contents or causing a crash. CVSS: 7.1 (High).

Affected versions in the 2.2.x stream:
- 2.2.0 (build 0.4.5): openssl-libs 3.0.7-25.el9_3
- 2.2.1 (build 0.4.8): openssl-libs 3.0.7-27.el9_4
- 2.2.2 (build 0.4.9): openssl-libs 3.0.7-27.el9_4 (retag of 2.2.1)

Already fixed in:
- 2.2.3 (build 0.4.11): openssl-libs 3.0.7-28.el9_4
- 2.2.4 (build 0.4.12): openssl-libs 3.0.7-28.el9_4

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- The openssl-libs package is an explicit install (present in rpms.lock.yaml)
- Update the package version spec in rpms.in.yaml or rpms.lock.yaml to
  >= 3.0.7-28.el9_4
- If lock file exists: regenerate rpms.lock.yaml to pick up the fixed version
- Note: versions 2.2.3+ already ship the fixed version; this task ensures
  the fix is tracked and any rebuild of older release branches picks up the
  patched package

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Depends on: TC-8005 (parent Vulnerability tracking issue)

---

## Jira Linkage

After task creation:

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<remediation-task-key>",
  type: "Depend"
)
```

## Post-Triage Summary

After all triage actions are complete:
1. Add `ai-cve-triaged` label to TC-8005
2. Post summary comment with version impact table, Affects Versions correction,
   and links to remediation tasks
3. @mention the issue reporter (PSIRT analyst)
