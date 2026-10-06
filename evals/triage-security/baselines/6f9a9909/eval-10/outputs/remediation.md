# Remediation — CVE-2026-55123 (tokio < 1.42.0)

## Triage Decision

- **Issue TC-8020** is scoped to stream **rhtpa-2.2**
- Version impact shows **rhtpa-2.2** versions are affected (Case B: create remediation tasks)
- Version impact also shows **rhtpa-2.1** is affected but has no CVE Jira (Case A: cross-stream impact + preemptive tasks)
- Ecosystem: Cargo (source dependency) -- 2 tasks per stream (upstream backport + downstream propagation)

---

## Case B — Remediation Tasks for Current Stream (rhtpa-2.2)

### Task 1: Upstream Backport (rhtpa-2.2)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

**Post-creation:**
- Post description digest comment per description-digest-protocol.md
- Link to TC-8020 with type "Depend"

---

### Task 2: Downstream Propagation (rhtpa-2.2)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0 on release/0.4.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

**Post-creation:**
- Post description digest comment per description-digest-protocol.md
- Link to TC-8020 with type "Depend"
- Link downstream blocked by upstream task with type "Blocks"

---

## Case A — Preemptive Remediation Tasks for rhtpa-2.1

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but has **no CVE Jira**.
Preemptive remediation tasks are created with the `security-preemptive` label
and linked to TC-8020 with "Related" (not "Depend").

### Preemptive Task 1: Upstream Backport (rhtpa-2.1)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for stream rhtpa-2.1. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (originating CVE Jira, stream rhtpa-2.2 — Related link)
```

**Post-creation:**
- Post description digest comment per description-digest-protocol.md
- Link to TC-8020 with type "Related" (preemptive — originating CVE is in a different stream)

---

### Preemptive Task 2: Downstream Propagation (rhtpa-2.1)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for stream rhtpa-2.1. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (originating CVE Jira, stream rhtpa-2.2 — Related link)
```

**Post-creation:**
- Post description digest comment per description-digest-protocol.md
- Link to TC-8020 with type "Related" (preemptive)
- Link downstream blocked by preemptive upstream task with type "Blocks"

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -> 2 tasks per stream. rhtpa-2.2: 2 tasks, rhtpa-2.1: 2 preemptive tasks. Total: 4 tasks.
- [x] **Cross-stream coverage**: rhtpa-2.1 (outside issue scope) has no sibling CVE Jira -> preemptive tasks created.
- [x] **Link types**: "Depend" for rhtpa-2.2 tasks linked to TC-8020; "Related" for rhtpa-2.1 preemptive tasks linked to TC-8020; "Blocks" for upstream -> downstream within each stream.
- [x] **Preemptive labels**: rhtpa-2.1 tasks carry `security-preemptive` label.
- [x] **Coordination guidance**: each task includes upstream coordination guidance (deployment context: upstream).

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8020.
2. Post summary comment to TC-8020 with version impact table, Affects Versions status, triage outcome, and links to all created remediation tasks.
3. Comment footnote: `sdlc-workflow/triage-security v0.13.9`.
