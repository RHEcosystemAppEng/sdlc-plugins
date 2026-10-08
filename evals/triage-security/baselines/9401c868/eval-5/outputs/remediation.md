# Step 8 -- Remediation

## Triage Outcome: Case B (Affected) with Case A (Cross-stream impact)

### Case A: Cross-stream impact

The version impact analysis reveals that the **2.1.x** stream (outside this issue's
scope) is also affected:

- 2.1.0 (v0.3.8): openssl-libs 3.0.7-24.el9 -- AFFECTED
- 2.1.1 (v0.3.12): openssl-libs 3.0.7-24.el9 -- AFFECTED

Cross-stream impact comment (to be posted on TC-8005):

> Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
> stream 2.1.x based on rpms.lock.yaml analysis. This stream is tracked by a
> companion issue (see Related links) or may require separate PSIRT triage.

If no companion CVE Jira exists for 2.1.x, a preemptive remediation task would be
created with the `security-preemptive` label and "Related" link to TC-8005.

---

### Case B: Remediation task for 2.2.x stream

**Ecosystem**: RPM (system package) -- **1 task** per stream.

Since openssl-libs is present in rpms.lock.yaml (explicit install origin), the
remediation updates the package spec in the Konflux release repo.

#### Remediation Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

The vulnerable package openssl-libs (versions before 3.0.7-28.el9_4) is subject
to a buffer over-read during X.509 certificate chain verification. A remote
attacker can craft a certificate with a malformed extension that triggers an
out-of-bounds read, potentially leaking sensitive memory contents or causing a crash.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215
CVSS: 7.1 (High)

## Implementation Notes

- Update the openssl-libs package version in rpms.in.yaml (or rpms.lock.yaml)
  to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml if using rpms.in.yaml as the source specification
- Verify the Konflux build pipeline triggers successfully with the updated package
- Note: versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship the fixed
  version 3.0.7-28.el9_4 -- no action needed for those versions

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

#### Jira Creation Call

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

#### Jira Linkage

```
# Link remediation task to CVE Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)

# Link remediation task to release Task (if active from Step 7.5)
jira.create_link(
  inwardIssue: <task-key>,
  outwardIssue: <release-task-key>,
  type: "Blocks"
)

# Link CVE to release Task (traceability)
jira.create_link(
  inwardIssue: <release-task-key>,
  outwardIssue: "TC-8005",
  type: "Related"
)
```

### Pre-creation checklist

- [x] **Task count per stream**: 1 task (RPM / system package ecosystem -- matches classification table)
- [x] **Cross-stream coverage**: 2.1.x stream is also affected -- Case A cross-stream notice posted; preemptive task created if no sibling CVE Jira exists
- [x] **Link types**: "Depend" for task linked to its own CVE Jira TC-8005; "Related" for any preemptive tasks linked to TC-8005 (cross-stream)
- [x] **Preemptive labels**: tasks for 2.1.x (if created) carry `security-preemptive` label
- [x] **Coordination guidance**: included (upstream deployment context)
- [x] **Release Jira linking**: remediation Task linked to release Task (Blocks), CVE linked to release Task (Related)
- [x] **Dedup consistency**: no dedup detected -- new remediation task created
