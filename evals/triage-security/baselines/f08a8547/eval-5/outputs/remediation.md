# Step 8 -- Remediation

## Triage Outcome

**Case A + Case B apply.**

- **Case A (cross-stream impact)**: The 2.1.x stream is also affected (openssl-libs 3.0.7-24.el9 at both versions). Since TC-8005 is scoped to 2.2.x, a cross-stream impact comment would be posted. If no companion CVE Jira exists for stream 2.1.x, a preemptive remediation task would be created with the `security-preemptive` label.
- **Case B (affected -- create remediation tasks)**: The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). Since openssl-libs is an RPM system package, **1 remediation task** is created for the 2.2.x stream.

---

## Remediation Task -- 2.2.x Stream (Explicit Install RPM)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs affects X.509 certificate chain
verification. Versions before 3.0.7-28.el9_4 are vulnerable to an out-of-bounds
read via a malformed Subject Alternative Name extension, potentially leaking
sensitive memory contents or causing a crash. CVSS: 7.1 (High).

Affected product versions (2.2.x stream):
- RHTPA 2.2.0 (build v0.4.5): openssl-libs 3.0.7-25.el9_3
- RHTPA 2.2.1 (build v0.4.8): openssl-libs 3.0.7-27.el9_4
- RHTPA 2.2.2 (build v0.4.9): retag of 2.2.1

Fixed in versions 2.2.3+ (openssl-libs 3.0.7-28.el9_4 already present).

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: **explicit install** (openssl-libs is present in rpms.lock.yaml)
- SBOM verification was skipped (cosign not available)
- Update the openssl-libs package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4
- If rpms.lock.yaml is auto-generated, update the input spec (rpms.in.yaml or equivalent) and regenerate the lock file
- Verify the Konflux build pipeline triggers successfully after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs package is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image
- [ ] No other package dependency conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent Vulnerability tracking issue)

---

## Cross-Stream Impact Comment (Case A)

The following comment would be posted to TC-8005:

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
stream 2.1.x based on rpms.lock.yaml analysis.

2.1.x versions affected:
- 2.1.0 (v0.3.8): openssl-libs 3.0.7-24.el9
- 2.1.1 (v0.3.12): openssl-libs 3.0.7-24.el9

These versions are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

If no companion CVE Jira exists for the 2.1.x stream, a preemptive remediation task
would be created with the `security-preemptive` label and linked to TC-8005 with
a "Related" link type. The preemptive task would follow the same system package
(explicit install) template above, targeting rhtpa-release.0.3.z instead.

---

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8005
2. Post summary comment to TC-8005 with:
   - Version impact table (both streams)
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation task link(s)
   - @mention of the issue reporter
3. Link remediation task(s) to TC-8005 with "Depend" link type
4. Transition TC-8005 to In Progress
