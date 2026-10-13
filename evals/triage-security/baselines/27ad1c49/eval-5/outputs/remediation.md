# Step 8 -- Remediation: TC-8005

## Triage Decision

**Case B: Affected -- create remediation tasks.**

The version impact table shows affected versions within the 2.2.x stream (2.2.0, 2.2.1, 2.2.2). Since the ecosystem is RPM (system package), **one** remediation task is created for the 2.2.x stream.

Additionally, **Case A (cross-stream impact)** applies: the 2.1.x stream is also affected but this issue is scoped to 2.2.x. A cross-stream impact comment would be posted, and preemptive remediation tasks would be created for the 2.1.x stream if no sibling CVE Jira exists for that stream.

## Remediation Task Description (2.2.x stream)

The following is the remediation task description that would be created as a Jira Task, following the system package "Explicit install origin" template from remediation-templates.md:

---

### Jira Task Details

- **Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)
- **Issue Type**: Task
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-40215`
- **Project**: TC

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4), RHTPA 2.2.2 (retag of 2.2.1)
Source tags: v0.4.5, v0.4.8, v0.4.9

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

Note: Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship openssl-libs 3.0.7-28.el9_4 and are not affected. The fix is already present in the latest releases of the 2.2.x stream.

## Implementation Notes

- Update the package version in rpms.in.yaml or the package spec to require openssl-libs >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated package version
- Verify the Konflux build pipeline triggers successfully
- **Dependency type**: explicit install (openssl-libs is present in rpms.lock.yaml)

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Jira Linkage

After creating the remediation task, the following links would be created:

1. **Depend link**: TC-8005 (CVE Vulnerability) -> remediation task (Depend)
2. **Release Task link** (if Step 7.5 produced a release Task): remediation task -> release Task (Blocks)
3. **Release Task CVE link** (if Step 7.5 produced a release Task): release Task -> TC-8005 (Related)

## Cross-Stream Impact (Case A)

Since this is a scoped issue ([rhtpa-2.2]) and the 2.1.x stream is also affected, a cross-stream impact comment would be posted on TC-8005:

> Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects stream 2.1.x based on rpms.lock.yaml analysis. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for the 2.1.x stream, a preemptive remediation task would also be created for 2.1.x using the same system package template but with:
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-40215`, `security-preemptive`
- Link type: "Related" (not "Depend") to TC-8005
- Repository: rhtpa-release.0.3.z
- Description prefix noting preemptive origin from TC-8005 (stream rhtpa-2.2)

## Post-Triage Summary

After all actions complete:
1. Add `ai-cve-triaged` label to TC-8005
2. Post summary comment on TC-8005 documenting:
   - Version impact table
   - Affects Versions correction: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
   - Remediation task key and link
   - Cross-stream impact notice for 2.1.x
   - @mention of the issue reporter
