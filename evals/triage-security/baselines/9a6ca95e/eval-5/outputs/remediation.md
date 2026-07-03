# Step 8 -- Remediation

## Triage Outcome: Case A (Affected) with Case B (Cross-stream impact)

### Case A -- In-scope stream (2.2.x) is affected

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship a vulnerable openssl-libs (before 3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 already ship the fixed version.

Since the fix already landed in 2.2.3 (tag v0.4.11), no new remediation task is needed for the 2.2.x stream -- the vulnerability is already resolved in the latest releases. However, the Affects Versions correction (Step 3) ensures proper tracking of which versions were affected.

**Decision**: No new remediation task is required for the 2.2.x stream because the latest releases (2.2.3, 2.2.4) already include the fix. The affected versions (2.2.0, 2.2.1, 2.2.2) are historical releases.

### Case B -- Cross-stream impact (2.1.x)

The version impact analysis shows that the **2.1.x** stream is also affected:

| Version | openssl-libs | Affected? |
|---------|--------------|-----------|
| 2.1.0 | 3.0.7-24.el9 | YES |
| 2.1.1 | 3.0.7-24.el9 | YES |

All versions in the 2.1.x stream ship openssl-libs 3.0.7-24.el9, which is within the affected range. A cross-stream impact comment would be posted to TC-8005, and a search for existing CVE Jiras with stream suffix `[rhtpa-2.1]` would be performed. If no companion CVE Jira exists for the 2.1.x stream, a preemptive remediation task would be created.

## Remediation Task Description (for 2.1.x preemptive task, if no companion CVE Jira exists)

Since openssl-libs is an RPM system package present in rpms.lock.yaml (explicit install), this uses the **system package -- explicit install** template with the **preemptive variant**.

---

### Task: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-40215, security-preemptive
**Link type**: Related (to TC-8005, the originating CVE Jira from a different stream)

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8005 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability exists in openssl-libs versions before 3.0.7-28.el9_4
during X.509 certificate chain verification. A remote attacker can craft a certificate
with a malformed extension that triggers an out-of-bounds read, potentially leaking
sensitive memory contents or causing a crash.

Affected versions in stream 2.1.x:
- 2.1.0 (tag v0.3.8): openssl-libs 3.0.7-24.el9
- 2.1.1 (tag v0.3.12): openssl-libs 3.0.7-24.el9

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update openssl-libs package version to >= 3.0.7-28.el9_4 in rpms.lock.yaml
  (and rpms.in.yaml if applicable)
- The patched package is available via RHSA-2026:4021
- Regenerate the lock file after updating the package spec
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue, cross-stream)
