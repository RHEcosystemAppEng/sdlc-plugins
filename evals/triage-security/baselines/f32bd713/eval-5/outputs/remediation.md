# Step 8 — Remediation: TC-8005 (CVE-2026-40215, openssl-libs)

## Triage Outcome

**Case B: Affected — create remediation task** for the 2.2.x stream.

Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable openssl-libs (before
3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 already include the fix.

**Ecosystem**: RPM (system package) — **1 remediation task** for the
Konflux release repo.

**Case A: Cross-stream impact** also applies — the 2.1.x stream is affected
(all versions ship openssl-libs < 3.0.7-28.el9_4). A cross-stream notice
should be posted and preemptive remediation tasks created for 2.1.x if no
sibling CVE Jira exists for that stream.

---

## Remediation Task Description (2.2.x stream — explicit install)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability was found in openssl-libs during X.509
certificate chain verification. Versions before 3.0.7-28.el9_4 are
vulnerable (CVSS 7.1 High). The fix adds bounds checking before reading
extension data in X509_verify_cert().

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8),
RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

Note: versions 2.2.3+ already ship the fixed openssl-libs 3.0.7-28.el9_4.
This remediation ensures any future rebuild from the affected source commits
or lock file state picks up the patched package.

## Implementation Notes

- Update the package version for openssl-libs in rpms.lock.yaml
  (and rpms.in.yaml if present) to require >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to resolve the updated package version
  from Red Hat errata RHSA-2026:4021
- The fix is already available in the RHEL 9.4 package repositories
  (openssl-libs-3.0.7-28.el9_4)
- **Dependency type**: direct (openssl-libs is explicitly installed
  per rpms.lock.yaml)
- **RPM origin**: explicit install (confirmed present in rpms.lock.yaml
  at all checked build tags)
- **SBOM verification**: skipped -- cosign not available. Using
  rpms.lock.yaml classification only.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

## Jira Issue Creation Details

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

## Jira Linkage

1. Link remediation task to TC-8005 (Depend):
   ```
   jira.create_link(inwardIssue: "TC-8005", outwardIssue: <task-key>, type: "Depend")
   ```

2. Link remediation task to release Task (Blocks) if release Jira is active:
   ```
   jira.create_link(inwardIssue: <task-key>, outwardIssue: <release-task-key>, type: "Blocks")
   ```

3. Link CVE to release Task (Related):
   ```
   jira.create_link(inwardIssue: <release-task-key>, outwardIssue: "TC-8005", type: "Related")
   ```

## Cross-Stream Impact Notice (Case A)

The following cross-stream comment would be posted to TC-8005:

> Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also
> affects stream 2.1.x based on rpms.lock.yaml analysis.
> All 2.1.x versions (2.1.0, 2.1.1) ship openssl-libs 3.0.7-24.el9.
> This stream is tracked by companion issues (see Related links)
> or may require separate PSIRT triage.

If no sibling CVE Jira exists for the 2.1.x stream, a preemptive remediation
task would be created with the `security-preemptive` label and linked to
TC-8005 via "Related" (not "Depend").

## Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8005
2. Post summary comment to TC-8005 with version impact table, Affects Versions
   correction, remediation task links, and cross-stream notice
3. Transition TC-8005 to In Progress
