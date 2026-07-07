# Step 8 -- Remediation: TC-8004

## Triage Outcome: Case A -- Affected (create remediation tasks)

The version impact analysis shows that supported versions in the **2.1.x stream** are affected. The **2.2.x stream** is not affected (all versions ship h2 >= 0.4.8). Since TC-8004 is an **unscoped** issue, Case B (cross-stream impact notice) does NOT apply -- unscoped issues cover all streams by definition, so there are no "other streams outside this issue's scope."

Remediation tasks are created only for the **2.1.x stream** (the only affected stream).

## Ecosystem: Cargo (source dependency) -- Two Tasks

Since h2 is a Cargo (source) dependency, two remediation tasks are required per the source dependency ecosystem pattern:

1. **Upstream backport task** -- fix in the source repo (rhtpa-backend)
2. **Downstream propagation subtask** -- update the reference in the Konflux release repo (rhtpa-release.0.3.z)

---

### Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (build v0.3.8), RHTPA 2.1.1 (build v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (h2 is a direct Cargo dependency of the backend workspace)
- Current h2 version on release/0.3.z: 0.4.5
- Required h2 version: >= 0.4.8

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
- The fix adds a configurable maximum header list size defaulting to 16 KiB
- If the bump introduces breaking API changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

### Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

#### Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

## Jira Operations (proposed)

### Task Creation

```
# 1. Upstream backport task
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)

# 2. Downstream propagation subtask
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Issue Linkage

```
# Link upstream task to CVE Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# Link downstream task to CVE Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Block downstream on upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

### Post-Triage Actions

```
# Add ai-cve-triaged label
jira.edit_issue("TC-8004", fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})

# Transition to In Progress
jira.transition_issue("TC-8004", <in-progress-transition-id>)
```

## Summary

- **Stream 2.1.x**: AFFECTED -- 2 remediation tasks created (upstream backport + downstream propagation)
- **Stream 2.2.x**: NOT AFFECTED -- no remediation needed (ships h2 >= 0.4.8)
- **Case B (cross-stream notice)**: NOT applicable -- issue is unscoped, so cross-stream impact check is skipped
- **Sibling issues**: None found (JQL returned empty)
