# Step 8 -- Remediation

## Triage Outcome

**Case A** applies: supported versions within the scoped 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2). Remediation task creation is required.

**Case B** also applies: cross-stream impact detected. The 2.1.x stream (versions 2.1.0, 2.1.1) is also affected but is outside this issue's scope. A cross-stream impact comment would be posted and preemptive remediation tasks created for the 2.1.x stream if no companion CVE Jira exists.

**Ecosystem**: RPM (system package) -- **one** remediation task per stream. No upstream backport task needed.

---

## Remediation Task -- 2.2.x stream

Since openssl-libs is an RPM package present in rpms.lock.yaml (explicit install origin), the remediation uses the **explicit install** template.

### Jira Issue Creation

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

A buffer over-read vulnerability was found in openssl-libs during X.509 certificate
chain verification. Versions before 3.0.7-28.el9_4 are vulnerable. A remote attacker
can craft a certificate with a malformed extension that triggers an out-of-bounds read,
potentially leaking sensitive memory contents or causing a crash.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4), RHTPA 2.2.2 (3.0.7-27.el9_4, retag of 2.2.1)
Source tags: v0.4.5, v0.4.8, v0.4.9

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install (openssl-libs is present in rpms.lock.yaml)
- Update the package version in rpms.lock.yaml (or rpms.in.yaml if applicable) to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml if using an input specification file
- Note: versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship the fixed openssl-libs 3.0.7-28.el9_4 -- no action needed for those versions
- SBOM verification was skipped (cosign not available) -- rpms.lock.yaml classification used

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Linkage

After task creation:

1. Link the remediation task to TC-8005:
   ```
   jira.create_link(
     inwardIssue: "TC-8005",
     outwardIssue: "<task-key>",
     type: "Depend"
   )
   ```

2. Transition TC-8005 to In Progress.

3. Add comment to TC-8005 listing the created task:
   "Remediation task created: <task-key>"

## Cross-Stream Impact (Case B)

Cross-stream impact comment for TC-8005:

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
stream 2.1.x based on rpms.lock.yaml analysis:
  - 2.1.0 (v0.3.8): openssl-libs 3.0.7-24.el9
  - 2.1.1 (v0.3.12): openssl-libs 3.0.7-24.el9

These versions are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

If no companion CVE Jira exists for the 2.1.x stream, a preemptive remediation task
would be created with the `security-preemptive` label and "Related" link type to TC-8005:

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.1)",
  description: <same template with preemptive prefix and 2.1.x stream context>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215", "security-preemptive"]
)
```
