# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected (create remediation task)

Versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream ship a vulnerable openssl-libs (< 3.0.7-28.el9_4). The vulnerability was already fixed in versions 2.2.3 and 2.2.4.

## Cross-Stream Impact (Case B)

The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship openssl-libs 3.0.7-24.el9). A cross-stream impact comment would be posted to TC-8005:

> Cross-stream impact: openssl-libs < 3.0.7-28.el9_4 also affects stream 2.1.x based on rpms.lock.yaml analysis. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

## Ecosystem: RPM (System Package) -- Single Task

Since openssl-libs is an RPM system package found in `rpms.lock.yaml` (explicit install origin), a single remediation task is created in the Konflux release repo. No upstream backport task is needed.

## Remediation Task Description

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

Remediate CVE-2026-40215: update openssl-libs to include patched version.
The vulnerable package (openssl-libs < 3.0.7-28.el9_4) is present in rpms.lock.yaml
and must be updated to the fixed version (3.0.7-28.el9_4).

A buffer over-read in X.509 certificate chain verification allows a remote attacker
to craft a certificate with a malformed Subject Alternative Name extension that
triggers an out-of-bounds read, potentially leaking sensitive memory or causing a crash.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4), RHTPA 2.2.2 (retag of 2.2.1)
Already fixed in: RHTPA 2.2.3, RHTPA 2.2.4 (3.0.7-28.el9_4)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version in rpms.lock.yaml (or rpms.in.yaml) to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml if using an input file (rpms.in.yaml)
- Verify the Konflux build pipeline triggers successfully
- Note: versions 2.2.3+ already ship the fix -- this task covers backport to the 2.2.0-2.2.2 lineage

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent Vulnerability tracking issue)

---

## Jira Linkage (would execute after task creation)

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<new-task-key>",
  type: "Depend"
)
```

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8005
2. Transition TC-8005 to In Progress
3. Assign TC-8005 to current user
4. Post summary comment to TC-8005 documenting version impact table, Affects Versions correction, and remediation task link
