# Remediation — CVE-2026-55123 (tokio < 1.42.0)

## Triage Outcome

- **Case A** applies for the current stream (rhtpa-2.2): supported versions RHTPA 2.2.0 and RHTPA 2.2.1 are affected.
- **Case B** applies for cross-stream impact: stream rhtpa-2.1 is also affected and has no sibling CVE Jira.

Ecosystem: **Cargo** (source dependency) -- two tasks per affected stream: upstream backport + downstream propagation.

---

## Case A — Remediation Tasks for Current Stream (rhtpa-2.2)

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

Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (tokio is a direct dependency of backend workspace)

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml / Cargo.lock
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

**Post-creation actions:**
1. Post description digest comment on the upstream task
2. Link upstream task to TC-8020 with "Depend" link type

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

The upstream backport bumps tokio to 1.42.0 on release/0.4.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

**Post-creation actions:**
1. Post description digest comment on the downstream task
2. Link downstream task to TC-8020 with "Depend" link type
3. Link downstream task as blocked by upstream task with "Blocks" link type

---

## Case B — Preemptive Remediation Tasks for Stream rhtpa-2.1

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but has no CVE Jira.
Preemptive remediation tasks are created with the `security-preemptive` label
and linked to TC-8020 with "Related" (not "Depend") link type.

### Task 3: Upstream Backport — Preemptive (rhtpa-2.1)

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
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (tokio is a direct dependency of backend workspace)

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml / Cargo.lock
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

- Depends on: TC-8020 (originating CVE tracking issue, Related link)
```

**Post-creation actions:**
1. Post description digest comment on the preemptive upstream task
2. Link preemptive upstream task to TC-8020 with **"Related"** link type (not "Depend")

### Task 4: Downstream Propagation — Preemptive (rhtpa-2.1)

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
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

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

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (originating CVE tracking issue, Related link)
```

**Post-creation actions:**
1. Post description digest comment on the preemptive downstream task
2. Link preemptive downstream task to TC-8020 with **"Related"** link type
3. Link preemptive downstream task as blocked by preemptive upstream task with "Blocks" link type

---

## Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8020
2. **Transition** TC-8020 to In Progress
3. **Post summary comment** to TC-8020 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.2.0, RHTPA 2.2.1 -- already correct)
   - Remediation tasks created (Case A: upstream + downstream for rhtpa-2.2)
   - Preemptive tasks created (Case B: upstream + downstream for rhtpa-2.1)
   - @mention of the issue reporter
   - Comment Footnote: sdlc-workflow/triage-security v0.13.4
