# Step 8 -- Remediation: TC-8005 (CVE-2026-40215)

## Triage Outcome

**Case B** -- affected versions exist in the 2.2.x stream. Create remediation task.

Additionally, **Case A** applies -- the 2.1.x stream is also affected (cross-stream impact). A cross-stream impact comment would be posted to TC-8005, and preemptive remediation tasks would be created for the 2.1.x stream if no sibling CVE Jira exists for that stream.

## Ecosystem Classification

- **Ecosystem**: RPM (system package)
- **Tasks per stream**: 1 (Konflux release repo fix only)

## Remediation Task for 2.2.x Stream

### Jira Issue Creation

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
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

Remediate CVE-2026-40215: update openssl-libs to include patched version.
Current rpms.lock.yaml pins openssl-libs to vulnerable versions in builds
v0.4.5 through v0.4.8 (product versions 2.2.0, 2.2.1, 2.2.2).

The fixed version (3.0.7-28.el9_4) is already present in builds v0.4.11+
(product versions 2.2.3, 2.2.4). This task tracks the remediation for
audit and ensures no regression in future builds.

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.9, retag of v0.4.8)
Fixed in: 2.2.3 (v0.4.11) and later

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install (openssl-libs found in rpms.lock.yaml)
- SBOM verification: skipped -- cosign not available
- The fix (openssl-libs 3.0.7-28.el9_4) is already present in builds v0.4.11+
  (product versions 2.2.3 and 2.2.4)
- Verify that rpms.lock.yaml continues to pin openssl-libs >= 3.0.7-28.el9_4
  in all future builds
- If rpms.in.yaml specifies a version constraint for openssl-libs, update it
  to require >= 3.0.7-28.el9_4 to prevent regression

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] No regression in future builds (version constraint prevents downgrade)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Cross-Stream Impact (Case A)

The 2.1.x stream is also affected -- both versions (2.1.0, 2.1.1) ship
openssl-libs 3.0.7-24.el9, which is before the fix version 3.0.7-28.el9_4.

**Cross-stream comment** (would be posted to TC-8005):

> Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also
> affects stream 2.1.x based on rpms.lock.yaml analysis.
> This stream is tracked by a companion issue (see Related links)
> or may require separate PSIRT triage.

If no sibling CVE Jira exists for the 2.1.x stream, a preemptive remediation
task would be created with labels `["ai-generated-jira", "Security",
"CVE-2026-40215", "security-preemptive"]` and linked to TC-8005 with
link type "Related".

## Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```
