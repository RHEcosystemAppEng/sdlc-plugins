# Step 8 -- Remediation Task Description

## Triage Outcome

Case A (Affected) with Case B (Cross-stream impact on 2.1.x).

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). The ecosystem is
RPM (system package), so a **single** remediation task is created -- no upstream
backport task is needed because RPM packages are updated directly in the Konflux
release repo.

## Remediation Task

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-40215

**Link**: Depend -- TC-8005 (parent Vulnerability issue)

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability exists in openssl-libs versions before
3.0.7-28.el9_4 during X.509 certificate chain verification. A remote attacker
can craft a certificate with a malformed Subject Alternative Name extension to
trigger an out-of-bounds read.

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Fixed in versions: RHTPA 2.2.3+ already ship openssl-libs 3.0.7-28.el9_4

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version spec to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to pin the updated version
- The package is an explicit install in rpms.lock.yaml (not inherited from base image)
- CVSS: 7.1 (High) -- due date 2026-08-15

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
