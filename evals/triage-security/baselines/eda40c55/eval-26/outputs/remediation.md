# Step 8 -- Remediation: CVE-2026-99001 (criterion)

## Triage Outcome: Case A -- Affected (dev-dependency)

All 2.2.x versions ship criterion 0.5.1 (affected range: < 0.5.2). criterion
is a dev-only dependency (not shipped in production). Per the dependency scope
decision tree, remediation tasks are created with the `dev-dependency` label
and Normal priority override.

## Task 1: Upstream Backport Task

**Summary:** Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Issue Type:** Task

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority:** Normal

### Task Description

```
## Repository

backend

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

Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Update criterion dependency to >= 0.5.2 in Cargo.toml and Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- This is a dev-only dependency ([dev-dependencies] in backend/Cargo.toml),
  used for benchmarks only. It is not shipped in production builds.
  Remediation priority is Normal regardless of CVE severity.
  Label: dev-dependency.

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

### Jira Creation (proposed)

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

---

## Task 2: Downstream Propagation Subtask

**Summary:** Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Issue Type:** Task

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority:** Normal

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

The upstream backport bumps criterion to 0.5.2 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

### Jira Creation (proposed)

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

---

## Jira Linkage (proposed)

```
# Link upstream task to CVE Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8050",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# Link downstream subtask as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# Link downstream task to CVE Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8050",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

## Dev-Dependency Modifications Summary

The following modifications were applied because criterion is a dev-only
dependency (declared in `[dev-dependencies]`, not shipped in production):

1. **Label**: `dev-dependency` added to both upstream and downstream tasks
   alongside standard labels (`ai-generated-jira`, `Security`, `CVE-2026-99001`)
2. **Priority**: Overridden to **Normal** regardless of CVE severity (CVSS 5.3
   Medium). Standard triage would inherit the CVE priority; dev-dependency
   scope reduces this to Normal because the risk is supply chain only.
3. **Description note**: Both task descriptions include the statement:
   "This dependency is dev/build-only and is not shipped in production.
   Remediation priority is Normal (supply chain risk only)."

## Post-Triage Summary Comment (proposed)

The following comment would be posted to TC-8050:

```
Version impact analysis for CVE-2026-99001 (criterion < 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0   | 0.5.1     | YES       |       |
| 2.2.1   | 0.5.1     | YES       |       |
| 2.2.2   | --        | YES       | retag of 2.2.1 |
| 2.2.3   | 0.5.1     | YES       |       |
| 2.2.4   | 0.5.1     | YES       |       |

Dependency scope: dev-only ([dev-dependencies] in backend/Cargo.toml).
Not shipped in production builds. Remediation priority overridden to Normal.

Remediation tasks created:
- <upstream-task-key> (upstream backport: bump criterion to 0.5.2, dev-dependency, Normal priority)
- <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>, dev-dependency, Normal priority)

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.12.2.
```
