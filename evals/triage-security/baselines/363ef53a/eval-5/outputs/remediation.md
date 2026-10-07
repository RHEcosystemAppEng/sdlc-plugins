# Step 8 -- Remediation Task for TC-8005

## Triage Outcome

**Case B: Affected -- create remediation tasks.**

Versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream are affected.
Ecosystem is RPM (system package) so 1 remediation task is created for the
Konflux release repo.

**Cross-stream impact (Case A)**: The 2.1.x stream is also affected (versions
2.1.0 and 2.1.1 ship openssl-libs 3.0.7-24.el9). A cross-stream impact comment
would be posted to TC-8005, and preemptive remediation tasks would be created
for the 2.1.x stream if no companion CVE Jira exists for that stream.

---

## Remediation Task Description (2.2.x stream -- explicit install origin)

### Jira Issue Creation

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <task-description-below>,
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

A buffer over-read vulnerability in openssl-libs versions before
3.0.7-28.el9_4 allows a remote attacker to craft a certificate with a
malformed Subject Alternative Name extension that triggers an out-of-bounds
read during X.509 certificate chain verification.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4),
RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1), v0.4.8 (2.2.2 retag)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Origin: explicit install (openssl-libs is present in rpms.lock.yaml)
- SBOM verification: skipped -- cosign not available
- Update the openssl-libs package version in rpms.in.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated package version
- The fixed version (3.0.7-28.el9_4) is already available via RHSA-2026:4021 errata
- Verify the Konflux build pipeline triggers successfully after the update
- Note: versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship
  openssl-libs 3.0.7-28.el9_4 -- this confirms the fix is available in
  the package repositories

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Jira Linkage

After task creation:

```
# Link remediation task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)

# Link remediation task to release Task (if Step 7.5 produced one)
jira.create_link(
  inwardIssue: <task-key>,
  outwardIssue: <release-task-key>,
  type: "Blocks"
)

# Link CVE to release Task (traceability)
jira.create_link(
  inwardIssue: <release-task-key>,
  outwardIssue: "TC-8005",
  type: "Related"
)
```

## Pre-Creation Checklist

- [x] Task count per stream: 1 task (RPM / system package ecosystem)
- [x] Cross-stream coverage: 2.1.x stream is also affected -- preemptive
      task or companion CVE Jira needed for that stream
- [x] Link types: "Depend" for task linked to TC-8005
- [x] Preemptive labels: N/A for this task (scoped to issue's own stream)
- [x] Coordination guidance: omitted (Deployment Context column absent
      from Source Repositories table)
- [x] Release Jira linking: remediation Task -> release Task (Blocks),
      CVE -> release Task (Related) -- pending Step 7.5 output
- [x] Dedup consistency: no prior dedup detected
