# Step 7 - Remediation: TC-8005

## Triage Outcome: Case A - Affected (create remediation task)

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2) that ship openssl-libs before the fixed version 3.0.7-28.el9_4. Since openssl-libs is an RPM system package (not a source dependency), a single remediation task is created for the Konflux release repo.

Note: versions 2.2.3 and 2.2.4 already ship the fixed version, so they do not require remediation. The fix was already picked up in build v0.4.11 (2.2.3). However, the earlier affected versions (2.2.0, 2.2.1, 2.2.2) remain in the Affects Versions to document the historical impact.

## Cross-Stream Impact Notice (Case B)

The 2.1.x stream is also affected (openssl-libs 3.0.7-24.el9 in both 2.1.0 and 2.1.1). A comment would be posted to TC-8005:

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
stream 2.1.x based on rpms.lock.yaml analysis. This stream is tracked by a
companion issue (see Related links) or may require separate PSIRT triage.
```

## Remediation Task (System Package - RPM)

Since the fix is already present in versions 2.2.3+ (openssl-libs 3.0.7-28.el9_4), and the affected versions 2.2.0-2.2.2 are already-shipped releases, the remediation task documents what was done and ensures no regression occurs.

### Jira Issue Creation

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

A buffer over-read vulnerability was found in openssl-libs. Versions before
3.0.7-28.el9_4 are vulnerable to a buffer over-read during X.509 certificate
chain verification. A remote attacker can craft a certificate with a malformed
extension that triggers an out-of-bounds read, potentially leaking sensitive
memory contents or causing a crash. CVSS: 7.1 (High).

Affected product versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8),
RHTPA 2.2.2 (v0.4.9, retag of 2.2.1).

Note: Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship
openssl-libs 3.0.7-28.el9_4 and are not affected.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

RPM origin: explicit install (present in rpms.lock.yaml).

## Implementation Notes

- The openssl-libs package is pinned via rpms.lock.yaml in the Konflux
  release repo (rhtpa-release.0.4.z)
- Update the openssl-libs entry in rpms.lock.yaml (or rpms.in.yaml) to
  >= 3.0.7-28.el9_4
- If lock file is generated: update rpms.in.yaml and regenerate
  rpms.lock.yaml
- Verify the updated package version resolves correctly from the
  configured RPM repositories
- Note: builds v0.4.11+ already include the fix; this task ensures
  the fix is documented and no regression occurs in future builds

## Acceptance Criteria

- [ ] openssl-libs dependency is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] No other RPM dependency conflicts introduced
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated dependency

## Dependencies

- Depends on: TC-8005 (parent Vulnerability tracking issue)
```

### Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<task-key>",
  type: "Depend"
)
```

### Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8005
2. Transition TC-8005 to In Progress
3. Assign TC-8005 to current user
4. Post summary comment to TC-8005 documenting the triage outcome
