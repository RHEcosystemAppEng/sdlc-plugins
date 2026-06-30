# Step 7 -- Remediation Analysis for TC-8005

## Triage Outcome

**No new remediation task required for the 2.2.x stream.**

The version impact analysis shows that the vulnerability (CVE-2026-40215, openssl-libs
< 3.0.7-28.el9_4) was already fixed starting in version 2.2.3 (build v0.4.11, released
2026-03-23). The latest release (2.2.4) also ships the fixed openssl-libs 3.0.7-28.el9_4.

While versions 2.2.0, 2.2.1, and 2.2.2 did ship vulnerable openssl-libs, these are
older releases that have been superseded by 2.2.3 and 2.2.4, which include the fix.
No backport remediation is needed.

**Recommendation**: Close TC-8005 as "Not a Bug" -- no currently supported version in
the 2.2.x stream requires remediation. The fix is already present in versions 2.2.3+.

### VEX Justification

If confirmed to close, set VEX Justification (customfield_12345) to:
**Vulnerable Code not Present** -- the latest supported versions (2.2.3, 2.2.4) ship
openssl-libs 3.0.7-28.el9_4 which is at or above the fix threshold.

### Close Comment (would post after engineer confirmation)

```
No supported versions in the 2.2.x stream currently ship a vulnerable version of
openssl-libs. Version impact analysis:

| Version | openssl-libs | Affected? |
|---------|--------------|-----------|
| 2.2.0 | 3.0.7-25.el9_3 | YES (superseded) |
| 2.2.1 | 3.0.7-27.el9_4 | YES (superseded) |
| 2.2.2 | (retag of 2.2.1) | YES (superseded) |
| 2.2.3 | 3.0.7-28.el9_4 | NO |
| 2.2.4 | 3.0.7-28.el9_4 | NO |

Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 which is at or above the
fix threshold. The vulnerability was resolved in the 2.2.x stream as of version 2.2.3
(build v0.4.11, released 2026-03-23).
```

## Cross-Stream Impact (Case B)

The 2.1.x stream is also affected by CVE-2026-40215:

| Version | openssl-libs | Affected? |
|---------|--------------|-----------|
| 2.1.0 | 3.0.7-24.el9 | YES |
| 2.1.1 | 3.0.7-24.el9 | YES |

Both versions in the 2.1.x stream ship openssl-libs 3.0.7-24.el9, which is below the
fix threshold. The 2.1.x stream has NOT picked up the fix.

### Cross-Stream Comment (would post to TC-8005)

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
stream 2.1.x based on rpms.lock.yaml lock file analysis. The 2.1.x stream ships
openssl-libs 3.0.7-24.el9 in all versions (2.1.0, 2.1.1).

This stream is tracked by a companion issue (see Related links) or may require
separate PSIRT triage.
```

### Preemptive Remediation Task for 2.1.x Stream

Since the 2.1.x stream lacks its own CVE Jira for CVE-2026-40215, a preemptive
remediation task would be created (Case B):

```
Summary: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.1)
Labels: ai-generated-jira, Security, CVE-2026-40215, security-preemptive
Link: Related to TC-8005
```

#### Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8005 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Remediate CVE-2026-40215: update base image or rpms.lock.yaml to include patched
openssl-libs (>= 3.0.7-28.el9_4).

Current openssl-libs version in 2.1.x stream: 3.0.7-24.el9 (both 2.1.0 and 2.1.1).
Fixed version: 3.0.7-28.el9_4.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update openssl-libs to >= 3.0.7-28.el9_4 in rpms.lock.yaml (or rpms.in.yaml)
- If openssl-libs is inherited from the base image, check base image vendor for
  an updated version that includes the patched openssl-libs
- Regenerate rpms.lock.yaml after updating the package spec
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in the built container image
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Depends on: TC-8005 (originating CVE tracking issue, cross-stream)
```
