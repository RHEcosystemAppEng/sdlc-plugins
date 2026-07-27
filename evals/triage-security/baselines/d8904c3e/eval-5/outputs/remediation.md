# Step 8 -- Remediation: CVE-2026-40215

## Triage Outcome

**Case B** (Affected -- create remediation tasks) with **Case A** cross-stream
impact notice.

- Ecosystem: RPM (system package) -- 1 task for the scoped stream (2.2.x)
- Cross-stream impact: 2.1.x is also affected -- post cross-stream notice
- Package origin: explicit install (openssl-libs found in rpms.lock.yaml)

## Cross-Stream Impact Comment (Case A)

```
Cross-stream impact: openssl-libs versions before 3.0.7-28.el9_4 also affects
stream(s) 2.1.x based on rpms.lock.yaml analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

## Remediation Task: 2.2.x Stream

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-40215

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.
Current versions in affected releases ship openssl-libs before 3.0.7-28.el9_4,
which is vulnerable to a buffer over-read during X.509 certificate chain
verification.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4),
RHTPA 2.2.2 (retag of 2.2.1, 3.0.7-27.el9_4)

Versions already fixed: RHTPA 2.2.3 (3.0.7-28.el9_4), RHTPA 2.2.4 (3.0.7-28.el9_4)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install (openssl-libs found in rpms.lock.yaml)
- Update the openssl-libs package version in rpms.in.yaml / rpms.lock.yaml
  to >= 3.0.7-28.el9_4
- If lock file exists: regenerate rpms.lock.yaml after updating the package spec
- SBOM verification was skipped (cosign not available) -- rpms.lock.yaml
  classification used as sole determination of package origin

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Jira Operations

### Task Creation

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```

### Transition

Transition TC-8005 to In Progress after task creation.
