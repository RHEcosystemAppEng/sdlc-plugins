# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected, create remediation task

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected.
Ecosystem is RPM (system package) so a single remediation task is created.

## Remediation Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in X.509 certificate chain verification
affects openssl-libs versions before 3.0.7-28.el9_4. Versions 2.2.0, 2.2.1,
and 2.2.2 ship vulnerable versions of openssl-libs (3.0.7-25.el9_3 and
3.0.7-27.el9_4 respectively). The fix is available via RHSA-2026:4021.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE: https://www.cve.org/CVERecord?id=CVE-2026-40215
CVSS: 7.1 (High)

## Implementation Notes

- Update the openssl-libs package version in rpms.lock.yaml (or rpms.in.yaml) to >= 3.0.7-28.el9_4
- openssl-libs is an explicit install (present in rpms.lock.yaml), not inherited from the base image
- If using rpms.in.yaml as input, update the version spec there and regenerate rpms.lock.yaml
- Verify the Konflux build pipeline triggers successfully with the updated package

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
