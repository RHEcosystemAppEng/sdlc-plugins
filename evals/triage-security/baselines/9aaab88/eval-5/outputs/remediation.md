# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected, create remediation task

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). Since openssl-libs is an RPM system package (not a source dependency), a **single remediation task** is created for the Konflux release repo. No upstream backport task is needed.

### Package Origin Classification

openssl-libs is classified as an **explicit install** -- it is present in `rpms.lock.yaml` for all 2.2.x versions. Remediation follows the "Explicit install origin" template.

---

## Remediation Task: Update openssl-libs in Konflux release repo (2.2.x)

**Jira Creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <see task description below>,
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

Versions of openssl-libs before 3.0.7-28.el9_4 are vulnerable to a buffer over-read during X.509 certificate chain verification (CVSS 7.1 High). A remote attacker can craft a certificate with a malformed extension that triggers an out-of-bounds read.

Affected versions: 2.2.0 (3.0.7-25.el9_3), 2.2.1 (3.0.7-27.el9_4), 2.2.2 (retag of 2.2.1)
Fixed in versions: 2.2.3+ (3.0.7-28.el9_4)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version in Dockerfile (dnf install command or package spec)
- If lock file exists: regenerate rpms.lock.yaml
- Target version: openssl-libs >= 3.0.7-28.el9_4
- The fix is available via RHSA-2026:4021 from RPM repositories
- Package origin: explicit install (present in rpms.lock.yaml)

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

---

## Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```

## Cross-Stream Impact (Case B)

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship openssl-libs 3.0.7-24.el9). This is outside the current issue's scope (scoped to 2.2.x via `[rhtpa-2.2]` suffix).

Cross-stream impact comment to post on TC-8005:

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
stream 2.1.x based on rpms.lock.yaml analysis.
This stream is tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

If no companion CVE Jira exists for the 2.1.x stream, a preemptive remediation task would be created with `security-preemptive` label and "Related" link to TC-8005.
