# Step 8 -- Remediation Task Description: TC-8005

## Triage Outcome

**Case B: Affected -- create remediation task** (system package / RPM ecosystem, 1 task).

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship a vulnerable version
of openssl-libs (before 3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 already ship the
fixed version. The remediation task targets the Konflux release repo to update the
openssl-libs package spec for any future builds from affected base configurations.

## Remediation Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x).

The vulnerable package openssl-libs (versions before 3.0.7-28.el9_4) is subject to
a buffer over-read in X.509 certificate chain verification (CVSS 7.1 High). A remote
attacker can craft a certificate with a malformed Subject Alternative Name extension
that triggers an out-of-bounds read, potentially leaking memory contents or causing
a crash.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4),
RHTPA 2.2.2 (retag of 2.2.1).
Fixed in: RHTPA 2.2.3+ (openssl-libs 3.0.7-28.el9_4, build tag v0.4.11+).

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- **Package origin**: explicit install (openssl-libs is present in rpms.lock.yaml)
- **SBOM verification**: skipped -- cosign not available. Using rpms.lock.yaml
  classification only.
- **Current state**: the fix (3.0.7-28.el9_4) is already present in build tags
  v0.4.11 and v0.4.12 (product versions 2.2.3 and 2.2.4). Verify that the
  rpms.lock.yaml and rpms.in.yaml pin openssl-libs to >= 3.0.7-28.el9_4 so that
  future rebuilds do not regress.
- Update the package version spec in rpms.in.yaml to require >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to lock the updated version
- Verify the Konflux build pipeline triggers successfully with the updated spec

### Dependency chain

  rpms.lock.yaml: PRESENT -> explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml / rpms.in.yaml)

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] rpms.in.yaml spec prevents regression below 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated package spec

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

## Jira Issue Creation (would be executed)

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

## Jira Linkage (would be executed)

1. Link remediation task to CVE Vulnerability issue (Depend):
   ```
   jira.create_link(
     inwardIssue: "TC-8005",
     outwardIssue: <task-key>,
     type: "Depend"
   )
   ```

2. If release Jira orchestration is active (Step 7.5), link remediation task to
   release Task (Blocks) and CVE to release Task (Related).

## Cross-Stream Impact (Case A)

The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship openssl-libs
3.0.7-24.el9, which is before the fix version). A cross-stream impact comment
would be posted to TC-8005:

> Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
> stream 2.1.x based on rpms.lock.yaml analysis. This stream is tracked by a
> companion issue (see Related links) or may require separate PSIRT triage.

If no companion CVE Jira exists for the 2.1.x stream, a preemptive remediation
task would be created with the `security-preemptive` label and linked to TC-8005
with "Related" (not "Depend").
