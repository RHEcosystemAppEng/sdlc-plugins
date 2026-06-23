# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected (2.1.x stream only)

The version impact analysis shows a **mixed result**:
- **2.1.x stream**: AFFECTED -- all versions (2.1.0, 2.1.1) ship h2 0.4.5 (< 0.4.8)
- **2.2.x stream**: NOT AFFECTED -- all versions ship h2 >= 0.4.8

Remediation tasks are created for the **2.1.x stream only**. No remediation is needed for the 2.2.x stream since it already ships the fixed version.

**Cross-stream impact notice**: Not applicable. The issue is unscoped (no stream suffix), so cross-stream notices are not generated. The version impact table already covers all streams.

**Sibling issues**: No sibling Vulnerability issues exist for CVE-2026-33501.

## Remediation Tasks (2.1.x stream)

Since h2 is a **Cargo** (source dependency) ecosystem, two tasks are required: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: 2.1.0 (tag v0.3.8), 2.1.1 (tag v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## Jira Operations

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
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Linkage

```
# Link upstream task to Vulnerability issue
jira.create_link(inwardIssue: "TC-8004", outwardIssue: <upstream-task-key>, type: "Depend")

# Link downstream subtask to Vulnerability issue
jira.create_link(inwardIssue: "TC-8004", outwardIssue: <downstream-task-key>, type: "Depend")

# Link downstream subtask as blocked by upstream task
jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
```

### Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8004
2. Transition TC-8004 to In Progress
3. Assign TC-8004 to current user
4. Post summary comment to TC-8004 documenting version impact, Affects Versions correction, and remediation task links
