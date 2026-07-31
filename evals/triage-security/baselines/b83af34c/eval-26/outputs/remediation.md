# Step 8 -- Remediation

## Triage Decision

**Case B: Affected -- create remediation tasks**

All supported versions in the 2.2.x stream ship criterion 0.5.1, which is within the
affected range (< 0.5.2). Remediation tasks are needed.

**Ecosystem**: Cargo (source dependency) -- 2 tasks per stream:
1. Upstream backport task (fix in source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

**Dev-dependency override**: criterion is a dev-only dependency (declared in
`[dev-dependencies]` in backend/Cargo.toml). Per the dependency scope decision tree:
- Priority is set to **Normal** (overriding the CVE severity of CVSS 5.3 Medium)
- The `dev-dependency` label is added to both tasks
- A note is included indicating the dependency is dev/build-only

---

## Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)
**Issue Type**: Task
**Priority**: Normal
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

### Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: Path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

Upstream fix: _(not available in remote links)_
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (criterion is a direct dev-dependency of backend workspace)
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production
- Priority override: Normal (dev-only dependency, not shipped in production, regardless of CVE severity CVSS 5.3 Medium)

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml ([dev-dependencies] section)
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency
- [ ] Benchmark suite compiles and runs with the updated criterion version

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Issue Type**: Task
**Priority**: Normal
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next build
ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: direct -- carried forward from upstream task
- **Dependency scope**: dev-only ([dev-dependencies]) -- NOT shipped in production
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

## Jira Issue Creation (simulated)

### Upstream backport task:
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

### Downstream propagation subtask:
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

### Linkage:
- Both tasks linked to TC-8050 with "Depend" link type
- Downstream subtask linked to upstream task with "Blocks" link type
