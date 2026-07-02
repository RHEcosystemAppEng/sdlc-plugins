# Step 8 -- Remediation

## Triage Outcome

**Case A: Affected** -- versions 2.2.0, 2.2.1, and 2.2.2 in the scoped
2.2.x stream ship vulnerable openssl-libs (< 3.0.7-28.el9_4).

**Case B: Cross-stream impact** -- the 2.1.x stream is also affected
(both 2.1.0 and 2.1.1 ship openssl-libs 3.0.7-24.el9). A cross-stream
impact comment would be posted to TC-8005 noting that the 2.1.x stream
requires separate triage or a preemptive remediation task.

**Ecosystem: RPM (system package)** -- single remediation task targeting
the Konflux release repo. No upstream backport step needed.

**Already-fixed note:** The fix is already present in 2.2.3+ (build tag
v0.4.11 onward). The remediation task below documents the vulnerability
and the fix that was applied. If no further action is needed (the latest
releases already include the fix), this task can be resolved immediately.

---

## Remediation Task Description

**Summary:** Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)

**Labels:** ai-generated-jira, Security, CVE-2026-40215

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability was found in openssl-libs during X.509
certificate chain verification. Versions before 3.0.7-28.el9_4 are
vulnerable. A remote attacker can craft a certificate with a malformed
Subject Alternative Name extension that triggers an out-of-bounds read,
potentially leaking memory contents or causing a crash.

Affected versions: 2.2.0 (3.0.7-25.el9_3), 2.2.1 (3.0.7-27.el9_4),
2.2.2 (retag of 2.2.1)
Fixed in: 2.2.3+ (3.0.7-28.el9_4, build tag v0.4.11 onward)

CVSS: 7.1 (High)
Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version in rpms.in.yaml / rpms.lock.yaml
  to >= 3.0.7-28.el9_4
- If lock file exists: regenerate rpms.lock.yaml to reflect the updated
  package version
- Note: the fix is already present in build tags v0.4.11 and v0.4.12
  (versions 2.2.3 and 2.2.4). Verify that the current rpms.lock.yaml
  on the main branch includes openssl-libs >= 3.0.7-28.el9_4

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Jira Operations (would be executed)

```
# Create remediation task
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)

# Post description digest comment
task_desc = jira.get_issue(<task-key>, fields=["description"])
python3 scripts/sha256-digest.py /tmp/task-desc.md
jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# Link task to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)

# Add ai-cve-triaged label to TC-8005
jira.edit_issue("TC-8005", labels: [...existing, "ai-cve-triaged"])

# Post cross-stream impact comment to TC-8005
jira.add_comment("TC-8005",
  "Cross-stream impact: openssl-libs (< 3.0.7-28.el9_4) also affects
   stream 2.1.x based on rpms.lock.yaml analysis.
   - 2.1.0: openssl-libs 3.0.7-24.el9 (affected)
   - 2.1.1: openssl-libs 3.0.7-24.el9 (affected)
   This stream is tracked by a companion issue or may require
   separate PSIRT triage.")
```
