# Step 7 -- Remediation

## Triage Outcome: Case A + Case B

### Case A: Affected -- create remediation task for 2.2.x stream

The version impact table confirms that versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream ship vulnerable openssl-libs (< 3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 already ship the fixed version. Since this is an RPM ecosystem (system package), a **single remediation task** is created (no upstream backport needed).

Note: Since 2.2.3 and 2.2.4 already include the fixed openssl-libs, the practical impact is limited to environments still running 2.2.0, 2.2.1, or 2.2.2 that have not yet upgraded. The remediation task documents the fix status for tracking purposes.

### Case B: Cross-stream impact -- 2.1.x stream also affected

The cross-stream analysis shows that the 2.1.x stream (versions 2.1.0 and 2.1.1) also ships vulnerable openssl-libs (3.0.7-24.el9, which is < 3.0.7-28.el9_4). Since this issue is scoped to 2.2.x, the 2.1.x stream requires either its own CVE Jira or a preemptive remediation task.

---

## PROPOSED Remediation Task for 2.2.x Stream

### Jira Issue Creation (RPM single-task pattern)

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs X.509 certificate verification
affects versions before 3.0.7-28.el9_4. CVSS: 7.1 (High).

Affected versions in the 2.2.x stream:
- 2.2.0 (openssl-libs 3.0.7-25.el9_3, tag v0.4.5)
- 2.2.1 (openssl-libs 3.0.7-27.el9_4, tag v0.4.8)
- 2.2.2 (retag of 2.2.1)

Already fixed in:
- 2.2.3 (openssl-libs 3.0.7-28.el9_4, tag v0.4.11)
- 2.2.4 (openssl-libs 3.0.7-28.el9_4, tag v0.4.12)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

RPM origin: explicit install (openssl-libs present in rpms.lock.yaml).

## Implementation Notes

- Update the openssl-libs package spec in rpms.in.yaml (or equivalent input file) to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated version
- The fix is available via RHSA-2026:4021
- Verify that no other RPM dependencies conflict with the updated openssl-libs version
- Note: versions 2.2.3+ already ship the fix -- this task ensures the lock file specification explicitly requires the patched version

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

### PROPOSED Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<new-task-key>",
  type: "Depend"
)
```

### PROPOSED Transition

```
jira.transition_issue("TC-8005", status: "In Progress")
```

---

## PROPOSED Cross-Stream Impact Comment (Case B)

```
jira.add_comment("TC-8005", "Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4)
also affects stream 2.1.x based on rpms.lock.yaml analysis:
- 2.1.0: openssl-libs 3.0.7-24.el9 (vulnerable)
- 2.1.1: openssl-libs 3.0.7-24.el9 (vulnerable)

This stream is tracked by companion issues (see Related links) or may require
separate PSIRT triage.")
```

## PROPOSED Preemptive Remediation Task for 2.1.x Stream (Case B)

If no sibling CVE Jira exists for the 2.1.x stream (i.e., no Vulnerability issue with label CVE-2026-40215 and suffix `[rhtpa-2.1]`), create a preemptive remediation task:

### Jira Issue Creation (RPM single-task, preemptive variant)

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.1.x)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215", "security-preemptive"]
)
```

### Preemptive Task Description

```
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

A buffer over-read vulnerability in openssl-libs X.509 certificate verification
affects versions before 3.0.7-28.el9_4. CVSS: 7.1 (High).

Affected versions in the 2.1.x stream:
- 2.1.0 (openssl-libs 3.0.7-24.el9, tag v0.3.8)
- 2.1.1 (openssl-libs 3.0.7-24.el9, tag v0.3.12)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

RPM origin: explicit install (openssl-libs present in rpms.lock.yaml).

## Implementation Notes

- Update the openssl-libs package spec in rpms.in.yaml (or equivalent input file) to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated version
- The fix is available via RHSA-2026:4021
- Verify that no other RPM dependencies conflict with the updated openssl-libs version

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

### PROPOSED Preemptive Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<preemptive-task-key>",
  type: "Related"
)
```

### PROPOSED Comment on TC-8005 Regarding Preemptive Tasks

```
jira.add_comment("TC-8005", "Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-task-key> (security-preemptive)

These tasks use the 'Related' link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.")
```

---

## Post-Triage Summary

### PROPOSED: Add `ai-cve-triaged` label to TC-8005

```
jira.edit_issue("TC-8005", fields={
  "labels": ["CVE-2026-40215", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### PROPOSED: Post-triage summary comment on TC-8005

```
jira.add_comment("TC-8005", "## CVE-2026-40215 Triage Summary

### Version Impact Table (2.2.x stream -- scoped)

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | fixed version |

### Cross-Stream Impact (2.1.x)

| Version | openssl-libs | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 3.0.7-24.el9 | YES |
| 2.1.1 | 3.0.7-24.el9 | YES |

### Affects Versions Correction

[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

### Triage Outcome

- **2.2.x stream**: Remediation task created: <task-key> (RPM update in rhtpa-release.0.4.z)
- **2.1.x stream**: Preemptive remediation task created: <preemptive-task-key> (security-preemptive, RPM update in rhtpa-release.0.3.z)

---
_Generated by triage-security skill_")
```
