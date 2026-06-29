# Step 7 — Remediation Task

## Task Summary

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)

## Task Description

### Repository

rhtpa-release.0.4.z

### Target Branch

main

### Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs (versions before 3.0.7-28.el9_4) affects the X.509 certificate verification code path. The openssl-libs package is an explicit install in rpms.lock.yaml and must be updated to the fixed version.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Advisory: https://access.redhat.com/errata/RHSA-2026:4021

### Implementation Notes

- Update the openssl-libs package version in rpms.in.yaml (or equivalent package spec) to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated package version
- openssl-libs is an explicit install (present in rpms.lock.yaml), not a base image dependency
- Verify no other packages have version conflicts with the updated openssl-libs

### Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] rpms.lock.yaml updated with the new package version
- [ ] Konflux rebuild triggers new container image
