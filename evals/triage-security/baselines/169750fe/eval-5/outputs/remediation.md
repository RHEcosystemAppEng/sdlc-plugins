# Step 8 -- Remediation Task Description

## Triage Outcome: Case B (Affected -- create remediation task)

Affected versions in the 2.2.x stream: 2.2.0, 2.2.1, 2.2.2
Not affected: 2.2.3, 2.2.4 (ship fixed version 3.0.7-28.el9_4)

Ecosystem: RPM (system package) -- **single task** per stream (no upstream+downstream split).
Package origin: explicit install (present in rpms.lock.yaml).

### Cross-Stream Impact (Case A notice)

The 2.1.x stream is also affected (2.1.0 and 2.1.1 ship openssl-libs 3.0.7-24.el9). A cross-stream impact comment would be posted to TC-8005 noting the 2.1.x stream impact. Preemptive remediation tasks for the 2.1.x stream would be created if no sibling CVE Jira exists for that stream.

---

## Remediation Task: Update openssl-libs in Konflux release repo (2.2.x)

**Jira creation parameters:**

- **Project**: TC
- **Issue type**: Task
- **Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)
- **Labels**: ai-generated-jira, Security, CVE-2026-40215
- **Link**: Depend (inward: TC-8005, outward: new task)

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability exists in openssl-libs versions before 3.0.7-28.el9_4 during X.509 certificate chain verification. A remote attacker can craft a certificate with a malformed Subject Alternative Name extension that triggers an out-of-bounds read, potentially leaking sensitive memory contents or causing a crash.

Affected product versions (2.2.x stream):
- 2.2.0 (build v0.4.5): openssl-libs 3.0.7-25.el9_3
- 2.2.1 (build v0.4.8): openssl-libs 3.0.7-27.el9_4
- 2.2.2 (build v0.4.9): retag of 2.2.1

Already fixed in:
- 2.2.3 (build v0.4.11): openssl-libs 3.0.7-28.el9_4
- 2.2.4 (build v0.4.12): openssl-libs 3.0.7-28.el9_4

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: **explicit install** (openssl-libs is present in rpms.lock.yaml)
- Update the openssl-libs package version in rpms.in.yaml or the package spec to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated package version
- Verify the Konflux build pipeline triggers successfully with the updated package
- Note: versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs 3.0.7-28.el9_4, confirming the fix is available in the RPM repository

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
