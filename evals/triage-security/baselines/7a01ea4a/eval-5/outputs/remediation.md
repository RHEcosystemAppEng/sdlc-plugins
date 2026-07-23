# Step 8 -- Remediation: TC-8005

## Triage Outcome: Case A -- Affected, create remediation task

Affected versions in the scoped 2.2.x stream: 2.2.0, 2.2.1, 2.2.2.
Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs 3.0.7-28.el9_4.

### Cross-stream impact (Case B)

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship openssl-libs 3.0.7-24.el9). Since this issue is scoped to 2.2.x, a cross-stream impact comment would be posted and preemptive remediation tasks created for the 2.1.x stream if no companion CVE Jira exists for that stream.

## Remediation Task -- 2.2.x stream (RPM, explicit install)

**Ecosystem**: RPM (system package) -- single task, no upstream backport needed.

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to include the fix for a buffer over-read in X.509 certificate verification.

The vulnerable package (openssl-libs, versions before 3.0.7-28.el9_4) is an explicit install in rpms.lock.yaml. The fixed version 3.0.7-28.el9_4 is available per RHSA-2026:4021.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4), RHTPA 2.2.2 (retag of 2.2.1)
Already fixed in: RHTPA 2.2.3 and RHTPA 2.2.4 (ship 3.0.7-28.el9_4)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install (openssl-libs found in rpms.lock.yaml)
- SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml classification only.
- Update the openssl-libs package spec in rpms.in.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to pick up the updated version
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<remediation-task-key>",
  type: "Depend"
)
```

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8005
2. Post summary comment to TC-8005 with version impact table, Affects Versions correction, remediation task link, and @mention of the reporter
3. Transition TC-8005 to In Progress
