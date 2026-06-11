# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected (create remediation task)

The version impact analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected by CVE-2026-40215. Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs 3.0.7-28.el9_4.

Since this is an RPM ecosystem vulnerability and the fix is already available in the 2.2.x stream (starting from 2.2.3), the affected versions (2.2.0-2.2.2) are older releases that already shipped. However, if there is a need to produce respins of those versions, a remediation task should be created in the Konflux release repo.

### Ecosystem: RPM (system package -- single task)

Since openssl-libs is present in `rpms.lock.yaml`, the package origin is **explicit install**. Remediation is a single Konflux release repo task (no upstream backport needed).

### Cross-Stream Impact Notice (Case B)

The version impact analysis also reveals that the **2.1.x stream** (versions 2.1.0, 2.1.1) is affected. This is outside the current issue's scope. A comment would be posted to TC-8005:

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
stream 2.1.x based on rpms.lock.yaml analysis.
This stream is tracked by a companion issue (see Related links) or may require
separate PSIRT triage.
```

---

## Remediation Task Description

The following task would be created in Jira as an RPM system package remediation task.

### Proposed Jira Issue Creation

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

A buffer over-read vulnerability was found in openssl-libs during X.509 certificate
chain verification. Versions before 3.0.7-28.el9_4 are vulnerable to an out-of-bounds
read via a crafted certificate with a malformed Subject Alternative Name extension.
CVSS: 7.1 (High).

Affected product versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Fixed in: openssl-libs-3.0.7-28.el9_4 (RHSA-2026:4021)

Note: Versions 2.2.3+ already ship the fixed version. This task ensures the lock
file is updated so any future respins of affected builds use the patched package.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version in rpms.lock.yaml (or rpms.in.yaml)
  to >= 3.0.7-28.el9_4
- If rpms.in.yaml is used as input, regenerate rpms.lock.yaml after the update
- Verify the Konflux build pipeline triggers successfully
- The fix is available via RHSA-2026:4021 in RHEL 9.4 repositories

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

### Proposed Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<new-task-key>",
  type: "Depend"
)
```

### Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8005
2. **Transition** TC-8005 to In Progress
3. **Assign** TC-8005 to current user
4. **Post summary comment** to TC-8005 documenting the triage outcome

All proposed Jira mutations require explicit engineer confirmation before execution.
