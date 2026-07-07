# Step 8 -- Remediation: CVE-2026-99001

## Triage Outcome

- **Case A**: Affected -- all 2.2.x versions ship criterion 0.5.1 (< 0.5.2)
- **Case B**: Cross-stream impact -- 2.1.x stream is also affected but is
  outside this issue's scope (TC-8050 is scoped to 2.2.x)
- **Dev-dependency override**: criterion is a dev-only dependency; priority
  overridden to Normal, `dev-dependency` label applied

## Remediation Tasks for 2.2.x Stream

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

Upstream fix: -- (no upstream PR link available)
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) --
  NOT shipped in production. Used for benchmarks only.

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml
  `[dev-dependencies]` section
- Run `cargo update -p criterion` to update Cargo.lock
- If the bump introduces breaking API changes to benchmark code, assess
  whether benchmark updates are viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

## Jira Issue Creation (pseudocode)

```
# 1. Upstream backport task
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)

# 2. Downstream propagation subtask
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)

# 3. Link upstream task to CVE Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8050",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# 4. Link downstream task blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# 5. Link downstream task to CVE Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8050",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

## Cross-Stream Impact (Case B)

The 2.1.x stream is also affected (criterion 0.5.1 in all 2.1.x versions).
Since TC-8050 is scoped to the 2.2.x stream, a cross-stream impact comment
would be posted to TC-8050:

> Cross-stream impact: criterion < 0.5.2 also affects stream 2.1.x based on
> lock file analysis. This stream is tracked by a companion issue (see Related
> links) or may require separate PSIRT triage.

If no CVE Jira exists for the 2.1.x stream, preemptive remediation tasks
would be created with the `security-preemptive` label using the "Related"
link type. Those tasks would also carry the `dev-dependency` label and Normal
priority since the dependency scope carries across streams.

## Dev-Dependency Summary

| Attribute | Value |
|-----------|-------|
| Dependency | criterion |
| Declared in | `[dev-dependencies]` in backend/Cargo.toml |
| Shipped in production | NO |
| Risk type | Supply chain only |
| Labels added | `dev-dependency` (in addition to `ai-generated-jira`, `Security`, `CVE-2026-99001`) |
| Priority override | Normal (overrides CVE severity of Medium/5.3) |
| Task description note | "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)." |
