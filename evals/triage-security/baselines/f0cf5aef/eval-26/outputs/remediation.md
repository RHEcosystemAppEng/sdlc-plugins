# Step 8 -- Remediation

## Triage Outcome

**Case B: Affected -- create remediation tasks**

All supported versions in the 2.2.x stream ship criterion 0.5.1, which is within
the affected range (< 0.5.2). Remediation tasks are required.

**Dev-dependency override applies:** criterion is a dev-only dependency
([dev-dependencies] in backend/Cargo.toml). Per the dependency scope decision tree:
- Label: `dev-dependency` added to all remediation tasks
- Priority: **Normal** (overrides CVE severity of Medium / 5.3)
- Description note: dev/build-only, not shipped in production

## Cross-Stream Impact (Case A)

The 2.1.x stream is also affected (criterion 0.5.1 in all versions).
A cross-stream impact comment would be posted to TC-8050:

> Cross-stream impact: criterion < 0.5.2 also affects stream 2.1.x based on
> lock file analysis. This stream is tracked by a companion issue (see Related
> links) or may require separate PSIRT triage.

If no CVE Jira exists for the 2.1.x stream, preemptive remediation tasks would
be created with the `security-preemptive` label and "Related" link type.

---

## Remediation Task 1: Upstream Backport (2.2.x stream)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

**Link**: Depend -> TC-8050

### Task Description

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
Source commits: v0.4.5, v0.4.8, v0.4.9 (retag), v0.4.11, v0.4.12

Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency (chain: backend -> criterion)
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production builds, used for benchmarks only

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

## Remediation Task 2: Downstream Propagation (2.2.x stream)

**Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

**Link**: Depend -> TC-8050, Blocked by upstream task (Task 1)

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

The upstream backport task bumps criterion to 0.5.2 on release/0.4.z. Once
that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

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

## Jira API Calls (simulated)

### Task 1 -- Upstream Backport

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

### Task 2 -- Downstream Propagation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

### Linkage

```
# Link upstream task to CVE
jira.create_link(inwardIssue: "TC-8050", outwardIssue: <upstream-task-key>, type: "Depend")

# Link downstream task to CVE
jira.create_link(inwardIssue: "TC-8050", outwardIssue: <downstream-task-key>, type: "Depend")

# Block downstream on upstream
jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
```

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks (source dependency ecosystem: Cargo) -- upstream backport + downstream propagation
- [x] **Cross-stream coverage**: 2.1.x stream identified as affected; preemptive tasks or existing sibling CVE Jira needed
- [x] **Link types**: "Depend" for tasks linked to TC-8050, "Blocks" for upstream -> downstream
- [x] **Dev-dependency label**: `dev-dependency` label applied to all tasks
- [x] **Priority override**: Normal priority set (overrides CVE Medium severity) because criterion is dev-only
- [x] **Dev-only note**: Description includes "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."
