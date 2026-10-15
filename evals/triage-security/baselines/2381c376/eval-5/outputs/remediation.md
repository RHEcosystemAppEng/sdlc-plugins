# Step 8 -- Remediation

## Triage Decision

### Scoped stream (2.2.x) -- Case B with already-fixed outcome

The version impact table shows that versions 2.2.0, 2.2.1, and 2.2.2 shipped the vulnerable openssl-libs, but the fix is **already present** in versions 2.2.3 and 2.2.4 (both ship 3.0.7-28.el9_4). Because the latest releases in the 2.2.x stream already include the patched package, **no new remediation task is required** for the 2.2.x stream.

The Affects Versions have been corrected (Step 3) to document which versions were affected: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.

### Cross-stream impact (2.1.x) -- Case A: preemptive remediation

The issue is scoped to 2.2.x, but the version impact analysis shows that the **2.1.x stream is also affected** (all versions ship openssl-libs 3.0.7-24.el9). Since no sibling CVE Jira was found for the 2.1.x stream in the mock data, a **preemptive remediation task** would be created for the 2.1.x stream.

Ecosystem: RPM (system package) -- 1 task per stream.

---

## Preemptive Remediation Task Description (2.1.x stream)

The following task would be created as a preemptive remediation for the 2.1.x stream, using the system package (RPM) explicit install template:

```
Summary: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.1)
Issue Type: Task
Labels: ai-generated-jira, Security, CVE-2026-40215, security-preemptive
Link: Related to TC-8005 (originating CVE Jira, different stream)
```

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8005 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for the 2.1.x stream. When PSIRT creates one, this task will be
> linked and the `security-preemptive` label removed.

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability exists in openssl-libs versions before
3.0.7-28.el9_4 during X.509 certificate chain verification. A remote attacker
can craft a certificate with a malformed extension that triggers an out-of-bounds
read, potentially leaking sensitive memory contents or causing a crash.

Affected versions in this stream:
- 2.1.0 (build v0.3.8): openssl-libs 3.0.7-24.el9
- 2.1.1 (build v0.3.12): openssl-libs 3.0.7-24.el9

Source commit(s): v0.3.8, v0.3.12

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: **explicit install** (openssl-libs present in rpms.lock.yaml)
- SBOM verification: skipped -- cosign not available
- Update the openssl-libs package version in rpms.in.yaml / rpms.lock.yaml
  to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml after updating the package spec
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Related to: TC-8005 (originating CVE Jira for 2.2.x stream, cross-stream link)

---

## Proposed Jira Actions (not executed)

### For the 2.2.x scoped stream

1. **No remediation task created** -- the fix is already present in versions 2.2.3+.
2. **Post cross-stream impact comment** on TC-8005:

   ```
   Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also
   affects stream 2.1.x based on rpms.lock.yaml analysis.
   Stream 2.1.x ships openssl-libs 3.0.7-24.el9 in all versions (2.1.0, 2.1.1).
   These streams are tracked by companion issues (see Related links)
   or may require separate PSIRT triage.
   ```

3. **Add `ai-cve-triaged` label** to TC-8005.

### For the 2.1.x cross-stream

1. **Create preemptive remediation task** (as described above) with labels
   `[ai-generated-jira, Security, CVE-2026-40215, security-preemptive]`.
2. **Link** the preemptive task to TC-8005 with link type "Related"
   (not "Depend", because TC-8005 belongs to a different stream).
3. **Post comment** on TC-8005 listing the preemptive task:

   ```
   Preemptive remediation tasks created for streams without CVE Jiras:
   - 2.1.x: <preemptive-task-key> (security-preemptive)

   These tasks use the "Related" link type and carry the security-preemptive
   label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
   reconciliation will link them and remove the label.
   ```

### Post-triage summary comment on TC-8005

```
CVE-2026-40215 triage summary for TC-8005 [rhtpa-2.2]:

Version impact (2.2.x stream):
| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fixed version |

Affects Versions corrected: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Triage outcome: Fix already present in 2.2.3+ (openssl-libs 3.0.7-28.el9_4).
No new remediation task required for the 2.2.x stream.

Cross-stream impact:
- 2.1.x: all versions affected (openssl-libs 3.0.7-24.el9)
  Preemptive remediation task: <preemptive-task-key> (security-preemptive)
```
