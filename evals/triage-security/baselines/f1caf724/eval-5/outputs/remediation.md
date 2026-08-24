# Step 8 -- Remediation

## Case Assessment

**Case B applies**: versions 2.2.0, 2.2.1, and 2.2.2 within the issue's 2.2.x
stream scope are affected. Ecosystem is RPM (system package) so **1 remediation
task** is created for the stream.

**Case A also applies** (cross-stream impact): the 2.1.x stream is also
affected (both 2.1.0 and 2.1.1 ship openssl-libs < 3.0.7-28.el9_4). A
cross-stream impact comment would be posted on TC-8005 noting the 2.1.x impact.
The 2.1.x stream is tracked by a companion issue or requires separate PSIRT triage.
No remediation tasks are created for 2.1.x from this scoped issue.

**Note**: the fix (openssl-libs 3.0.7-28.el9_4) was already incorporated in
build 0.4.11 (version 2.2.3). Versions 2.2.3 and 2.2.4 are not affected. The
remediation task documents this context for tracking purposes.

## Remediation Task Description (RPM System Package -- Explicit Install)

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-40215`

---

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to >= 3.0.7-28.el9_4 in the
Konflux release repo for the 2.2.x stream.

openssl-libs versions before 3.0.7-28.el9_4 are vulnerable to a buffer
over-read during X.509 certificate chain verification (CVSS 7.1 High). A
remote attacker can craft a certificate with a malformed Subject Alternative
Name extension that triggers an out-of-bounds read, potentially leaking
sensitive memory contents or causing a crash.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Already fixed in: RHTPA 2.2.3 (build 0.4.11), RHTPA 2.2.4 (build 0.4.12)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: **explicit install** (openssl-libs present in rpms.lock.yaml)
- The fix (3.0.7-28.el9_4) was already incorporated starting with build
  0.4.11 (version 2.2.3). Verify that the current rpms.lock.yaml on the
  main branch specifies openssl-libs >= 3.0.7-28.el9_4.
- If the lock file already contains the fixed version: no code change is
  required. Confirm the fix and close the remediation task.
- If for any reason the lock file has regressed: update the package spec
  in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4 and trigger a
  Konflux rebuild.
- SBOM verification was skipped (cosign not available). When cosign becomes
  available, verify the final container image SBOM confirms the patched
  openssl-libs version.

## Acceptance Criteria

- [ ] openssl-libs in rpms.lock.yaml is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild (if needed) triggers new container image
- [ ] No regression in openssl-libs version in subsequent builds

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent Vulnerability tracking issue)

---

## Jira Creation (would execute after engineer confirmation)

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)

jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```

## Cross-Stream Impact Comment (Case A)

The following comment would be posted on TC-8005:

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also
affects stream 2.1.x based on rpms.lock.yaml analysis.

2.1.x impact:
- 2.1.0 (v0.3.8): openssl-libs 3.0.7-24.el9 -- AFFECTED
- 2.1.1 (v0.3.12): openssl-libs 3.0.7-24.el9 -- AFFECTED

The 2.1.x stream is tracked by a companion issue (see Related links)
or may require separate PSIRT triage.
```
