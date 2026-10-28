# Step 8 -- Remediation

## Triage Outcome

**Case B: Affected -- create remediation task**

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2) that shipped vulnerable openssl-libs. Although versions 2.2.3 and 2.2.4 already ship the fixed version (3.0.7-28.el9_4), the earlier releases within the stream were affected and the Affects Versions must be recorded for traceability.

**Ecosystem**: RPM (system package) -- 1 remediation task for the Konflux release repo.

**Cross-stream impact (Case A)**: The 2.1.x stream is also affected (all versions ship openssl-libs 3.0.7-24.el9). A cross-stream impact comment would be posted to TC-8005 noting the 2.1.x stream impact. Preemptive remediation tasks for the 2.1.x stream would be created if no companion CVE Jira exists for that stream.

---

## Remediation Task Description (2.2.x stream -- System Package)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 in
rhtpa-release.0.4.z.

A buffer over-read vulnerability was found in openssl-libs versions before
3.0.7-28.el9_4 during X.509 certificate chain verification. A remote attacker
can craft a certificate with a malformed extension that triggers an out-of-bounds
read, potentially leaking sensitive memory contents or causing a crash.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4),
RHTPA 2.2.2 (retag of 2.2.1)
Fixed in versions: RHTPA 2.2.3+ (3.0.7-28.el9_4)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215
CVSS: 7.1 (High)

## Implementation Notes

- Package origin: explicit install (openssl-libs found in rpms.lock.yaml)
- SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml
  classification only.
- The fix (3.0.7-28.el9_4) is already present in builds 0.4.11+ (versions
  2.2.3 and 2.2.4). Verify that rpms.lock.yaml and rpms.in.yaml (if applicable)
  specify openssl-libs >= 3.0.7-28.el9_4 to prevent regression in future builds.
- If rpms.lock.yaml pins a specific version, ensure the pin is at or above the
  fixed version.
- Regenerate rpms.lock.yaml if updating rpms.in.yaml.
- Verify the Konflux build pipeline triggers successfully after the update.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] No regression in future builds (version pin prevents downgrade)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

---

## Jira Operations Summary

The following Jira operations would be performed after engineer confirmation:

1. **Create remediation Task**:
   - Summary: `Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)`
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-40215`
   - Description: as above

2. **Post description digest comment** on the new task (before links).

3. **Link** the remediation task to TC-8005 with link type `Depend`.

4. **Link** the remediation task to the release Task (if release Jira orchestration
   is active from Step 7.5) with link type `Blocks`.

5. **Link** TC-8005 to the release Task with link type `Related`.

6. **Add `ai-cve-triaged` label** to TC-8005.

7. **Post summary comment** to TC-8005 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 --> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation task key
   - Cross-stream impact on 2.1.x
